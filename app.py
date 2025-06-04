import os
from typing import List, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS
from lib.app_logger import logger, trim_log_file
from lib.query_generation import generate_search_queries, check_ollama_connection_health
from lib.text_processing import extract_keywords, detect_language
from lib.types.StreamResponse import StreamResponse, StreamProcessStatus
from lib.word_extraction import read_file_from_bytes
from lib.youtube_interactions import search_youtube_videos, Video

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://yt-reference-finder-frontend.vercel.app"])  # Allow requests only from http://localhost:3000

MAX_QUERIES_TO_GENERATE = 2  # Numero massimo di query da generare, che poi verranno passate a youtube per la ricerca


def rank_videos(notes_text, videos: List[Video]):
    # Ordina i video per punteggio di engagement
    ranked_videos = sorted(videos, key=lambda x: x.engagement_score, reverse=True)
    return ranked_videos


def filter_unique_videos(all_videos):
    unique_videos = []
    seen_ids = set()
    for video in all_videos:
        if video.video_id not in seen_ids:
            unique_videos.append(video)
            seen_ids.add(video.video_id)
    return unique_videos


@app.route('/')
@app.route('/about', methods=['GET'])
def about():
    return jsonify(
        {'about': 'This is a simple API to extract keywords from a text and search YouTube videos based on them.'})


@app.route('/health', methods=['GET'])
def health_check():
    is_ollama_connection_healthy = check_ollama_connection_health()
    return jsonify(
        {'status': 'ok', 'message': 'API is running', 'ollama_connection_healthy': is_ollama_connection_healthy})


@app.route('/logs', methods=['GET'])
def get_api_logs():
    try:
        with open('app.log', 'r', encoding='utf-8') as f:
            logs = f.readlines()
        return jsonify({'logs': logs})
    except Exception as e:
        logger.error(f"Error reading logs: {e}")
        return jsonify({'error': 'Could not read logs'}), 500


def generate_process_stream(file_bytes_arg: Optional[bytes], original_filename_arg: Optional[str], form_text_arg: str):
    text_from_file = ""
    try:
        if file_bytes_arg is not None and original_filename_arg:
            logger.info(f"Received file for streaming: {original_filename_arg} ({len(file_bytes_arg)} bytes)")
            yield StreamResponse(status=StreamProcessStatus.FILE_RECEIVED, filename=original_filename_arg).to_json()

            read_suc, text_from_file_content = read_file_from_bytes(file_bytes_arg, original_filename_arg)
            if not read_suc:
                yield StreamResponse(status=StreamProcessStatus.ERROR,
                                     message='File format not supported or error reading file content',
                                     filename=original_filename_arg).to_json()
                return
            text_from_file = text_from_file_content  # Assegna il contenuto letto
            yield StreamResponse(status=StreamProcessStatus.FILE_PROCESSED, filename=original_filename_arg,
                                 file_content=text_from_file).to_json()

        # Combina testo da file e da form
        text_parts = []
        if text_from_file.strip():
            text_parts.append(text_from_file.strip())
        if form_text_arg and form_text_arg.strip():
            text_parts.append(form_text_arg.strip())

        text = "\n".join(text_parts).strip()

        if not text:
            logger.error("No text provided")
            yield StreamResponse(status=StreamProcessStatus.ERROR, message='No text provided').to_json()
            return

        logger.info(f"Processing text: {text[:100]}\n...\n{text[-100:]}")
        yield StreamResponse(status=StreamProcessStatus.EXTRACTING_KEYWORDS).to_json()

        detected_language = detect_language(text)

        keywords_data = extract_keywords(text=text, top_n=15, n_word_range=(1, 5), algorithm='yake', language=detected_language)
        logger.info(f"Extracted Keywords: {keywords_data}")
        yield StreamResponse(status=StreamProcessStatus.KEYWORDS_EXTRACTED, keywords=keywords_data).to_json()

        yield StreamResponse(status=StreamProcessStatus.GENERATING_QUERIES).to_json()
        queries = generate_search_queries(keywords=keywords_data, num_queries=MAX_QUERIES_TO_GENERATE, query_language=detected_language)
        logger.info(f"Generated Queries: {queries}")

        if not queries or len(queries) == 0:
            logger.warning(f"No queries generated from keywords, MAX_QUERIES_TO_GENERATE={MAX_QUERIES_TO_GENERATE}")

        yield StreamResponse(status=StreamProcessStatus.QUERIES_GENERATED, queries=queries).to_json()

        yield StreamResponse(status=StreamProcessStatus.YOUTUBE_SEARCH_STARTED, queries=queries).to_json()
        all_videos = []
        with app.app_context():
            for i, query in enumerate(queries):
                try:
                    videos = search_youtube_videos(query, video_language=detected_language)
                    all_videos.extend(videos)
                    logger.info(f"Found {len(videos)} videos for query '{query}'")
                except Exception as e:
                    logger.error(f"Error searching YouTube for query '{query}': {e}")

        unique_videos = filter_unique_videos(all_videos)
        ranked_videos = rank_videos(text, unique_videos)
        logger.info(f"Ranked Videos (first 10): {[v.title for v in ranked_videos[:10]]}")

        yield StreamResponse(status=StreamProcessStatus.YOUTUBE_SEARCH_COMPLETED, videos=ranked_videos[:10]).to_json()

        yield StreamResponse(status=StreamProcessStatus.PROCESSING_COMPLETE, keywords=keywords_data, queries=queries,
                             videos=ranked_videos[:10]).to_json()
        logger.info("Streamed all processing steps.")
    except Exception as e:
        logger.error(f"Error during stream generation: {e}")
        yield StreamResponse(status=StreamProcessStatus.ERROR,
                             message=f'An internal error occurred during processing: {str(e)}').to_json()
    finally:
        trim_log_file()


@app.route('/process', methods=['POST'])
def process():
    is_stream = request.form.get('response_as_stream', 'false').lower() == 'true'

    file_bytes_from_request: Optional[bytes] = None
    filename_from_request: Optional[str] = None

    if 'file' in request.files:
        file_storage_obj = request.files['file']
        if file_storage_obj and file_storage_obj.filename: # Assicurati che ci sia un file e un nome file
            filename_from_request = file_storage_obj.filename
            try:
                file_bytes_from_request = file_storage_obj.read()
                logger.info(f"Successfully read {len(file_bytes_from_request)} bytes from file {filename_from_request}")
            except Exception as e:
                logger.error(f"Error reading file {filename_from_request} from request: {e}", exc_info=True)
                # Se lo streaming è abilitato, il generatore gestirà l'errore se file_bytes_from_request è None.
                # Se non è streaming, restituisci un errore qui.
                if not is_stream:
                    return jsonify({'error': f'Error reading file: {str(e)}', 'filename': filename_from_request}), 500


    text_from_request = request.form.get('text', '')

    if is_stream:
        logger.info("Processing request with streaming enabled")
        return app.response_class(
            generate_process_stream(
                form_text_arg=text_from_request,
                file_bytes_arg=file_bytes_from_request,
                original_filename_arg=filename_from_request
            ),
            mimetype='application/x-ndjson')

    # Percorso non in streaming
    text_from_file_content = ""
    if file_bytes_from_request and filename_from_request:
        read_suc, text_from_file_content = read_file_from_bytes(file_bytes_from_request, filename_from_request)
        if not read_suc:
            return jsonify({'error': 'Formato file non supportato o errore nella lettura del contenuto del file',
                            'filename': filename_from_request}), 400

    # Combina testo da file e da form per il percorso non streaming
    text_parts = []
    if text_from_file_content.strip():
        text_parts.append(text_from_file_content.strip())
    if text_from_request.strip():
        text_parts.append(text_from_request.strip())

    text = "\n".join(text_parts).strip()

    if not text:
        logger.error("No text provided (file or form) for non-streaming process")
        return jsonify({'error': 'Nessun testo fornito'}), 400

    logger.info(f"Processing text: {text[:100]}\n...\n{text[-100:]}")

    detected_language = detect_language(text)

    keywords = extract_keywords(text=text, top_n=15, n_word_range=(1, 5), algorithm='yake', language=detected_language)
    logger.info(f"Extracted Keywords: {keywords}")

    queries = generate_search_queries(keywords=keywords, num_queries=MAX_QUERIES_TO_GENERATE, query_language=detected_language)
    logger.info(f"Generated Queries: {queries}")

    if not queries or len(queries) == 0:
        logger.warning(f"No queries generated from keywords, MAX_QUERIES_TO_GENERATE={MAX_QUERIES_TO_GENERATE}")

    # Cerca video
    all_videos = []
    for query in queries:
        try:
            videos = search_youtube_videos(query, video_language=detected_language)
            all_videos.extend(videos)
        except Exception as e:
            logger.error(f"Error searching YouTube for query '{query}': {e}")

    unique_videos = filter_unique_videos(all_videos)
    ranked_videos = rank_videos(text, unique_videos)
    logger.info(f"Ranked Videos (first 10): {[v.title for v in ranked_videos[:10]]}")

    response_data = {
        'keywords': [kw for kw, _ in keywords],
        'queries': queries,
        'videos': [video.__dict__ for video in ranked_videos[:10]]
    }
    response = jsonify(response_data)
    try:
        logger.info(f"Created response JSON (non-streaming): {response.get_json()}")
    except Exception as e:
        logger.error(f"Error creating and getting JSON from response: {e}")

    trim_log_file()
    return response


if __name__ == '__main__':
    prod_env = os.environ.get("PRODUCTION_ENVIROMENT", "False")  # Set to True in production
    if prod_env.lower() == "true":
        logger.info("Starting Flask app in PRODUCTION mode")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        logger.info("Starting Flask app in DEVELOPMENT mode")
        app.run(host='0.0.0.0', port=5000, debug=True)

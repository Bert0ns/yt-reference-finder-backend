import os
import logging
from typing import List
from flask import Flask, request, jsonify
from lib.query_generation import generate_search_queries
from lib.text_processing import extract_keywords
from lib.word_extraction import extract_text_from_pdf, extract_text_from_image, extract_text_from_docx, extract_text_from_doc, extract_text_from_txt, extract_text_from_md
from lib.youtube_interactions import search_youtube_videos, Video
from flask_cors import CORS

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s : %(message)s',
                    handlers=[logging.FileHandler("app.log", encoding='utf-8'),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app , origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://yt-reference-finder-frontend.vercel.app"])  # Allow requests only from http://localhost:3000

MAX_QUERIES_TO_GENERATE = 4 # Numero massimo di query da generare, che poi verranno passate a youtube per la ricerca


def rank_videos(notes_text, videos: List[Video]):
    # Ordina i video per punteggio di engagement
    ranked_videos = sorted(videos, key=lambda x: x.engagement_score, reverse=True)
    return ranked_videos


@app.route('/')
@app.route('/about', methods=['GET'])
def about():
    return jsonify({'about': 'This is a simple API to extract keywords from a text and search YouTube videos based on them.'})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'API is running'})

@app.route('/logs', methods=['GET'])
def get_api_logs():
    try:
        with open('app.log', 'r', encoding='utf-8') as f:
            logs = f.readlines()
        return jsonify({'logs': logs})
    except Exception as e:
        logger.error(f"Error reading logs: {e}")
        return jsonify({'error': 'Could not read logs'}), 500

@app.route('/process', methods=['POST'])
def process():
    text = ""
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        logger.info(f"Received file: {file.filename}")
        filename = file.filename

        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        elif filename.endswith(('.jpg', '.jpeg', '.png')):
            text = extract_text_from_image(file)
        elif filename.endswith('.txt'):
            text = extract_text_from_txt(file)
        elif filename.endswith('.md'):
            text = extract_text_from_md(file)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(file)
        elif filename.endswith('.doc'):
            text = extract_text_from_doc(file)
        else:
            logger.warning(f"Unsupported file format: {filename}")
            return jsonify({'error': 'Formato file non supportato'})

    text = "\n".join([text, request.form.get('text', '')])  # Unisce il testo del file con il testo inviato nel form, se presente

    if not text or text.strip() == '':
        logger.error("No text provided")
        return jsonify({'error': 'Nessun testo fornito'})

    logger.info(f"Processing text: {text[:100]}\n...\n{text[-100:]}")  # Logga solo una parte del testo per brevità

    # Analizza il testo
    keywords = extract_keywords(text=text, top_n=10, n_word_range=(1, 6))
    logger.info(f"Extracted Keywords: {keywords}")

    queries = generate_search_queries(keywords=keywords, num_queries=MAX_QUERIES_TO_GENERATE)
    logger.info(f"Generated Queries: {queries}")

    # Cerca video
    all_videos = []
    for query in queries:
        try:
            videos = search_youtube_videos(query)
            all_videos.extend(videos)
        except Exception as e:
            logger.error(f"Error searching YouTube for query '{query}': {e}")

    # Elimina duplicati (basati su video_id)
    unique_videos = []
    seen_ids = set()
    for video in all_videos:
        if video.video_id not in seen_ids:
            unique_videos.append(video)
            seen_ids.add(video.video_id)

    # Classifica i video
    ranked_videos = rank_videos(text, unique_videos)

    logger.info(f"Ranked Videos (first 10): {[v.title for v in ranked_videos[:10]]}")

    response_data = {
        'keywords': [kw for kw, _ in keywords],
        'queries': queries,
        'videos': [video.__dict__ for video in ranked_videos[:10]]
    }
    response = jsonify(response_data)
    try:
        logger.info(f"Created response JSON: {response.get_json()}")
    except Exception as e:
        logger.error(f"Error creating and getting JSON from response: {e}")

    return response


if __name__ == '__main__':
    prod_env = os.environ.get("PRODUCTION_ENVIROMENT", "False")  # Set to True in production
    if prod_env.lower() == "true":
        logger.info("Starting Flask app in PRODUCTION mode")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        logger.info("Starting Flask app in DEVELOPMENT mode")
        app.run(host='0.0.0.0', port=5000, debug=True)

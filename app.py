import os
from typing import List
from flask import Flask, request, jsonify
from lib.query_generation import generate_search_queries
from lib.text_processing import extract_keywords
from lib.word_extraction import extract_text_from_pdf, extract_text_from_image
from lib.youtube_interactions import search_youtube_videos, Video
from flask_cors import CORS
app = Flask(__name__)
CORS(app , origins=["http://localhost:3000", "http://127.0.0.1:3000"])  # Allow requests only from http://localhost:3000

def rank_videos(notes_text, videos: List[Video]):
    # Ordina i video per punteggio di engagement
    ranked_videos = sorted(videos, key=lambda x: x.engagement_score, reverse=True)
    return ranked_videos


@app.route('/')
@app.route('/about')
def about():
    return jsonify({'about': 'This is a simple API to extract keywords from a text and search YouTube videos based on them.'})


@app.route('/process', methods=['POST'])
def process():
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        print("file submitted:", file)
        filename = file.filename

        # Estrai il testo dal file
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        elif filename.endswith(('.jpg', '.jpeg', '.png')):
            text = extract_text_from_image(file)
        else:
            return jsonify({'error': 'Formato file non supportato'})
    else:
        text = request.form.get('text', '')
    if not text:
        return jsonify({'error': 'Nessun testo fornito'})

    print("Text:", text)
    print("------------------------------------------------------------------------------------")

    # Analizza il testo
    keywords = extract_keywords(text=text, top_n=10, n_word_range=(1, 6))
    print("Extracted Keywords:", keywords)
    print("------------------------------------------------------------------------------------")

    queries = generate_search_queries(keywords=keywords, num_queries=5)
    print("Generated Queries:", queries)
    print("------------------------------------------------------------------------------------")

    # Cerca video
    all_videos = []
    for query in queries:
        videos = search_youtube_videos(query)
        all_videos.extend(videos)

    # Elimina duplicati (basati su video_id)
    unique_videos = []
    seen_ids = set()
    for video in all_videos:
        if video.video_id not in seen_ids:
            unique_videos.append(video)
            seen_ids.add(video.video_id)

    # Classifica i video
    ranked_videos = rank_videos(text, unique_videos)

    print("-------------------------------------------------------------------------------------")
    print("Ranked Videos:", ranked_videos)

    response = jsonify({
        'keywords': [kw for kw, _ in keywords],
        'queries': queries,
        'videos': ranked_videos[:10]  # Limita a 10 risultati
    })

    print("-------------------------------------------------------------------------------------")
    print(str(response.json))

    return response


if __name__ == '__main__':
    prod_env = os.environ.get("PRODUCTION_ENVIROMENT", "False")  # Set to True in production
    if prod_env.lower() == "true":
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        app.run(debug=False, port=5000, host='0.0.0.0')

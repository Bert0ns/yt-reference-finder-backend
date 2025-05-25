from typing import List
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from lib.query_generation import generate_search_queries
from lib.text_processing import extract_keywords
from lib.word_extraction import extract_text_from_pdf, extract_text_from_image
from lib.youtube_interactions import search_youtube_videos, Video
from flask_cors import CORS
app = Flask(__name__)
CORS(app , origins=["http://localhost:3000", "http://127.0.0.1:3000"])  # Allow requests only from http://localhost:3000
# Modelli NLP
similarity_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def rank_videos(notes_text, videos: List[Video]):
    # Genera embedding per gli appunti
    notes_embedding = similarity_model.encode([notes_text])[0]

    # Calcola similarità per ogni video
    for video in videos:
        video_text = video.title + " " + video.description
        video_embedding = similarity_model.encode([video_text])[0]
        similarity = cosine_similarity([notes_embedding], [video_embedding])[0][0]
        video.relevance_score = float(similarity)

    # Ordina i video per punteggio di rilevanza
    ranked_videos = sorted(videos, key=lambda x: x.relevance_score, reverse=True)
    return ranked_videos


@app.route('/')
def home():
    return render_template('index.html')

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
    queries = generate_search_queries(keywords=keywords, num_queries=5)
    print("Extracted Keywords:", keywords)
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
    app.run(host='0.0.0.0', debug=False)
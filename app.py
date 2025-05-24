from flask import Flask, request, jsonify, render_template
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from lib.word_extraction import extract_text_from_pdf, extract_text_from_image
from lib.youtube_interactions import search_youtube_videos
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Allow requests only from http://localhost:3000

# Modelli NLP
keyword_model = KeyBERT()
similarity_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def extract_keywords(text, top_n=5, n_word_range=(3, 8)):
    keywords = keyword_model.extract_keywords(
        text,
        keyphrase_ngram_range=n_word_range,
        top_n=top_n
    )
    return keywords


def generate_search_queries(keywords, text_sample=" ", num_queries=3):
    # Versione semplificata per il prototipo
    queries = []
    for keyword, _ in keywords[:num_queries]:
        queries.append(f"{keyword}")
    return queries


def rank_videos(notes_text, videos):
    # Genera embedding per gli appunti
    notes_embedding = similarity_model.encode([notes_text])[0]

    # Calcola similarità per ogni video
    for video in videos:
        video_text = video['title'] + " " + video['description']
        video_embedding = similarity_model.encode([video_text])[0]
        similarity = cosine_similarity([notes_embedding], [video_embedding])[0][0]
        video['relevance_score'] = float(similarity)

    # Ordina i video per punteggio di rilevanza
    ranked_videos = sorted(videos, key=lambda x: x['relevance_score'], reverse=True)

    return ranked_videos


@app.route('/')
def home():
    return render_template('index.html')


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
    keywords = extract_keywords(text=text, top_n=10, n_word_range=(1, 4))
    queries = generate_search_queries(keywords=keywords, text_sample=text, num_queries=3)
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
        if video['video_id'] not in seen_ids:
            unique_videos.append(video)
            seen_ids.add(video['video_id'])

    # Classifica i video
    ranked_videos = rank_videos(text, unique_videos)

    print("-------------------------------------------------------------------------------------")
    print("Ranked Videos:", ranked_videos)

    return jsonify({
        'keywords': [kw for kw, _ in keywords],
        'queries': queries,
        'videos': ranked_videos[:10]  # Limita a 10 risultati
    })


if __name__ == '__main__':
    app.run(debug=True)
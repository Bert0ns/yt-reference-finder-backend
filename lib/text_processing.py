import re
from keybert import KeyBERT
from sklearn.feature_extraction.text import CountVectorizer

# Aggiungi altre stopwords specifiche al contesto
italian_stopwords = set()
compound_stopwords = ['cioè', 'ad esempio', 'inoltre', 'quindi', 'però', 'perché']
italian_stopwords.update(compound_stopwords)
# Aggiungi anche i token singoli delle frasi composte
for compound in compound_stopwords:
    italian_stopwords.update(compound.split())

kw_model = KeyBERT(model="paraphrase-albert-small-v2")

def preprocess_text(text):
    # Rimuovi caratteri speciali e numeri
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)

    text = text.lower()
    # Rimuovi spazi multipli
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_keywords(text, top_n=10, n_word_range=(1, 4)):
    # Pre-elabora il testo
    clean_text = preprocess_text(text)
    # Lista delle stopwords per garantire consistenza
    stopwords_list = list(italian_stopwords)

    # Configura il vectorizer personalizzato con stopwords italiane
    vectorizer = CountVectorizer(
        stop_words=stopwords_list,
        lowercase=True,
        ngram_range=n_word_range,
    )

    # Estrai parole chiave con diversità (MMR)
    keywords_mmr = kw_model.extract_keywords(
        clean_text,
        use_mmr=True,
        diversity=0.7,
        top_n=top_n,
        vectorizer=vectorizer
    )

    # Estrai parole chiave con MaxSum
    keywords_max_sum = kw_model.extract_keywords(
        clean_text,
        use_maxsum=True,
        nr_candidates=20,
        top_n=top_n,
        vectorizer=vectorizer
    )

    # Resto del codice invariato
    combined_keywords = []
    seen = set()
    for keyword_list in [keywords_mmr, keywords_max_sum]:
        for keyword, score in keyword_list:
            if keyword not in seen:
                combined_keywords.append((keyword, score))
                seen.add(keyword)

    # Ordina per punteggio e prendi i migliori
    sorted_keywords = sorted(combined_keywords, key=lambda x: x[1], reverse=True)
    return sorted_keywords[:top_n]
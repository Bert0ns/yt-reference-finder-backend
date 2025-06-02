import re
import nltk
from rake_nltk import Rake

nltk.download('punkt_tab')
nltk.download('stopwords')

italian_stopwords = set()
compound_stopwords = ['cioè', 'ad esempio', 'inoltre', 'quindi', 'però', 'perché']
italian_stopwords.update(compound_stopwords)
# Aggiungi anche i token singoli delle frasi composte
for compound in compound_stopwords:
    italian_stopwords.update(compound.split())


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
    # stopwords_list = list(italian_stopwords)

    keywords = extract_keywords_rake(clean_text, top_n=top_n, n_word_range=n_word_range)

    # Resto del codice invariato
    combined_keywords = []
    seen = set()
    for keyword, score in keywords:
        if keyword not in seen:
            combined_keywords.append((keyword, score))
            seen.add(keyword)

    # Ordina per punteggio e prendi i migliori
    sorted_keywords = sorted(combined_keywords, key=lambda x: x[1], reverse=True)
    return sorted_keywords[:top_n]


def extract_keywords_rake(text, top_n=10, n_word_range=(1, 4), language='italian'):
    from lib.app_logger import logger

    try:
        # Inizializza RAKE
        r = Rake(language=language, min_length=n_word_range[0], max_length=n_word_range[1])

        # Per usare stopwords personalizzate, modifica manualmente
        r.stopwords = set(nltk.corpus.stopwords.words(language)).union(italian_stopwords)

        r.extract_keywords_from_text(text)
        ranked_phrases_with_scores = r.get_ranked_phrases_with_scores()

        if not ranked_phrases_with_scores:
            logger.warning("Nessuna parola chiave estratta dal testo")
            return []

        # Converti il formato e filtra parole chiave troppo brevi o con punteggio basso
        keywords = [(phrase, score) for score, phrase in ranked_phrases_with_scores]
        keywords.sort(key=lambda x: x[1], reverse=True)

        return keywords[:top_n]
    except Exception as e:
        logger.error(f"Errore nell'estrazione delle parole chiave: {e}")
        return []
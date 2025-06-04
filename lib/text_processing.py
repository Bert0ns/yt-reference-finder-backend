import re
import nltk
from rake_nltk import Rake
from yake import KeywordExtractor
from langdetect import detect
from lib.app_logger import logger

nltk.download('punkt_tab')
nltk.download('stopwords')
nltk_stopwords_languages = {
    'ar': 'arabic',
    'az': 'azerbaijani',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'german',
    'el': 'greek',
    'hu': 'hungarian',
    'id': 'indonesian',
    'it': 'italian',
    'kk': 'kazakh',
    'ne': 'nepali',
    'no': 'norwegian',
    'pt': 'portuguese',
    'ro': 'romanian',
    'ru': 'russian',
    'sl': 'slovene',
    'es': 'spanish',
    'sv': 'swedish',
    'tg': 'tajik',
    'tr': 'turkish'
}


def preprocess_text(text):
    # Rimuovi caratteri speciali e numeri
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)

    text = text.lower()
    # Rimuovi spazi multipli
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_keywords_rake(text, top_n=10, n_word_range=(1, 4), language='italian', stopwords_set=None):
    try:
        r = Rake(language=language, min_length=n_word_range[0], max_length=n_word_range[1], stopwords=stopwords_set)
        r.extract_keywords_from_text(text)
        ranked_phrases_with_scores = r.get_ranked_phrases_with_scores()

        # format
        keywords = [(phrase, score) for score, phrase in ranked_phrases_with_scores]
        keywords.sort(key=lambda x: x[1], reverse=True)
        return keywords[:top_n]
    except Exception as e:
        logger.error(f"Error extracting keywords: {e}")
        return []


def extract_keywords_yake(text, top_n=10, max_ngram_size=4, language='it', stopword_set=None):
    if stopword_set is None:
        stopword_set = {}
    try:
        extractor = KeywordExtractor(lan=language, n=max_ngram_size, top=top_n, stopwords=stopword_set)
        keywords = extractor.extract_keywords(text)
        return keywords[:top_n]
    except Exception as e:
        logger.error(f"Error extracting keywords: {e}")
        return []

def detect_language(text):
    """Detect the language of the given text."""
    try:
        lang = detect(text)
        logger.info(f"Detected language: {lang}")
        return lang
    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        return 'en'

def extract_keywords(text, top_n=10, n_word_range=(1, 4), algorithm='rake', language=None):
    if language is None:
        detected_lang = detect_language(text)
    else:
        detected_lang = language

    try:
        nltk_stopwords = nltk.corpus.stopwords.words(nltk_stopwords_languages.get(detected_lang))
        stopwords_set = set(nltk_stopwords)
    except Exception as e:
        logger.error(f"Did not find stopword set for language {detected_lang} : {e}")
        stopwords_set = None


    if algorithm == 'rake':
        keywords = extract_keywords_rake(text, top_n=top_n, n_word_range=n_word_range, language=detected_lang, stopwords_set=stopwords_set)
    elif algorithm == 'yake':
        keywords = extract_keywords_yake(text, top_n=top_n, max_ngram_size=n_word_range[1], language=detected_lang, stopword_set=stopwords_set)
    else:
        logger.error(f"Keyword extraction algorithm unknown: {algorithm}")
        return []

    return keywords[:top_n]
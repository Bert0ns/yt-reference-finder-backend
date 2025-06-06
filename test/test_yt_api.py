import json
from googleapiclient.discovery import build

def _get_all_youtube_topic() -> dict[str, str]:
    """
    Carica i topic di YouTube da un file JSON e restituisce un dizionario

    ref: https://gist.github.com/stpe/2951130dfc8f1d0d1a2ad736bef3b703
    """
    try:
        with open('static/youtube_topics.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}
    return {i['topic']: i['id'] for i in data}

def _get_all_youtube_categories() -> dict[str, str]:
    """
    Carica le categorie di YouTube da un file JSON e restituisce un dizionario

    ref: https://gist.github.com/stpe/2951130dfc8f1d0d1a2ad736bef3b703
    """
    try:
        with open('static/youtube_categories.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}
    return data

def _initialize_youtube_api():
    """Inizializza e restituisce l'oggetto API di YouTube"""
    youtube_api_key = ' '  # Replace with your actual API key or use os.environ.get('YOUTUBE_API_KEY')

    if not youtube_api_key:
        raise ValueError("YOUTUBE_API_KEY non è impostata")

    return build('youtube', 'v3', developerKey=youtube_api_key)

if __name__ == "__main__":
    youtube_topics = _get_all_youtube_topic()
    youtube_categories = _get_all_youtube_categories()

    youtube = _initialize_youtube_api()
    topicId = youtube_topics.get('Knowledge', '')

    print("Topic id for 'Knowledge':", topicId)

    yt_request = youtube.search().list(
        q="What is a CPU",
        part='snippet',
        type='video',
        maxResults=50,
        relevanceLanguage='it',
        order='relevance',
        videoDimension='2d',
        videoDuration='any',
        videoCaption='closedCaption',
        videoCategoryId='27',
        videoDefinition='high',
        safeSearch='none',
        topicId=topicId,
    )
    response = yt_request.execute()

    print("Search response:", response)

    with open('yt_search_response.json', 'w') as f:
        json.dump(response, f, indent=2)
import os
import json
from typing import List
from googleapiclient.discovery import build, Resource
from lib.app_logger import logger
from lib.types.youtube_types import ChannelInfo, VideoStatistics, Video, YouTubeSearchListResponse, SearchResource


def get_all_youtube_topic() -> dict[str, str]:
    """
    Carica i topic di YouTube da un file JSON e restituisce un dizionario

    ref: https://gist.github.com/stpe/2951130dfc8f1d0d1a2ad736bef3b703
    """
    try:
        with open('static/youtube_topics.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error('File youtube_topics.json not found. Please ensure it exists in the static directory.')
        return {}
    logger.info('YouTube topics loaded successfully.')
    return {i['topic']: i['id'] for i in data}


def get_all_youtube_categories() -> dict[str, str]:
    """
    Carica le categorie di YouTube da un file JSON e restituisce un dizionario

    ref: https://gist.github.com/stpe/2951130dfc8f1d0d1a2ad736bef3b703
    """
    try:
        with open('static/youtube_categories.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error('File youtube_categories.json not found. Please ensure it exists in the static directory.')
        return {}
    logger.info('YouTube categories loaded successfully.')
    return data


youtube_topics = get_all_youtube_topic()
youtube_categories = get_all_youtube_categories()


def initialize_youtube_api() -> Resource:
    """Inizializza e restituisce l'oggetto API di YouTube"""
    youtube_api_key = os.environ.get('YOUTUBE_API_KEY')

    if not youtube_api_key:
        raise ValueError("YOUTUBE_API_KEY non è impostata")

    return build('youtube', 'v3', developerKey=youtube_api_key)


def search_videos(youtube: Resource, query, max_results=10, language='it', youtube_topic_key='Knowledge') -> YouTubeSearchListResponse:
    """
    Esegue la ricerca dei video su YouTube e restituisce i risultati grezzi

    docs: https://developers.google.com/youtube/v3/docs/search/list
    """

    yt_request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results,
        relevanceLanguage=language,
        order='relevance',
        videoDimension='2d',
        videoDuration='any',
        videoCaption='closedCaption',
        videoCategoryId='27',
        videoDefinition='high',
        safeSearch='none',
        topicId=youtube_topics.get(youtube_topic_key, youtube_topics.get('Knowledge', '')),
    )

    data: dict = yt_request.execute()
    return YouTubeSearchListResponse.from_dict(data)


def process_search_results(response_items : List[SearchResource]):
    """Estrae informazioni dai risultati di ricerca e restituisce video temporanei e IDs"""
    temp_videos = []
    channel_ids = set()
    video_ids = []

    for item in response_items:
        channel_id = item.snippet.channelId
        video_id = item.id.videoId
        channel_ids.add(channel_id)
        video_ids.append(video_id)
        temp_videos.append({
            'title': item.snippet.title,
            'description': item.snippet.description,
            'thumbnail': item.snippet.thumbnails.high.url,
            'video_id': video_id,
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'channel_id': channel_id
        })

    return temp_videos, channel_ids, video_ids


def get_channel_info_batch(youtube: Resource, channel_ids):
    """Recupera informazioni sui canali in batch"""
    channels_data = {}

    if not channel_ids:
        return channels_data

    channels_request = youtube.channels().list(
        part='statistics,snippet',
        id=','.join(channel_ids)
    )
    channels_response = channels_request.execute()

    for channel in channels_response.get('items', []):
        channel_id = channel['id']
        subscriber_count = int(channel['statistics'].get('subscriberCount', 0))
        language = channel['snippet'].get('defaultLanguage', '')

        channels_data[channel_id] = ChannelInfo(
            subscriber_count=subscriber_count,
            language=language
        )

    return channels_data


def get_video_statistics_batch(youtube: Resource, video_ids):
    """Recupera statistiche dei video in batch"""
    videos_statistics = {}

    if not video_ids:
        return videos_statistics

    video_stats_request = youtube.videos().list(
        part='statistics',
        id=','.join(video_ids)
    )
    video_stats_response = video_stats_request.execute()

    for video_stat in video_stats_response.get('items', []):
        video_id = video_stat['id']
        like_count = int(video_stat['statistics'].get('likeCount', 0))
        view_count = int(video_stat['statistics'].get('viewCount', 0))
        videos_statistics[video_id] = VideoStatistics(
            like_count=like_count,
            view_count=view_count
        )

    return videos_statistics


def calculate_engagement_score(view_count, like_count):
    """Calcola il punteggio di engagement di un video"""
    if view_count > 0:
        return like_count / view_count
    return 0.0


def filter_and_create_videos(temp_videos, channels_data, videos_statistics, min_subscribers, min_likes):
    """Filtra i video in base ai criteri e crea oggetti Video"""
    filtered_videos = []

    for video_dict in temp_videos:
        channel_info = channels_data.get(video_dict['channel_id'], ChannelInfo())
        video_stats = videos_statistics.get(video_dict['video_id'], VideoStatistics())

        engagement_score = calculate_engagement_score(video_stats.view_count, video_stats.like_count)

        # Verifica criteri di filtro
        if (channel_info.subscriber_count >= min_subscribers and
                (not channel_info.language or channel_info.language in ['it', 'en']) and
                video_stats.like_count >= min_likes):
            video = Video(
                title=video_dict['title'],
                description=video_dict['description'],
                thumbnail=video_dict['thumbnail'],
                video_id=video_dict['video_id'],
                url=video_dict['url'],
                channel_id=video_dict['channel_id'],
                channel_subscribers=channel_info.subscriber_count,
                like_count=video_stats.like_count,
                view_count=video_stats.view_count,
                engagement_score=round(engagement_score, 10)
            )
            filtered_videos.append(video)

    return filtered_videos


def normalize_engagement_scores(videos):
    """Normalizza i punteggi di engagement su scala 0-1"""
    if not videos:
        return videos

    max_engagement = max(video.engagement_score for video in videos)
    if max_engagement > 0:
        for video in videos:
            video.engagement_score = round(video.engagement_score / max_engagement, 5)

    return videos


def search_youtube_videos(query, video_language='it', max_results=50, min_subscribers=30000, min_likes=1000, verbose=False):
    """Funzione principale per la ricerca di video su YouTube con filtri"""
    if verbose:
        logger.info(f"Inizializzazione API YouTube con query: {query}, video_language: {video_language}, max_results: {max_results}, min_subscribers: {min_subscribers}, min_likes: {min_likes}, verbose: {verbose}")

    youtube = initialize_youtube_api()
    if verbose:
        logger.info(f"API YouTube: {youtube}")

    # Ricerca video
    search_response = search_videos(youtube, query, max_results, video_language)
    if verbose:
        logger.info(f"search_response: {search_response}")
        try:
            search_dict = search_response.to_dict()
            with open('search_response.json', 'w') as f:
                json.dump(search_dict, f, ensure_ascii=False, indent=2)
        except (TypeError, AttributeError) as e:
            logger.error(f"Impossibile serializzare search_response in JSON: {e}")

    # Processa i risultati della ricerca
    temp_videos, channel_ids, video_ids = process_search_results(search_response.items)

    # Ottieni informazioni su canali e statistiche video
    channels_data = get_channel_info_batch(youtube, channel_ids)
    videos_statistics = get_video_statistics_batch(youtube, video_ids)

    # Filtra e crea oggetti video
    filtered_videos = filter_and_create_videos(
        temp_videos, channels_data, videos_statistics, min_subscribers, min_likes
    )

    # Normalizza i punteggi
    filtered_videos = normalize_engagement_scores(filtered_videos)

    return filtered_videos


if __name__ == "__main__":
    """
    per testare dalla root del progetto:
    
    python -m lib.youtube_interactions
    """
    # Aggiungi il percorso della directory principale al sys.path quando esegui direttamente
    import sys
    import os.path

    # Ottieni il percorso della directory principale del progetto
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    # Configura l'API key di YouTube per i test
    if not os.environ.get('YOUTUBE_API_KEY'):
        api_key = input("Inserisci la tua YOUTUBE_API_KEY: ")
        os.environ['YOUTUBE_API_KEY'] = api_key

    # Esempio di utilizzo della funzione di ricerca
    test_query = input("Inserisci la query di ricerca (default: 'Python programming'): ") or "Python programming"
    print(f"Ricerca in corso per: {test_query}...")

    try:
        results = search_youtube_videos(test_query, verbose=True, max_results=2)
        print(f"\nTrovati {len(results)} video che soddisfano i criteri.")
        for i, video in enumerate(results[:5], 1):  # Mostra solo i primi 5 risultati
            print(f"\n{i}. {video.title}")
            print(f"   Engagement Score: {video.engagement_score}")
            print(f"   Views: {video.view_count}, Likes: {video.like_count}")
            print(f"   URL: {video.url}")
    except Exception as e:
        print(f"Errore durante la ricerca: {e}")
        import traceback
        traceback.print_exc()

from dataclasses import dataclass
import os
from flask import jsonify
from googleapiclient.discovery import build


@dataclass
class VideoStatistics:
    like_count: int = 0
    view_count: int = 0

@dataclass
class ChannelInfo:
    subscriber_count: int = 0
    language: str = ""

@dataclass
class Video:
    title: str
    description: str
    thumbnail: str
    video_id: str
    url: str
    channel_id: str
    channel_subscribers: int = 0
    like_count: int = 0
    view_count: int = 0
    engagement_score: float = 0.0
    relevance_score: float = 0.0


def initialize_youtube_api():
    """Inizializza e restituisce l'oggetto API di YouTube"""
    youtube_api_key = os.environ.get('YOUTUBE_API_KEY')

    if not youtube_api_key:
        raise ValueError("YOUTUBE_API_KEY non è impostata")

    return build('youtube', 'v3', developerKey=youtube_api_key)

def search_videos(youtube, query, max_results, language='it'):
    """Esegue la ricerca dei video su YouTube e restituisce i risultati grezzi"""
    yt_request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results,
        relevanceLanguage=language,
        order='relevance',
        videoDimension='2d',
        videoCaption='closedCaption',
        videoCategoryId='27',
        videoDefinition='high'
    )

    return yt_request.execute()

def process_search_results(response_items):
    """Estrae informazioni dai risultati di ricerca e restituisce video temporanei e IDs"""
    temp_videos = []
    channel_ids = set()
    video_ids = []

    for item in response_items:
        channel_id = item['snippet']['channelId']
        video_id = item['id']['videoId']
        channel_ids.add(channel_id)
        video_ids.append(video_id)
        temp_videos.append({
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'thumbnail': item['snippet']['thumbnails']['high']['url'],
            'video_id': video_id,
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'channel_id': channel_id
        })

    return temp_videos, channel_ids, video_ids

def get_channel_info_batch(youtube, channel_ids):
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

def get_video_statistics_batch(youtube, video_ids):
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

def log_response(query, filtered_videos):
    """Registra la risposta in un file di log"""
    with open('youtube_responses.log', 'a', encoding="utf-8") as log_file:
        log_file.write("----------------------------------\n")
        log_file.write(f"Query: {query}\n")
        log_file.write(f"Processed Response: \n")
        log_file.write(str(jsonify(filtered_videos).json))

def search_youtube_videos(query, video_language='it', max_results=50, min_subscribers=30000, min_likes=1000):
    """Funzione principale per la ricerca di video su YouTube con filtri"""
    youtube = initialize_youtube_api()

    # Ricerca video
    search_response = search_videos(youtube, query, max_results, video_language)

    # Processa i risultati della ricerca
    temp_videos, channel_ids, video_ids = process_search_results(search_response['items'])

    # Ottieni informazioni su canali e statistiche video
    channels_data = get_channel_info_batch(youtube, channel_ids)
    videos_statistics = get_video_statistics_batch(youtube, video_ids)

    # Filtra e crea oggetti video
    filtered_videos = filter_and_create_videos(
        temp_videos, channels_data, videos_statistics, min_subscribers, min_likes
    )

    # Normalizza i punteggi
    filtered_videos = normalize_engagement_scores(filtered_videos)

    # Registra la risposta
    log_response(query, filtered_videos)

    return filtered_videos
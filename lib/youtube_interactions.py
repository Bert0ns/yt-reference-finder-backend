from dataclasses import dataclass
from typing import List, Set, Dict
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

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

def search_youtube_videos(query, max_results=50, min_subscribers=30000, min_likes=1000):
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY non è impostata")

    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    yt_request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results,
        relevanceLanguage='it',
        order='relevance',
        videoDimension='2d',
        videoCaption='closedCaption',
        videoCategoryId='27'
    )

    response = yt_request.execute()

    # Lista temporanea per raccogliere i video e i loro canali
    temp_videos = []
    channel_ids: Set[str] = set()
    video_ids: List[str] = []

    for item in response['items']:
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

    # Ottieni informazioni sui canali in batch
    channels_data: Dict[str, ChannelInfo] = {}
    if channel_ids:
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

    # Ottieni statistiche dei video in batch
    videos_statistics: Dict[str, VideoStatistics] = {}
    if video_ids:
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

    # Filtra i video in base ai criteri
    filtered_videos: List[Video] = []
    for video_dict in temp_videos:
        channel_info = channels_data.get(video_dict['channel_id'], ChannelInfo())
        video_stats = videos_statistics.get(video_dict['video_id'], VideoStatistics())

        # Calcola un punteggio di engagement
        engagement_score = 0.0
        if video_stats.view_count > 0:
            engagement_score = (video_stats.like_count / video_stats.view_count)

        # Verifica tutti i criteri di filtro
        if (channel_info.subscriber_count >= min_subscribers and
            (not channel_info.language or channel_info.language in ['it', 'en']) and
            video_stats.like_count >= min_likes):

            # Crea un oggetto Video invece di un dizionario
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

    # Normalize engagement scores to a scale of 0-1
    if filtered_videos:
        max_engagement = max(video.engagement_score for video in filtered_videos)
        for video in filtered_videos:
            video.engagement_score = round(video.engagement_score / max_engagement, 5)

    # Crea un file di log per la risposta
    with open('youtube_responses.log', 'a', encoding="utf-8") as log_file:
        log_file.write("----------------------------------\n")
        log_file.write(f"Query: {query}\n")
        log_file.write(f"Processed Response: \n")
        log_file.write(str(jsonify(filtered_videos).json))

    return filtered_videos
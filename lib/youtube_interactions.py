import json
import os
from typing import List
from googleapiclient.discovery import build, Resource
from lib.app_logger import logger
from lib.types.youtube_types import YouTubeSearchListResponse, SearchResource, YouTubeChannelListResponse, \
    YouTubeVideoListResponse
from lib.types.youtube_types_custom import ChannelInfo, VideoStatistics, Video, VideoPartialData


def get_all_youtube_topic() -> dict[str, str]:
    """
    Load YouTube topics from a JSON file and return a dictionary.

    ref: https://gist.github.com/stpe/2951130dfc8f1d0d1a2ad736bef3b703
    """
    try:
        with open('static/youtube_topics.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error('File youtube_topics.json not found. Please ensure it exists in the static directory.')
        return {}
    logger.info('YouTube topics loaded successfully.')
    return {item['topic']: item['id'] for item in data}


def get_all_youtube_categories() -> dict[str, str]:
    """
    Load YouTube categories from a JSON file and return a dictionary.

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
    """Initialize and return the YouTube API object."""
    youtube_api_key = os.environ.get('YOUTUBE_API_KEY')

    if not youtube_api_key:
        raise ValueError("YOUTUBE_API_KEY is not set")

    return build('youtube', 'v3', developerKey=youtube_api_key)


def search_videos(youtube: Resource, query: str, max_results=10, language='it',
                  youtube_topic_key='Knowledge') -> YouTubeSearchListResponse:
    """
    Run a YouTube video search and return raw results.

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
        topicId=youtube_topics.get(youtube_topic_key, youtube_topics.get('Society', '')),
    )

    data: dict = yt_request.execute()
    return YouTubeSearchListResponse.from_dict(data)


def process_search_results(search_resources: List[SearchResource]) -> tuple[List[VideoPartialData], set[str], set[str]]:
    """Extract info from search results and return temporary videos and IDs."""
    temp_videos: List[VideoPartialData] = []
    channel_ids = set()
    video_ids = set()

    for item in search_resources:
        channel_id = item.snippet.channelId
        video_id = item.id.videoId
        channel_ids.add(channel_id)
        video_ids.add(video_id)

        video_partial_data = VideoPartialData(title=item.snippet.title,
                                              description=item.snippet.description,
                                              video_id=video_id,
                                              url=f"https://www.youtube.com/watch?v={video_id}",
                                              channel_id=channel_id,
                                              thumbnails=item.snippet.thumbnails)

        temp_videos.append(video_partial_data)

    return temp_videos, channel_ids, video_ids


def get_channel_info_batch(youtube: Resource, channel_ids: set[str]) -> dict[str, ChannelInfo]:
    """Fetch channel information in batch."""
    channels_data = {}

    if not channel_ids:
        return channels_data

    channels_request = youtube.channels().list(
        part='statistics,snippet',
        id=','.join(channel_ids)
    )
    channels_response_data = channels_request.execute()
    channels_response = YouTubeChannelListResponse.from_dict(channels_response_data)

    for channel in channels_response.items:
        channel_id = channel.id
        subscriber_count = int(channel.statistics.subscriberCount)
        language = channel.snippet.defaultLanguage

        channels_data[channel_id] = ChannelInfo(
            subscriber_count=subscriber_count,
            language=language
        )

    return channels_data


def get_video_statistics_batch(youtube: Resource, video_ids: set[str]) -> dict[str, VideoStatistics]:
    """Fetch video statistics in batch."""
    videos_statistics = {}

    if not video_ids:
        return videos_statistics

    video_stats_request = youtube.videos().list(
        part='statistics',
        id=','.join(video_ids)
    )
    video_stats_response_data = video_stats_request.execute()
    video_stats_response = YouTubeVideoListResponse.from_dict(video_stats_response_data)

    for video_stat in video_stats_response.items:
        video_id = video_stat.id
        like_count = int(video_stat.statistics.likeCount)
        view_count = int(video_stat.statistics.viewCount)
        videos_statistics[video_id] = VideoStatistics(
            like_count=like_count,
            view_count=view_count
        )

    return videos_statistics


def calculate_engagement_score(view_count, like_count):
    """Calculate a video's engagement score."""
    if view_count > 0:
        return like_count / view_count
    return 0.0


def filter_and_create_videos(temp_videos: List[VideoPartialData], channels_data, videos_statistics, min_subscribers, min_likes, language_set: set[str]) -> List[Video]:
    """Filter videos by criteria and create Video objects."""
    filtered_videos: List[Video] = []

    for v_partial_data in temp_videos:
        channel_info = channels_data.get(v_partial_data.channel_id, ChannelInfo())
        video_stats = videos_statistics.get(v_partial_data.video_id, VideoStatistics())

        engagement_score = calculate_engagement_score(video_stats.view_count, video_stats.like_count)

        # Check filter criteria
        include = channel_info.subscriber_count >= min_subscribers and (not channel_info.language or channel_info.language in language_set) and video_stats.like_count >= min_likes
        if include:
            video_complete_data = Video(
                title=v_partial_data.title,
                description=v_partial_data.description,
                video_id=v_partial_data.video_id,
                url=v_partial_data.url,
                channel_id=v_partial_data.channel_id,
                thumbnails=v_partial_data.thumbnails,
                channel_subscribers=channel_info.subscriber_count,
                like_count=video_stats.like_count,
                view_count=video_stats.view_count,
                engagement_score=round(engagement_score, 10)
            )
            filtered_videos.append(video_complete_data)

    return filtered_videos


def normalize_engagement_scores(videos):
    """Normalize engagement scores to a 0-1 scale."""
    if not videos:
        return videos

    max_engagement = max(v.engagement_score for v in videos)
    if max_engagement > 0:
        for v in videos:
            v.engagement_score = round(v.engagement_score / max_engagement, 5)

    return videos


def search_youtube_videos(query, video_language='it', max_results=50, min_subscribers=30000, min_likes=1000,
                          verbose=False):
    """Main function to search YouTube videos with filters."""
    if verbose:
        logger.info(
            f"Initializing YouTube API with query: {query}, video_language: {video_language}, max_results: {max_results}, min_subscribers: {min_subscribers}, min_likes: {min_likes}, verbose: {verbose}")

    youtube = initialize_youtube_api()
    if verbose:
        logger.info(f"API YouTube: {youtube}")

    # Search videos
    search_response: YouTubeSearchListResponse = search_videos(youtube, query, max_results, video_language)
    if verbose:
        logger.info(f"search_response: {search_response}")
        try:
            search_dict = search_response.to_dict()
            with open('search_response.json', 'w') as f:
                json.dump(search_dict, f, ensure_ascii=False, indent=2)
        except (TypeError, AttributeError) as error:
            logger.error(f"Unable to serialize search_response to JSON: {error}")


    # Process search results
    temp_videos, channel_ids, video_ids = process_search_results(search_response.items)

    # Fetch channel info and video stats
    channels_data = get_channel_info_batch(youtube, channel_ids)
    videos_statistics = get_video_statistics_batch(youtube, video_ids)

    # Filter and create video objects
    filtered_videos = filter_and_create_videos(temp_videos, channels_data, videos_statistics, min_subscribers,
                                               min_likes, language_set={video_language, 'en'})

    # Normalize scores
    filtered_videos = normalize_engagement_scores(filtered_videos)

    return filtered_videos


if __name__ == "__main__":
    """
    To test from the project root:

    python -m lib.youtube_interactions
    """
    # Add the project root to sys.path when running directly
    import sys
    import os.path

    # Get the project root directory
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    # Configure the YouTube API key for tests
    if not os.environ.get('YOUTUBE_API_KEY'):
        api_key = input("Enter your YOUTUBE_API_KEY: ")
        os.environ['YOUTUBE_API_KEY'] = api_key

    # Example usage of the search function
    test_query = input("Enter the search query (default: 'Python programming'): ") or "Python programming"
    print(f"Searching for: {test_query}...")

    try:
        results = search_youtube_videos(test_query, verbose=True, max_results=2)
        print(f"\nFound {len(results)} videos that match the criteria.")
        for i, video in enumerate(results[:5], 1):  # Show only the first 5 results
            print(f"\n{i}. {video.title}")
            print(f"   Engagement Score: {video.engagement_score}")
            print(f"   Views: {video.view_count}, Likes: {video.like_count}")
            print(f"   URL: {video.url}")
    except Exception as e:
        print(f"Error during search: {e}")
        import traceback

        traceback.print_exc()

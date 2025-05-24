import os

from googleapiclient.discovery import build

# Configurazione API keys
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')


def search_youtube_videos(query, max_results=5):
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY non è impostata")

    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    yt_request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results,
        relevanceLanguage='it',
        order='rating',
        videoDimension='2d',
    )

    response = yt_request.execute()

    # Crea un file di log per la risposta
    with open('youtube_responses.log', 'a', encoding="utf-8") as log_file:
        log_file.write("----------------------------------\n")
        log_file.write(f"Query: {query}\n")
        log_file.write(f"Response: \n")
        log_file.write(str(response))


    videos = []
    for item in response['items']:
        video = {
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'thumbnail': item['snippet']['thumbnails']['high']['url'],
            'video_id': item['id']['videoId'],
            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        }
        videos.append(video)

    return videos
import os

from googleapiclient.discovery import build

# Configurazione API keys
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')


def search_youtube_videos(query, max_results=50, min_subscribers=30000):
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
        videoCaption='closedCaption',  # Preferisci video con sottotitoli
        videoCategoryId='27'  # 27 è la categoria Education
    )

    response = yt_request.execute()

    # Lista temporanea per raccogliere i video e i loro canali
    videos = []
    channel_ids = set()

    for item in response['items']:
        channel_id = item['snippet']['channelId']
        channel_ids.add(channel_id)
        videos.append({
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'thumbnail': item['snippet']['thumbnails']['high']['url'],
            'video_id': item['id']['videoId'],
            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            'channel_id': channel_id
        })

    # Ottieni informazioni sui canali in batch
    channels_data = {}
    if channel_ids:
        channels_request = youtube.channels().list(
            part='statistics,snippet',
            id=','.join(channel_ids)
        )
        channels_response = channels_request.execute()

        # Crea un dizionario con le informazioni dei canali
        for channel in channels_response.get('items', []):
            channel_id = channel['id']
            subscriber_count = int(channel['statistics'].get('subscriberCount', 0))
            language = channel['snippet'].get('defaultLanguage', '')

            channels_data[channel_id] = {
                'subscriber_count': subscriber_count,
                'language': language
            }

    # Filtra i video in base ai criteri
    filtered_videos = []
    for video in videos:
        channel_info = channels_data.get(video['channel_id'], {})
        subscribers = channel_info.get('subscriber_count', 0)
        language = channel_info.get('language', '')

        # Verifica che il canale abbia abbastanza iscritti e la lingua sia accettabile
        if subscribers >= min_subscribers and (not language or language in ['it', 'en']):
            # Aggiungi informazioni sul canale al video
            video['channel_subscribers'] = subscribers
            filtered_videos.append(video)


    # Crea un file di log per la risposta
    with open('youtube_responses.log', 'a', encoding="utf-8") as log_file:
        log_file.write("----------------------------------\n")
        log_file.write(f"Query: {query}\n")
        log_file.write(f"Response: \n")
        log_file.write(str(filtered_videos))

    return filtered_videos
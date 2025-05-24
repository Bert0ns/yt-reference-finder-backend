import os

from googleapiclient.discovery import build

# Configurazione API keys
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
        videos = []
        channel_ids = set()
        video_ids = []

        for item in response['items']:
            channel_id = item['snippet']['channelId']
            video_id = item['id']['videoId']
            channel_ids.add(channel_id)
            video_ids.append(video_id)
            videos.append({
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'video_id': video_id,
                'url': f"https://www.youtube.com/watch?v={video_id}",
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

            for channel in channels_response.get('items', []):
                channel_id = channel['id']
                subscriber_count = int(channel['statistics'].get('subscriberCount', 0))
                language = channel['snippet'].get('defaultLanguage', '')

                channels_data[channel_id] = {
                    'subscriber_count': subscriber_count,
                    'language': language
                }

        # Ottieni statistiche dei video in batch
        videos_statistics = {}
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
                videos_statistics[video_id] = {
                    'like_count': like_count,
                    'view_count': view_count
                }

        # Filtra i video in base ai criteri
        filtered_videos = []
        for video in videos:
            channel_info = channels_data.get(video['channel_id'], {})
            video_stats = videos_statistics.get(video['video_id'], {})

            subscribers = channel_info.get('subscriber_count', 0)
            language = channel_info.get('language', '')
            like_count = video_stats.get('like_count', 0)
            view_count = video_stats.get('view_count', 0)

            # Calcola un punteggio di engagement (alternativa al rapporto like/dislike)
            engagement_score = 0
            if view_count > 0:
                engagement_score = (like_count / view_count) * 100  # percentuale like/views

            # Verifica tutti i criteri di filtro
            if (subscribers >= min_subscribers and
                (not language or language in ['it', 'en']) and
                like_count >= min_likes):
                # Aggiungi informazioni aggiuntive al video
                video['channel_subscribers'] = subscribers
                video['like_count'] = like_count
                video['view_count'] = view_count
                video['engagement_score'] = round(engagement_score, 2)
                filtered_videos.append(video)

        # Crea un file di log per la risposta
        with open('youtube_responses.log', 'a', encoding="utf-8") as log_file:
            log_file.write("----------------------------------\n")
            log_file.write(f"Query: {query}\n")
            log_file.write(f"Response: \n")
            log_file.write(str(filtered_videos))

        return filtered_videos
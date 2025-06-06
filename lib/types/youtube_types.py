from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict


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


# YouTube objects

@dataclass
class Thumbnail:
    url: str
    width: int = 0
    height: int = 0

    @classmethod
    def from_dict(cls, json_dict: dict):
        """Crea un oggetto Thumbnail da un dizionario JSON."""
        return cls(
            url=json_dict.get('url', ''),
            width=json_dict.get('width', 0),
            height=json_dict.get('height', 0)
        )

    def to_dict(self):
        """Converte l'oggetto Thumbnail in un dizionario JSON."""
        return {
            'url': self.url,
            'width': self.width,
            'height': self.height
        }


@dataclass
class Thumbnails:
    default: Optional[Thumbnail] = None
    medium: Optional[Thumbnail] = None
    high: Optional[Thumbnail] = None
    standard: Optional[Thumbnail] = None
    maxres: Optional[Thumbnail] = None

    @classmethod
    def from_dict(cls, json_dict: dict):
        """        Crea un oggetto Thumbnails da un dizionario JSON."""
        default = None
        medium = None
        high = None
        standard = None
        maxres = None

        if 'default' in json_dict:
            default = Thumbnail.from_dict(json_dict['default'])
        if 'medium' in json_dict:
            medium = Thumbnail.from_dict(json_dict['medium'])
        if 'high' in json_dict:
            high = Thumbnail.from_dict(json_dict['high'])
        if 'standard' in json_dict:
            standard = Thumbnail.from_dict(json_dict['standard'])
        if 'maxres' in json_dict:
            maxres = Thumbnail.from_dict(json_dict['maxres'])

        return cls(
            default=default,
            medium=medium,
            high=high,
            standard=standard,
            maxres=maxres
        )

    def to_dict(self):
        """Converte l'oggetto Thumbnails in un dizionario JSON."""
        return {
            'default': self.default.to_dict() if self.default else None,
            'medium': self.medium.to_dict() if self.medium else None,
            'high': self.high.to_dict() if self.high else None,
            'standard': self.standard.to_dict() if self.standard else None,
            'maxres': self.maxres.to_dict() if self.maxres else None
        }


@dataclass
class Localized:
    title: str = ""
    description: str = ""

    @classmethod
    def from_dict(cls, json_dict: dict) -> 'Localized':
        """Crea un oggetto Localized da un dizionario JSON."""
        return cls(
            title=json_dict.get('title', ''),
            description=json_dict.get('description', '')
        )

    def to_dict(self) -> dict:
        """Converte l'oggetto Localized in un dizionario JSON."""
        return {
            'title': self.title,
            'description': self.description
        }


@dataclass
class RegionRestriction:
    allowed: List[str] = field(default_factory=list)
    blocked: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, json_dict: dict) -> 'RegionRestriction':
        """Crea un oggetto RegionRestriction da un dizionario JSON."""
        return cls(
            allowed=json_dict.get('allowed', []),
            blocked=json_dict.get('blocked', [])
        )

    def to_dict(self) -> dict:
        """Converte l'oggetto RegionRestriction in un dizionario JSON."""
        return {
            'allowed': self.allowed,
            'blocked': self.blocked
        }


@dataclass
class ContentRating:
    # TODO aggiungi tutti i campi di ContentRating secondo le specifiche di YouTube
    # Includo solo alcuni campi rappresentativi
    acb_rating: str = ""
    mpaa_rating: str = ""
    yt_rating: str = ""

    # Aggiungere gli altri rating secondo necessità

    @classmethod
    def from_dict(cls, param) -> 'ContentRating':
        """Crea un oggetto ContentRating da un dizionario JSON."""
        return cls(
            acb_rating=param.get('acbRating', ''),
            mpaa_rating=param.get('mpaaRating', ''),
            yt_rating=param.get('ytRating', '')
            # Aggiungere gli altri campi secondo necessità
        )

    def to_dict(self):
        """Converte l'oggetto ContentRating in un dizionario JSON."""
        return {
            'acbRating': self.acb_rating,
            'mpaaRating': self.mpaa_rating,
            'ytRating': self.yt_rating
            # Aggiungere gli altri campi secondo necessità
        }


@dataclass
class ContentDetails:
    duration: str = ""
    dimension: str = ""
    definition: str = ""
    caption: str = ""
    licensedContent: bool = False
    regionRestriction: RegionRestriction = field(default_factory=RegionRestriction)
    contentRating: ContentRating = field(default_factory=ContentRating)
    projection: str = ""
    hasCustomThumbnail: bool = False

    @classmethod
    def from_dict(cls, json_dict: dict) -> 'ContentDetails':
        """
        Crea un oggetto ContentDetails da un dizionario JSON.

        Args:
            json_dict: Dizionario contenente i dati dei dettagli del contenuto

        Returns:
            Un'istanza di ContentDetails
        """
        region_restriction = RegionRestriction.from_dict(json_dict.get('regionRestriction', {}))
        content_rating = ContentRating.from_dict(json_dict.get('contentRating', {}))

        return cls(
            duration=json_dict.get('duration', ''),
            dimension=json_dict.get('dimension', ''),
            definition=json_dict.get('definition', ''),
            caption=json_dict.get('caption', ''),
            licensedContent=json_dict.get('licensedContent', False),
            regionRestriction=region_restriction,
            contentRating=content_rating,
            projection=json_dict.get('projection', ''),
            hasCustomThumbnail=json_dict.get('hasCustomThumbnail', False)
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei dettagli del contenuto.
        """
        return {
            'duration': self.duration,
            'dimension': self.dimension,
            'definition': self.definition,
            'caption': self.caption,
            'licensedContent': self.licensedContent,
            'regionRestriction': self.regionRestriction.to_dict(),
            'contentRating': self.contentRating.to_dict(),
            'projection': self.projection,
            'hasCustomThumbnail': self.hasCustomThumbnail
        }


@dataclass
class Status:
    upload_status: str = ""
    failure_reason: str = ""
    rejection_reason: str = ""
    privacy_status: str = ""
    publish_at: Optional[datetime] = None
    license: str = ""
    embeddable: bool = True
    public_stats_viewable: bool = True
    made_for_kids: bool = False
    self_declared_made_for_kids: bool = False
    contains_synthetic_media: bool = False

    @classmethod
    def from_dict(cls, param) -> 'Status':
        """
        Crea un oggetto Status da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dello stato

        Returns:
            Un'istanza di Status
        """
        return cls(
            upload_status=param.get('uploadStatus', ''),
            failure_reason=param.get('failureReason', ''),
            rejection_reason=param.get('rejectionReason', ''),
            privacy_status=param.get('privacyStatus', ''),
            publish_at=datetime.fromisoformat(param['publishAt']) if 'publishAt' in param else None,
            license=param.get('license', ''),
            embeddable=param.get('embeddable', True),
            public_stats_viewable=param.get('publicStatsViewable', True),
            made_for_kids=param.get('madeForKids', False),
            self_declared_made_for_kids=param.get('selfDeclaredMadeForKids', False),
            contains_synthetic_media=param.get('containsSyntheticMedia', False)
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dello stato.
        """
        return {
            'uploadStatus': self.upload_status,
            'failureReason': self.failure_reason,
            'rejectionReason': self.rejection_reason,
            'privacyStatus': self.privacy_status,
            'publishAt': self.publish_at.isoformat() if self.publish_at else None,
            'license': self.license,
            'embeddable': self.embeddable,
            'publicStatsViewable': self.public_stats_viewable,
            'madeForKids': self.made_for_kids,
            'selfDeclaredMadeForKids': self.self_declared_made_for_kids,
            'containsSyntheticMedia': self.contains_synthetic_media
        }


@dataclass
class Statistics:
    view_count: str = "0"
    like_count: str = "0"
    dislike_count: str = "0"
    favorite_count: str = "0"
    comment_count: str = "0"

    @classmethod
    def from_dict(cls, param):
        """
        Crea un oggetto Statistics da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati delle statistiche

        Returns:
            Un'istanza di Statistics
        """
        return cls(
            view_count=param.get('viewCount', '0'),
            like_count=param.get('likeCount', '0'),
            dislike_count=param.get('dislikeCount', '0'),
            favorite_count=param.get('favoriteCount', '0'),
            comment_count=param.get('commentCount', '0')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati delle statistiche.
        """
        return {
            'viewCount': self.view_count,
            'likeCount': self.like_count,
            'dislikeCount': self.dislike_count,
            'favoriteCount': self.favorite_count,
            'commentCount': self.comment_count
        }


@dataclass
class PaidProductPlacementDetails:
    has_paid_product_placement: bool = False

    @classmethod
    def from_dict(cls, param):
        """
        Crea un oggetto PaidProductPlacementDetails da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dei dettagli del posizionamento del prodotto a pagamento

        Returns:
            Un'istanza di PaidProductPlacementDetails
        """
        return cls(
            has_paid_product_placement=param.get('hasPaidProductPlacement', False)
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei dettagli del posizionamento del prodotto a pagamento.
        """
        return {
            'hasPaidProductPlacement': self.has_paid_product_placement
        }


@dataclass
class Player:
    embedHtml: str = ""
    embedHeight: int = 0
    embedWidth: int = 0

    @classmethod
    def from_dict(cls, param):
        """
        Crea un oggetto Player da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati del player

        Returns:
            Un'istanza di Player
        """
        return cls(
            embedHtml=param.get('embedHtml', ''),
            embedHeight=param.get('embedHeight', 0),
            embedWidth=param.get('embedWidth', 0)
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati del player.
        """
        return {
            'embedHtml': self.embedHtml,
            'embedHeight': self.embedHeight,
            'embedWidth': self.embedWidth
        }


@dataclass
class TopicDetails:
    topicIds: List[str] = field(default_factory=list)
    relevantTopicIds: List[str] = field(default_factory=list)
    topic_categories: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, param):
        """
        Crea un oggetto TopicDetails da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dei dettagli del topic

        Returns:
            Un'istanza di TopicDetails
        """
        return cls(
            topicIds=param.get('topicIds', []),
            relevantTopicIds=param.get('relevantTopicIds', []),
            topic_categories=param.get('topicCategories', [])
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei dettagli del topic.
        """
        return {
            'topicIds': self.topicIds,
            'relevantTopicIds': self.relevantTopicIds,
            'topicCategories': self.topic_categories
        }


@dataclass
class RecordingDetails:
    recording_date: Optional[datetime] = None

    @classmethod
    def from_dict(cls, param) -> 'RecordingDetails':
        """
        Crea un oggetto RecordingDetails da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dei dettagli di registrazione

        Returns:
            Un'istanza di RecordingDetails
        """
        return cls(
            recording_date=datetime.fromisoformat(param['recordingDate']) if 'recordingDate' in param else None
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei dettagli di registrazione.
        """
        return {
            'recordingDate': self.recording_date.isoformat() if self.recording_date else None
        }


@dataclass
class VideoStream:
    widthPixels: int = 0
    heightPixels: int = 0
    frameRateFps: float = 0.0
    aspectRatio: float = 0.0
    codec: str = ""
    bitrateBps: int = 0
    rotation: str = ""
    vendor: str = ""

    @classmethod
    def from_dict(cls, vs):
        """
        Crea un oggetto VideoStream da un dizionario JSON.

        Args:
            vs: Dizionario contenente i dati dello stream video

        Returns:
            Un'istanza di VideoStream
        """
        return cls(
            widthPixels=vs.get('widthPixels', 0),
            heightPixels=vs.get('heightPixels', 0),
            frameRateFps=vs.get('frameRateFps', 0.0),
            aspectRatio=vs.get('aspectRatio', 0.0),
            codec=vs.get('codec', ''),
            bitrateBps=vs.get('bitrateBps', 0),
            rotation=vs.get('rotation', ''),
            vendor=vs.get('vendor', '')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dello stream video.
        """
        return {
            'widthPixels': self.widthPixels,
            'heightPixels': self.heightPixels,
            'frameRateFps': self.frameRateFps,
            'aspectRatio': self.aspectRatio,
            'codec': self.codec,
            'bitrateBps': self.bitrateBps,
            'rotation': self.rotation,
            'vendor': self.vendor
        }


@dataclass
class AudioStream:
    channel_count: int = 0
    codec: str = ""
    bitrate_bps: int = 0
    vendor: str = ""

    @classmethod
    def from_dict(cls, json_dict: dict) -> 'AudioStream':
        """
        Crea un oggetto AudioStream da un dizionario JSON.

        Args:
            json_dict: Dizionario contenente i dati dello stream audio

        Returns:
            Un'istanza di AudioStream
        """
        return cls(
            channel_count=json_dict.get('channelCount', 0),
            codec=json_dict.get('codec', ''),
            bitrate_bps=json_dict.get('bitrateBps', 0),
            vendor=json_dict.get('vendor', '')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dello stream audio.
        """
        return {
            'channelCount': self.channel_count,
            'codec': self.codec,
            'bitrateBps': self.bitrate_bps,
            'vendor': self.vendor
        }


@dataclass
class FileDetails:
    file_name: str = ""
    file_size: int = 0
    file_type: str = ""
    container: str = ""
    video_streams: List[VideoStream] = field(default_factory=list)
    audio_streams: List[AudioStream] = field(default_factory=list)
    duration_ms: int = 0
    bitrate_bps: int = 0
    creation_time: str = ""

    @classmethod
    def from_dict(cls, param):
        """
        Crea un oggetto FileDetails da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dei dettagli del file

        Returns:
            Un'istanza di FileDetails
        """
        video_streams = [VideoStream.from_dict(vs) for vs in param.get('videoStreams', [])]
        audio_streams = [AudioStream.from_dict(as_) for as_ in param.get('audioStreams', [])]

        return cls(
            file_name=param.get('fileName', ''),
            file_size=param.get('fileSize', 0),
            file_type=param.get('fileType', ''),
            container=param.get('container', ''),
            video_streams=video_streams,
            audio_streams=audio_streams,
            duration_ms=param.get('durationMs', 0),
            bitrate_bps=param.get('bitrateBps', 0),
            creation_time=param.get('creationTime', '')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei dettagli del file.
        """
        return {
            'fileName': self.file_name,
            'fileSize': self.file_size,
            'fileType': self.file_type,
            'container': self.container,
            'videoStreams': [vs.to_dict() for vs in self.video_streams],
            'audioStreams': [as_.to_dict() for as_ in self.audio_streams],
            'durationMs': self.duration_ms,
            'bitrateBps': self.bitrate_bps,
            'creationTime': self.creation_time
        }


@dataclass
class ProcessingProgress:
    partsTotal: int = 0
    partsProcessed: int = 0
    timeLeftMs: int = 0

    @classmethod
    def from_dict(cls, param: dict) -> 'ProcessingProgress':
        """
        Crea un oggetto ProcessingProgress da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati del progresso dell'elaborazione

        Returns:
            Un'istanza di ProcessingProgress
        """
        return cls(
            partsTotal=param.get('partsTotal', 0),
            partsProcessed=param.get('partsProcessed', 0),
            timeLeftMs=param.get('timeLeftMs', 0)
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati del progresso dell'elaborazione.
        """
        return {
            'partsTotal': self.partsTotal,
            'partsProcessed': self.partsProcessed,
            'timeLeftMs': self.timeLeftMs
        }


@dataclass
class ProcessingDetails:
    processingStatus: str = ""
    processingProgress: ProcessingProgress = field(default_factory=ProcessingProgress)
    processingFailureReason: str = ""
    fileDetailsAvailability: str = ""
    processingIssuesAvailability: str = ""
    tagSuggestionsAvailability: str = ""
    editorSuggestionsAvailability: str = ""
    thumbnailsAvailability: str = ""

    @classmethod
    def from_dict(cls, param) -> 'ProcessingDetails':
        """
        Crea un oggetto ProcessingDetails da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dei dettagli di elaborazione

        Returns:
            Un'istanza di ProcessingDetails
        """
        processing_progress = ProcessingProgress.from_dict(param.get('processingProgress', {}))

        return cls(
            processingStatus=param.get('processingStatus', ''),
            processingProgress=processing_progress,
            processingFailureReason=param.get('processingFailureReason', ''),
            fileDetailsAvailability=param.get('fileDetailsAvailability', ''),
            processingIssuesAvailability=param.get('processingIssuesAvailability', ''),
            tagSuggestionsAvailability=param.get('tagSuggestionsAvailability', ''),
            editorSuggestionsAvailability=param.get('editorSuggestionsAvailability', ''),
            thumbnailsAvailability=param.get('thumbnailsAvailability', '')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei dettagli di elaborazione.
        """
        return {
            'processingStatus': self.processingStatus,
            'processingProgress': self.processingProgress.to_dict(),
            'processingFailureReason': self.processingFailureReason,
            'fileDetailsAvailability': self.fileDetailsAvailability,
            'processingIssuesAvailability': self.processingIssuesAvailability,
            'tagSuggestionsAvailability': self.tagSuggestionsAvailability,
            'editorSuggestionsAvailability': self.editorSuggestionsAvailability,
            'thumbnailsAvailability': self.thumbnailsAvailability
        }


@dataclass
class TagSuggestion:
    tag: str = ""
    categoryRestricts: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, ts):
        """
        Crea un oggetto TagSuggestion da un dizionario JSON.

        Args:
            ts: Dizionario contenente i dati del suggerimento di tag

        Returns:
            Un'istanza di TagSuggestion
        """
        return cls(
            tag=ts.get('tag', ''),
            categoryRestricts=ts.get('categoryRestricts', [])
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati del suggerimento di tag.
        """
        return {
            'tag': self.tag,
            'categoryRestricts': self.categoryRestricts
        }


@dataclass
class Suggestions:
    processingErrors: List[str] = field(default_factory=list)
    processingWarnings: List[str] = field(default_factory=list)
    processingHints: List[str] = field(default_factory=list)
    tagSuggestions: List[TagSuggestion] = field(default_factory=list)
    editorSuggestions: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, param: dict) -> 'Suggestions':
        """
        Crea un oggetto Suggestions da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dei suggerimenti

        Returns:
            Un'istanza di Suggestions
        """
        tag_suggestions = [TagSuggestion.from_dict(ts) for ts in param.get('tagSuggestions', [])]

        return cls(
            processingErrors=param.get('processingErrors', []),
            processingWarnings=param.get('processingWarnings', []),
            processingHints=param.get('processingHints', []),
            tagSuggestions=tag_suggestions,
            editorSuggestions=param.get('editorSuggestions', [])
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei suggerimenti.
        """
        return {
            'processingErrors': self.processingErrors,
            'processingWarnings': self.processingWarnings,
            'processingHints': self.processingHints,
            'tagSuggestions': [ts.to_dict() for ts in self.tagSuggestions],
            'editorSuggestions': self.editorSuggestions
        }


@dataclass
class LiveStreamingDetails:
    actualStartTime: Optional[datetime] = None
    actualEndTime: Optional[datetime] = None
    scheduledStartTime: Optional[datetime] = None
    scheduledEndTime: Optional[datetime] = None
    concurrentViewers: int = 0
    activeLiveChatId: str = ""

    @classmethod
    def from_dict(cls, param: dict) -> 'LiveStreamingDetails':
        """
        Crea un oggetto LiveStreamingDetails da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dei dettagli dello streaming live

        Returns:
            Un'istanza di LiveStreamingDetails
        """
        return cls(
            actualStartTime=datetime.fromisoformat(param['actualStartTime']) if 'actualStartTime' in param else None,
            actualEndTime=datetime.fromisoformat(param['actualEndTime']) if 'actualEndTime' in param else None,
            scheduledStartTime=datetime.fromisoformat(
                param['scheduledStartTime']) if 'scheduledStartTime' in param else None,
            scheduledEndTime=datetime.fromisoformat(param['scheduledEndTime']) if 'scheduledEndTime' in param else None,
            concurrentViewers=param.get('concurrentViewers', 0),
            activeLiveChatId=param.get('activeLiveChatId', '')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei dettagli dello streaming live.
        """
        return {
            'actualStartTime': self.actualStartTime.isoformat() if self.actualStartTime else None,
            'actualEndTime': self.actualEndTime.isoformat() if self.actualEndTime else None,
            'scheduledStartTime': self.scheduledStartTime.isoformat() if self.scheduledStartTime else None,
            'scheduledEndTime': self.scheduledEndTime.isoformat() if self.scheduledEndTime else None,
            'concurrentViewers': self.concurrentViewers,
            'activeLiveChatId': self.activeLiveChatId
        }


@dataclass
class VideoResourceSnippet:
    publishedAt: Optional[datetime] = None
    channelId: str = ""
    title: str = ""
    description: str = ""
    thumbnails: Thumbnails = field(default_factory=Thumbnails)
    channelTitle: str = ""
    tags: List[str] = field(default_factory=list)
    categoryId: str = ""
    liveBroadcastContent: str = ""
    defaultLanguage: str = ""
    localized: Localized = field(default_factory=Localized)
    defaultAudioLanguage: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> 'VideoResourceSnippet':
        """
        Crea un oggetto VideoResourceSnippet da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati dello snippet della risorsa video

        Returns:
            Un'istanza di VideoResourceSnippet
        """
        thumbnails = Thumbnails.from_dict(data.get('thumbnails', {}))
        localized = Localized.from_dict(data.get('localized', {}))

        return cls(
            publishedAt=datetime.fromisoformat(data['publishedAt']) if 'publishedAt' in data else None,
            channelId=data.get('channelId', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            thumbnails=thumbnails,
            channelTitle=data.get('channelTitle', ''),
            tags=data.get('tags', []),
            categoryId=data.get('categoryId', ''),
            liveBroadcastContent=data.get('liveBroadcastContent', ''),
            defaultLanguage=data.get('defaultLanguage', ''),
            localized=localized,
            defaultAudioLanguage=data.get('defaultAudioLanguage', '')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dello snippet della risorsa video.
        """
        return {
            'publishedAt': self.publishedAt.isoformat() if self.publishedAt else None,
            'channelId': self.channelId,
            'title': self.title,
            'description': self.description,
            'thumbnails': self.thumbnails.to_dict(),
            'channelTitle': self.channelTitle,
            'tags': self.tags,
            'categoryId': self.categoryId,
            'liveBroadcastContent': self.liveBroadcastContent,
            'defaultLanguage': self.defaultLanguage,
            'localized': self.localized.to_dict(),
            'defaultAudioLanguage': self.defaultAudioLanguage
        }


@dataclass
class VideoResource:
    kind: str = "youtube#video"
    etag: str = ""
    id: str = ""
    snippet: VideoResourceSnippet = field(default_factory=VideoResourceSnippet)
    contentDetails: ContentDetails = field(default_factory=ContentDetails)
    status: Status = field(default_factory=Status)
    statistics: Statistics = field(default_factory=Statistics)
    paidProductPlacementDetails: PaidProductPlacementDetails = field(default_factory=PaidProductPlacementDetails)
    player: Player = field(default_factory=Player)
    topicDetails: TopicDetails = field(default_factory=TopicDetails)
    recordingDetails: RecordingDetails = field(default_factory=RecordingDetails)
    fileDetails: FileDetails = field(default_factory=FileDetails)
    processingDetails: ProcessingDetails = field(default_factory=ProcessingDetails)
    suggestions: Suggestions = field(default_factory=Suggestions)
    liveStreamingDetails: LiveStreamingDetails = field(default_factory=LiveStreamingDetails)
    localizations: Dict[str, Localized] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> 'VideoResource':
        """
        Crea un oggetto VideoResource da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati della risorsa video

        Returns:
            Un'istanza di VideoResource
        """
        kind_received = data.get('kind', '')
        if kind_received != 'youtube#video':
            raise ValueError(f"Expected kind='youtube#video', got '{kind_received}'")

        snippet = VideoResourceSnippet.from_dict(data.get('snippet', {}))
        content_details = ContentDetails.from_dict(data.get('contentDetails', {}))
        status = Status.from_dict(data.get('status', {}))
        statistics = Statistics.from_dict(data.get('statistics', {}))
        paid_product_placement_details = PaidProductPlacementDetails.from_dict(
            data.get('paidProductPlacementDetails', {}))
        player = Player.from_dict(data.get('player', {}))
        topic_details = TopicDetails.from_dict(data.get('topicDetails', {}))
        recording_details = RecordingDetails.from_dict(data.get('recordingDetails', {}))
        file_details = FileDetails.from_dict(data.get('fileDetails', {}))
        processing_details = ProcessingDetails.from_dict(data.get('processingDetails', {}))
        suggestions = Suggestions.from_dict(data.get('suggestions', {}))
        live_streaming_details = LiveStreamingDetails.from_dict(data.get('liveStreamingDetails', {}))

        localizations_data = data.get('localizations', {})
        localizations = {lang: Localized.from_dict(loc) for lang, loc in localizations_data.items()}

        return cls(
            kind=kind_received,
            etag=data.get('etag', ''),
            id=data.get('id', ''),
            snippet=snippet,
            contentDetails=content_details,
            status=status,
            statistics=statistics,
            paidProductPlacementDetails=paid_product_placement_details,
            player=player,
            topicDetails=topic_details,
            recordingDetails=recording_details,
            fileDetails=file_details,
            processingDetails=processing_details,
            suggestions=suggestions,
            liveStreamingDetails=live_streaming_details,
            localizations=localizations
        )


@dataclass
class SearchResourceId:
    kind: str = ""
    videoId: str = ""
    channelId: str = ""
    playlistId: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> 'SearchResourceId':
        """
        Crea un oggetto YouTubeSearchResourceId da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati dell'ID della risorsa di ricerca

        Returns:
            Un'istanza di YouTubeSearchResourceId
        """
        return cls(
            kind=data.get('kind', ''),
            videoId=data.get('videoId', ''),
            channelId=data.get('channelId', ''),
            playlistId=data.get('playlistId', '')
        )

    def to_dict(self):
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dell'ID della risorsa di ricerca.
        """
        return {
            'kind': self.kind,
            'videoId': self.videoId,
            'channelId': self.channelId,
            'playlistId': self.playlistId
        }


@dataclass
class SearchResourceSnippet:
    publishedAt: Optional[datetime] = None
    channelId: str = ""
    title: str = ""
    description: str = ""
    thumbnails: Thumbnails = field(default_factory=Thumbnails)
    channelTitle: str = ""
    liveBroadcastContent: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> 'SearchResourceSnippet':
        """
        Crea un oggetto SearchResourceSnippet da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati dello snippet della risorsa di ricerca

        Returns:
            Un'istanza di SearchResourceSnippet
        """
        thumbnails = Thumbnails.from_dict(data.get('thumbnails', {}))
        return cls(
            publishedAt=datetime.fromisoformat(data['publishedAt']) if 'publishedAt' in data else None,
            channelId=data.get('channelId', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            thumbnails=thumbnails,
            channelTitle=data.get('channelTitle', ''),
            liveBroadcastContent=data.get('liveBroadcastContent', '')
        )

    def to_dict(self):
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dello snippet della risorsa di ricerca.
        """
        return {
            'publishedAt': self.publishedAt.isoformat() if self.publishedAt else None,
            'channelId': self.channelId,
            'title': self.title,
            'description': self.description,
            'thumbnails': self.thumbnails.to_dict(),
            'channelTitle': self.channelTitle,
            'liveBroadcastContent': self.liveBroadcastContent
        }


@dataclass
class SearchResource:
    kind: str = "youtube#searchResult"
    etag: str = ""
    id: SearchResourceId = field(default_factory=SearchResourceId)
    snippet: SearchResourceSnippet = field(default_factory=SearchResourceSnippet)

    @classmethod
    def from_dict(cls, data: dict) -> 'SearchResource':
        """
        Crea un oggetto YoutubeSearchResource da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati della risorsa di ricerca

        Returns:
            Un'istanza di YoutubeSearchResource
        """
        kind_received = data.get('kind', '')
        if kind_received != 'youtube#searchResult':
            raise ValueError(f"Expected kind='youtube#searchResult', got '{kind_received}'")

        resource_id = SearchResourceId.from_dict(data.get('id', {}))
        snippet = SearchResourceSnippet.from_dict(data.get('snippet', {}))

        return cls(
            kind=kind_received,
            etag=data.get('etag', ''),
            id=resource_id,
            snippet=snippet
        )

    def to_dict(self):
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati della risorsa di ricerca.
        """
        return {
            'kind': self.kind,
            'etag': self.etag,
            'id': self.id.to_dict(),
            'snippet': self.snippet.to_dict()
        }


@dataclass
class PageInfo:
    totalResults: int = 0
    resultsPerPage: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> 'PageInfo':
        """
        Crea un oggetto PageInfo da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati della pagina

        Returns:
            Un'istanza di PageInfo
        """
        return cls(
            totalResults=data.get('totalResults', 0),
            resultsPerPage=data.get('resultsPerPage', 0)
        )


@dataclass
class YouTubeSearchListResponse:
    kind: str = "youtube#searchListResponse"
    etag: str = ""
    nextPageToken: Optional[str] = None
    prevPageToken: Optional[str] = None
    regionCode: Optional[str] = None
    pageInfo: PageInfo = field(default_factory=PageInfo)
    items: List[SearchResource] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'YouTubeSearchListResponse':
        """
        Crea un oggetto YouTubeSearchListResponse da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati della risposta di ricerca di YouTube

        Returns:
            Un'istanza di YouTubeSearchListResponse
        """

        kind_received = data.get('kind', '')
        if kind_received != 'youtube#searchListResponse':
            raise ValueError(f"Expected kind='youtube#searchListResponse', got '{kind_received}'")

        # Utilizzo from_dict per PageInfo
        page_info = PageInfo.from_dict(data.get('pageInfo', {}))

        # Elabora gli elementi
        items = []
        for item_data in data.get('items', []):
            # Utilizza from_dict per YoutubeSearchResource
            search_item = SearchResource.from_dict(item_data)
            items.append(search_item)

        # Crea e restituisce l'oggetto di risposta
        return cls(
            kind=kind_received,
            etag=data.get('etag', ''),
            nextPageToken=data.get('nextPageToken'),
            prevPageToken=data.get('prevPageToken'),
            regionCode=data.get('regionCode'),
            pageInfo=page_info,
            items=items
        )

    def to_dict(self):
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati della risposta di ricerca di YouTube.
        """
        return {
            'kind': self.kind,
            'etag': self.etag,
            'nextPageToken': self.nextPageToken,
            'prevPageToken': self.prevPageToken,
            'regionCode': self.regionCode,
            'pageInfo': self.pageInfo.__dict__,
            'items': [item.to_dict() for item in self.items]
        }

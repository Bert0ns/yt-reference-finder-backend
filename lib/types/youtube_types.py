from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict


def parse_iso_datetime(datetime_str: Optional[str]) -> Optional[datetime]:
    """
    Converte una stringa di data ISO 8601 in un oggetto datetime,
    gestendo correttamente i suffissi 'Z'.

    Args:
        datetime_str: La stringa di data in formato ISO 8601

    Returns:
        Un oggetto datetime o None se l'input è None
    """
    if not datetime_str:
        return None

    # Gestisci il formato con 'Z' (UTC/Zulu time)
    if datetime_str.endswith('Z'):
        datetime_str = datetime_str[:-1] + '+00:00'

    return datetime.fromisoformat(datetime_str)


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

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati della pagina.
        """
        return {
            'totalResults': self.totalResults,
            'resultsPerPage': self.resultsPerPage
        }


@dataclass
class VideoRegionRestriction:
    allowed: List[str] = field(default_factory=list)
    blocked: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, json_dict: dict) -> 'VideoRegionRestriction':
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
class VideoContentRating:
    # Includo solo alcuni campi rappresentativi
    ytRating: str = ""

    # Aggiungere gli altri rating secondo necessità

    @classmethod
    def from_dict(cls, param) -> 'VideoContentRating':
        """Crea un oggetto ContentRating da un dizionario JSON."""
        return cls(
            ytRating=param.get('ytRating', '')
            # Aggiungere gli altri campi secondo necessità
        )

    def to_dict(self):
        """Converte l'oggetto ContentRating in un dizionario JSON."""
        return {
            'ytRating': self.ytRating
            # Aggiungere gli altri campi secondo necessità
        }


@dataclass
class VideoContentDetails:
    duration: str = ""
    dimension: str = ""
    definition: str = ""
    caption: str = ""
    licensedContent: bool = False
    regionRestriction: VideoRegionRestriction = field(default_factory=VideoRegionRestriction)
    contentRating: VideoContentRating = field(default_factory=VideoContentRating)
    projection: str = ""
    hasCustomThumbnail: bool = False

    @classmethod
    def from_dict(cls, json_dict: dict) -> 'VideoContentDetails':
        """
        Crea un oggetto ContentDetails da un dizionario JSON.

        Args:
            json_dict: Dizionario contenente i dati dei dettagli del contenuto

        Returns:
            Un'istanza di ContentDetails
        """
        region_restriction = VideoRegionRestriction.from_dict(json_dict.get('regionRestriction', {}))
        content_rating = VideoContentRating.from_dict(json_dict.get('contentRating', {}))

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
class VideoStatus:
    uploadStatus: str = ""
    failureReason: str = ""
    rejectionReason: str = ""
    privacyStatus: str = ""
    publishAt: Optional[datetime] = None
    license: str = ""
    embeddable: bool = True
    publicStatsViewable: bool = True
    madeForFids: bool = False
    selfDeclaredMadeForKids: bool = False
    containsSyntheticMedia: bool = False

    @classmethod
    def from_dict(cls, param) -> 'VideoStatus':
        """
        Crea un oggetto Status da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dello stato

        Returns:
            Un'istanza di Status
        """
        return cls(
            uploadStatus=param.get('uploadStatus', ''),
            failureReason=param.get('failureReason', ''),
            rejectionReason=param.get('rejectionReason', ''),
            privacyStatus=param.get('privacyStatus', ''),
            publishAt=parse_iso_datetime(param.get('publishAt', None)),
            license=param.get('license', ''),
            embeddable=param.get('embeddable', True),
            publicStatsViewable=param.get('publicStatsViewable', True),
            madeForFids=param.get('madeForKids', False),
            selfDeclaredMadeForKids=param.get('selfDeclaredMadeForKids', False),
            containsSyntheticMedia=param.get('containsSyntheticMedia', False)
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dello stato.
        """
        return {
            'uploadStatus': self.uploadStatus,
            'failureReason': self.failureReason,
            'rejectionReason': self.rejectionReason,
            'privacyStatus': self.privacyStatus,
            'publishAt': self.publishAt.isoformat() if self.publishAt else None,
            'license': self.license,
            'embeddable': self.embeddable,
            'publicStatsViewable': self.publicStatsViewable,
            'madeForKids': self.madeForFids,
            'selfDeclaredMadeForKids': self.selfDeclaredMadeForKids,
            'containsSyntheticMedia': self.containsSyntheticMedia
        }


@dataclass
class VideoStatistics:
    viewCount: str = "0"
    likeCount: str = "0"
    dislikeCount: str = "0"
    favoriteCount: str = "0"
    commentCount: str = "0"

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
            viewCount=param.get('viewCount', '0'),
            likeCount=param.get('likeCount', '0'),
            dislikeCount=param.get('dislikeCount', '0'),
            favoriteCount=param.get('favoriteCount', '0'),
            commentCount=param.get('commentCount', '0')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati delle statistiche.
        """
        return {
            'viewCount': self.viewCount,
            'likeCount': self.likeCount,
            'dislikeCount': self.dislikeCount,
            'favoriteCount': self.favoriteCount,
            'commentCount': self.commentCount
        }


@dataclass
class VideoPaidProductPlacementDetails:
    hasPaidProductPlacement: bool = False

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
            hasPaidProductPlacement=param.get('hasPaidProductPlacement', False)
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei dettagli del posizionamento del prodotto a pagamento.
        """
        return {
            'hasPaidProductPlacement': self.hasPaidProductPlacement
        }


@dataclass
class VideoPlayer:
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
class VideoTopicDetails:
    topicIds: List[str] = field(default_factory=list)
    relevantTopicIds: List[str] = field(default_factory=list)
    topicCategories: List[str] = field(default_factory=list)

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
            topicCategories=param.get('topicCategories', [])
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
            'topicCategories': self.topicCategories
        }


@dataclass
class VideoRecordingDetails:
    recordingDate: Optional[datetime] = None

    @classmethod
    def from_dict(cls, param) -> 'VideoRecordingDetails':
        """
        Crea un oggetto RecordingDetails da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dei dettagli di registrazione

        Returns:
            Un'istanza di RecordingDetails
        """
        return cls(
            recordingDate=parse_iso_datetime(param.get('recordingDate', None))
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei dettagli di registrazione.
        """
        return {
            'recordingDate': self.recordingDate.isoformat() if self.recordingDate else None
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
class VideoAudioStream:
    channel_count: int = 0
    codec: str = ""
    bitrate_bps: int = 0
    vendor: str = ""

    @classmethod
    def from_dict(cls, json_dict: dict) -> 'VideoAudioStream':
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
class VideoFileDetails:
    file_name: str = ""
    file_size: int = 0
    file_type: str = ""
    container: str = ""
    video_streams: List[VideoStream] = field(default_factory=list)
    audio_streams: List[VideoAudioStream] = field(default_factory=list)
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
        audio_streams = [VideoAudioStream.from_dict(as_) for as_ in param.get('audioStreams', [])]

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
class VideoProcessingProgress:
    partsTotal: int = 0
    partsProcessed: int = 0
    timeLeftMs: int = 0

    @classmethod
    def from_dict(cls, param: dict) -> 'VideoProcessingProgress':
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
class VideoProcessingDetails:
    processingStatus: str = ""
    processingProgress: VideoProcessingProgress = field(default_factory=VideoProcessingProgress)
    processingFailureReason: str = ""
    fileDetailsAvailability: str = ""
    processingIssuesAvailability: str = ""
    tagSuggestionsAvailability: str = ""
    editorSuggestionsAvailability: str = ""
    thumbnailsAvailability: str = ""

    @classmethod
    def from_dict(cls, param) -> 'VideoProcessingDetails':
        """
        Crea un oggetto ProcessingDetails da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dei dettagli di elaborazione

        Returns:
            Un'istanza di ProcessingDetails
        """
        processing_progress = VideoProcessingProgress.from_dict(param.get('processingProgress', {}))

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
class VideoTagSuggestion:
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
class VideoSuggestions:
    processingErrors: List[str] = field(default_factory=list)
    processingWarnings: List[str] = field(default_factory=list)
    processingHints: List[str] = field(default_factory=list)
    tagSuggestions: List[VideoTagSuggestion] = field(default_factory=list)
    editorSuggestions: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, param: dict) -> 'VideoSuggestions':
        """
        Crea un oggetto Suggestions da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dei suggerimenti

        Returns:
            Un'istanza di Suggestions
        """
        tag_suggestions = [VideoTagSuggestion.from_dict(ts) for ts in param.get('tagSuggestions', [])]

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
class VideoLiveStreamingDetails:
    actualStartTime: Optional[datetime] = None
    actualEndTime: Optional[datetime] = None
    scheduledStartTime: Optional[datetime] = None
    scheduledEndTime: Optional[datetime] = None
    concurrentViewers: int = 0
    activeLiveChatId: str = ""

    @classmethod
    def from_dict(cls, param: dict) -> 'VideoLiveStreamingDetails':
        """
        Crea un oggetto LiveStreamingDetails da un dizionario JSON.

        Args:
            param: Dizionario contenente i dati dei dettagli dello streaming live

        Returns:
            Un'istanza di LiveStreamingDetails
        """
        return cls(
            actualStartTime=parse_iso_datetime(param.get('actualStartTime', None)),
            actualEndTime=parse_iso_datetime(param.get('actualEndTime', None)),
            scheduledStartTime=parse_iso_datetime(param.get('scheduledStartTime', None)),
            scheduledEndTime=parse_iso_datetime(param.get('scheduledEndTime', None)),
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
            publishedAt=parse_iso_datetime(data.get('publishedAt', None)),
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
    contentDetails: VideoContentDetails = field(default_factory=VideoContentDetails)
    status: VideoStatus = field(default_factory=VideoStatus)
    statistics: VideoStatistics = field(default_factory=VideoStatistics)
    paidProductPlacementDetails: VideoPaidProductPlacementDetails = field(
        default_factory=VideoPaidProductPlacementDetails)
    player: VideoPlayer = field(default_factory=VideoPlayer)
    topicDetails: VideoTopicDetails = field(default_factory=VideoTopicDetails)
    recordingDetails: VideoRecordingDetails = field(default_factory=VideoRecordingDetails)
    fileDetails: VideoFileDetails = field(default_factory=VideoFileDetails)
    processingDetails: VideoProcessingDetails = field(default_factory=VideoProcessingDetails)
    suggestions: VideoSuggestions = field(default_factory=VideoSuggestions)
    liveStreamingDetails: VideoLiveStreamingDetails = field(default_factory=VideoLiveStreamingDetails)
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
        content_details = VideoContentDetails.from_dict(data.get('contentDetails', {}))
        status = VideoStatus.from_dict(data.get('status', {}))
        statistics = VideoStatistics.from_dict(data.get('statistics', {}))
        paid_product_placement_details = VideoPaidProductPlacementDetails.from_dict(
            data.get('paidProductPlacementDetails', {}))
        player = VideoPlayer.from_dict(data.get('player', {}))
        topic_details = VideoTopicDetails.from_dict(data.get('topicDetails', {}))
        recording_details = VideoRecordingDetails.from_dict(data.get('recordingDetails', {}))
        file_details = VideoFileDetails.from_dict(data.get('fileDetails', {}))
        processing_details = VideoProcessingDetails.from_dict(data.get('processingDetails', {}))
        suggestions = VideoSuggestions.from_dict(data.get('suggestions', {}))
        live_streaming_details = VideoLiveStreamingDetails.from_dict(data.get('liveStreamingDetails', {}))

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

    def to_dict(self):
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati della risorsa video.
        """
        return {
            'kind': self.kind,
            'etag': self.etag,
            'id': self.id,
            'snippet': self.snippet.to_dict(),
            'contentDetails': self.contentDetails.to_dict(),
            'status': self.status.to_dict(),
            'statistics': self.statistics.to_dict(),
            'paidProductPlacementDetails': self.paidProductPlacementDetails.to_dict(),
            'player': self.player.to_dict(),
            'topicDetails': self.topicDetails.to_dict(),
            'recordingDetails': self.recordingDetails.to_dict(),
            'fileDetails': self.fileDetails.to_dict(),
            'processingDetails': self.processingDetails.to_dict(),
            'suggestions': self.suggestions.to_dict(),
            'liveStreamingDetails': self.liveStreamingDetails.to_dict(),
            'localizations': {lang: loc.to_dict() for lang, loc in self.localizations.items()}
        }


@dataclass
class YouTubeVideoListResponse:
    kind: str = "youtube#videoListResponse"
    etag: str = ""
    nextPageToken: Optional[str] = None
    prevPageToken: Optional[str] = None
    pageInfo: PageInfo = field(default_factory=PageInfo)
    items: List[VideoResource] = field(default_factory=list[VideoResource])

    @classmethod
    def from_dict(cls, data: dict) -> 'YouTubeVideoListResponse':
        """
        Crea un oggetto YouTubeVideoListResponse da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati della risposta della lista video

        Returns:
            Un'istanza di YouTubeVideoListResponse
        """
        kind = data.get('kind', '')
        if kind != 'youtube#videoListResponse':
            raise ValueError(f"Expected kind='youtube#videoListResponse', got '{kind}'")

        items_data = data.get('items', [])
        items = [VideoResource.from_dict(item) for item in items_data]

        return cls(
            kind=kind,
            etag=data.get('etag', ''),
            pageInfo=PageInfo.from_dict(data.get('pageInfo', {})),
            items=items,
            nextPageToken=data.get('nextPageToken'),
            prevPageToken=data.get('prevPageToken')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati della risposta della lista video.
        """
        return {
            'kind': self.kind,
            'etag': self.etag,
            'pageInfo': self.pageInfo.to_dict(),
            'items': [item.to_dict() for item in self.items],
            'nextPageToken': self.nextPageToken,
            'prevPageToken': self.prevPageToken,
        }


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
            publishedAt=parse_iso_datetime(data.get('publishedAt', None)),
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
            'pageInfo': self.pageInfo.to_dict(),
            'items': [item.to_dict() for item in self.items]
        }


@dataclass
class ChannelResourceSnippet:
    title: str = ""
    description: str = ""
    customUrl: str = ""
    publishedAt: Optional[datetime] = None
    thumbnails: Thumbnails = field(default_factory=Thumbnails)
    defaultLanguage: str = ""
    localized: Localized = field(default_factory=Localized)
    country: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> 'ChannelResourceSnippet':
        """
        Crea un oggetto ChannelResourceSnippet da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati dello snippet della risorsa canale

        Returns:
            Un'istanza di ChannelResourceSnippet
        """
        thumbnails = Thumbnails.from_dict(data.get('thumbnails', {}))
        localized = Localized.from_dict(data.get('localized', {}))

        return cls(
            title=data.get('title', ''),
            description=data.get('description', ''),
            customUrl=data.get('customUrl', ''),
            publishedAt=parse_iso_datetime(data.get('publishedAt', None)),
            thumbnails=thumbnails,
            defaultLanguage=data.get('defaultLanguage', ''),
            localized=localized,
            country=data.get('country', '')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dello snippet della risorsa canale.
        """
        return {
            'title': self.title,
            'description': self.description,
            'customUrl': self.customUrl,
            'publishedAt': self.publishedAt.isoformat() if self.publishedAt else None,
            'thumbnails': self.thumbnails.to_dict(),
            'defaultLanguage': self.defaultLanguage,
            'localized': self.localized.to_dict(),
            'country': self.country
        }


@dataclass
class RelatedPlaylists:
    likes: str = ""
    favorites: str = ""
    uploads: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> 'RelatedPlaylists':
        """
        Crea un oggetto RelatedPlaylists da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati delle playlist correlate

        Returns:
            Un'istanza di RelatedPlaylists
        """
        return cls(
            likes=data.get('likes', ''),
            favorites=data.get('favorites', ''),
            uploads=data.get('uploads', '')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati delle playlist correlate.
        """
        return {
            'likes': self.likes,
            'favorites': self.favorites,
            'uploads': self.uploads
        }


@dataclass
class ChannelContentDetails:
    relatedPlaylists: RelatedPlaylists = field(default_factory=RelatedPlaylists)

    @classmethod
    def from_dict(cls, data: dict) -> 'ChannelContentDetails':
        """
        Crea un oggetto ChannelContentDetails da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati dei dettagli del contenuto del canale

        Returns:
            Un'istanza di ChannelContentDetails
        """
        related_playlists = RelatedPlaylists.from_dict(data.get('relatedPlaylists', {}))
        return cls(relatedPlaylists=related_playlists)

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei dettagli del contenuto del canale.
        """
        return {
            'relatedPlaylists': self.relatedPlaylists.to_dict()
        }


@dataclass
class ChannelStatistics:
    viewCount: int = 0
    subscriberCount: int = 0
    hiddenSubscriberCount: bool = False
    videoCount: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> 'ChannelStatistics':
        """
        Crea un oggetto ChannelStatistics da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati delle statistiche del canale

        Returns:
            Un'istanza di ChannelStatistics
        """
        return cls(
            viewCount=data.get('viewCount', 0),
            subscriberCount=data.get('subscriberCount', 0),
            hiddenSubscriberCount=data.get('hiddenSubscriberCount', False),
            videoCount=data.get('videoCount', 0)
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati delle statistiche del canale.
        """
        return {
            'viewCount': self.viewCount,
            'subscriberCount': self.subscriberCount,
            'hiddenSubscriberCount': self.hiddenSubscriberCount,
            'videoCount': self.videoCount
        }


@dataclass
class ChannelTopicDetails:
    topicIds: List[str] = field(default_factory=list)
    topicCategories: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'ChannelTopicDetails':
        """
        Crea un oggetto TopicDetails da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati dei dettagli del topic

        Returns:
            Un'istanza di TopicDetails
        """
        return cls(
            topicIds=data.get('topicIds', []),
            topicCategories=data.get('topicCategories', [])
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei dettagli del topic.
        """
        return {
            'topicIds': self.topicIds,
            'topicCategories': self.topicCategories
        }


@dataclass
class ChannelStatus:
    privacyStatus: str = ""
    isLinked: bool = False
    longUploadsStatus: str = ""
    madeForKids: bool = False
    selfDeclaredMadeForKids: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> 'ChannelStatus':
        """
        Crea un oggetto ChannelStatus da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati dello stato del canale

        Returns:
            Un'istanza di ChannelStatus
        """
        return cls(
            privacyStatus=data.get('privacyStatus', ''),
            isLinked=data.get('isLinked', False),
            longUploadsStatus=data.get('longUploadsStatus', ''),
            madeForKids=data.get('madeForKids', False),
            selfDeclaredMadeForKids=data.get('selfDeclaredMadeForKids', False)
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dello stato del canale.
        """
        return {
            'privacyStatus': self.privacyStatus,
            'isLinked': self.isLinked,
            'longUploadsStatus': self.longUploadsStatus,
            'madeForKids': self.madeForKids,
            'selfDeclaredMadeForKids': self.selfDeclaredMadeForKids
        }


@dataclass
class BrandingSettingsChannel:
    title: str = ""
    description: str = ""
    keywords: str = ""
    trackingAnalyticsAccountId: str = ""
    unsubscribedTrailer: str = ""
    defaultLanguage: str = ""
    country: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> 'BrandingSettingsChannel':
        """
        Crea un oggetto BrandingSettingsChannel da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati delle impostazioni di branding del canale

        Returns:
            Un'istanza di BrandingSettingsChannel
        """
        return cls(
            title=data.get('title', ''),
            description=data.get('description', ''),
            keywords=data.get('keywords', ''),
            trackingAnalyticsAccountId=data.get('trackingAnalyticsAccountId', ''),
            unsubscribedTrailer=data.get('unsubscribedTrailer', ''),
            defaultLanguage=data.get('defaultLanguage', ''),
            country=data.get('country', '')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati delle impostazioni di branding del canale.
        """
        return {
            'title': self.title,
            'description': self.description,
            'keywords': self.keywords,
            'trackingAnalyticsAccountId': self.trackingAnalyticsAccountId,
            'unsubscribedTrailer': self.unsubscribedTrailer,
            'defaultLanguage': self.defaultLanguage,
            'country': self.country
        }


@dataclass
class BrandingSettingsWatch:
    textColor: str = ""
    backgroundColor: str = ""
    featuredPlaylistId: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> 'BrandingSettingsWatch':
        """
        Crea un oggetto BrandingSettingsWatch da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati delle impostazioni di branding della visualizzazione

        Returns:
            Un'istanza di BrandingSettingsWatch
        """
        return cls(
            textColor=data.get('textColor', ''),
            backgroundColor=data.get('backgroundColor', ''),
            featuredPlaylistId=data.get('featuredPlaylistId', '')
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati delle impostazioni di branding della visualizzazione.
        """
        return {
            'textColor': self.textColor,
            'backgroundColor': self.backgroundColor,
            'featuredPlaylistId': self.featuredPlaylistId
        }


@dataclass
class ChannelBrandingSettings:
    channel: BrandingSettingsChannel = field(default_factory=BrandingSettingsChannel)
    watch: BrandingSettingsWatch = field(default_factory=BrandingSettingsWatch)

    @classmethod
    def from_dict(cls, data: dict) -> 'ChannelBrandingSettings':
        """
        Crea un oggetto BrandingSettings da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati delle impostazioni di branding

        Returns:
            Un'istanza di BrandingSettings
        """
        channel = BrandingSettingsChannel.from_dict(data.get('channel', {}))
        watch = BrandingSettingsWatch.from_dict(data.get('watch', {}))

        return cls(channel=channel, watch=watch)

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati delle impostazioni di branding.
        """
        return {
            'channel': self.channel.to_dict(),
            'watch': self.watch.to_dict()
        }


@dataclass
class ChannelAuditDetails:
    overallGoodStanding: bool = False
    communityGuidelinesGoodStanding: bool = False
    copyrightStrikesGoodStanding: bool = False
    contentIdClaimsGoodStanding: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> 'ChannelAuditDetails':
        """
        Crea un oggetto AuditDetails da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati degli audit

        Returns:
            Un'istanza di AuditDetails
        """
        return cls(
            overallGoodStanding=data.get('overallGoodStanding', False),
            communityGuidelinesGoodStanding=data.get('communityGuidelinesGoodStanding', False),
            copyrightStrikesGoodStanding=data.get('copyrightStrikesGoodStanding', False),
            contentIdClaimsGoodStanding=data.get('contentIdClaimsGoodStanding', False)
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati degli audit.
        """
        return {
            'overallGoodStanding': self.overallGoodStanding,
            'communityGuidelinesGoodStanding': self.communityGuidelinesGoodStanding,
            'copyrightStrikesGoodStanding': self.copyrightStrikesGoodStanding,
            'contentIdClaimsGoodStanding': self.contentIdClaimsGoodStanding
        }


@dataclass
class ChannelContentOwnerDetails:
    contentOwner: str = ""
    timeLinked: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'ChannelContentOwnerDetails':
        """
        Crea un oggetto ContentOwnerDetails da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati dei dettagli del proprietario del contenuto

        Returns:
            Un'istanza di ContentOwnerDetails
        """
        return cls(
            contentOwner=data.get('contentOwner', ''),
            timeLinked=parse_iso_datetime(data.get('timeLinked', None))
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati dei dettagli del proprietario del contenuto.
        """
        return {
            'contentOwner': self.contentOwner,
            'timeLinked': self.timeLinked.isoformat() if self.timeLinked else None
        }


@dataclass
class ChannelResource:
    kind: str = "youtube#channel"
    etag: str = ""
    id: str = ""
    snippet: ChannelResourceSnippet = field(default_factory=ChannelResourceSnippet)
    contentDetails: ChannelContentDetails = field(default_factory=ChannelContentDetails)
    statistics: ChannelStatistics = field(default_factory=ChannelStatistics)
    topicDetails: ChannelTopicDetails = field(default_factory=ChannelTopicDetails)
    status: ChannelStatus = field(default_factory=ChannelStatus)
    brandingSettings: ChannelBrandingSettings = field(default_factory=ChannelBrandingSettings)
    auditDetails: ChannelAuditDetails = field(default_factory=ChannelAuditDetails)
    contentOwnerDetails: ChannelContentOwnerDetails = field(default_factory=ChannelContentOwnerDetails)
    localizations: Dict[str, Localized] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> 'ChannelResource':
        """
        Crea un oggetto ChannelResource da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati della risorsa canale

        Returns:
            Un'istanza di ChannelResource
        """
        kind_received = data.get('kind', '')
        if kind_received != 'youtube#channel':
            raise ValueError(f"Expected kind='youtube#channel', got '{kind_received}'")

        snippet = ChannelResourceSnippet.from_dict(data.get('snippet', {}))
        content_details = ChannelContentDetails.from_dict(data.get('contentDetails', {}))
        statistics = ChannelStatistics.from_dict(data.get('statistics', {}))
        topic_details = ChannelTopicDetails.from_dict(data.get('topicDetails', {}))
        status = ChannelStatus.from_dict(data.get('status', {}))
        branding_settings = ChannelBrandingSettings.from_dict(data.get('brandingSettings', {}))
        audit_details = ChannelAuditDetails.from_dict(data.get('auditDetails', {}))
        content_owner_details = ChannelContentOwnerDetails.from_dict(data.get('contentOwnerDetails', {}))

        localizations_data = data.get('localizations', {})
        localizations = {lang: Localized.from_dict(loc) for lang, loc in localizations_data.items()}

        return cls(
            kind=kind_received,
            etag=data.get('etag', ''),
            id=data.get('id', ''),
            snippet=snippet,
            contentDetails=content_details,
            statistics=statistics,
            topicDetails=topic_details,
            status=status,
            brandingSettings=branding_settings,
            auditDetails=audit_details,
            contentOwnerDetails=content_owner_details,
            localizations=localizations
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati della risorsa canale.
        """
        return {
            'kind': self.kind,
            'etag': self.etag,
            'id': self.id,
            'snippet': self.snippet.to_dict(),
            'contentDetails': self.contentDetails.to_dict(),
            'statistics': self.statistics.to_dict(),
            'topicDetails': self.topicDetails.to_dict(),
            'status': self.status.to_dict(),
            'brandingSettings': self.brandingSettings.to_dict(),
            'auditDetails': self.auditDetails.to_dict(),
            'contentOwnerDetails': self.contentOwnerDetails.to_dict(),
            'localizations': {lang: loc.to_dict() for lang, loc in self.localizations.items()}
        }


@dataclass
class YouTubeChannelListResponse:
    kind: str = "youtube#channelListResponse"
    etag: str = ""
    nextPageToken: Optional[str] = None
    prevPageToken: Optional[str] = None
    pageInfo: PageInfo = field(default_factory=PageInfo)
    items: List[ChannelResource] = field(default_factory=ChannelResource)

    @classmethod
    def from_dict(cls, data: dict) -> 'YouTubeChannelListResponse':
        """
        Crea un oggetto YouTubeChannelListResponse da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati della risposta della lista canali di YouTube

        Returns:
            Un'istanza di YouTubeChannelListResponse
        """
        kind_received = data.get('kind', '')
        if kind_received != 'youtube#channelListResponse':
            raise ValueError(f"Expected kind='youtube#channelListResponse', got '{kind_received}'")

        page_info = PageInfo.from_dict(data.get('pageInfo', {}))

        items = [ChannelResource.from_dict(item_data) for item_data in data.get('items', [])]

        return cls(
            kind=kind_received,
            etag=data.get('etag', ''),
            nextPageToken=data.get('nextPageToken'),
            prevPageToken=data.get('prevPageToken'),
            pageInfo=page_info,
            items=items
        )

    def to_dict(self) -> dict:
        """
        Converte l'istanza in un dizionario JSON.

        Returns:
            Un dizionario contenente i dati della risposta della lista canali di YouTube.
        """
        return {
            'kind': self.kind,
            'etag': self.etag,
            'nextPageToken': self.nextPageToken,
            'prevPageToken': self.prevPageToken,
            'pageInfo': self.pageInfo.to_dict(),
            'items': [item.to_dict() for item in self.items]
        }

from datetime import datetime
from dataclasses import dataclass, field
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

@dataclass
class VideoResourceSnippet:
    published_at: Optional[datetime] = None
    channel_id: str = ""
    title: str = ""
    description: str = ""
    thumbnails: Thumbnails = field(default_factory=Thumbnails)
    channel_title: str = ""
    tags: List[str] = field(default_factory=list)
    category_id: str = ""
    live_broadcast_content: str = ""
    default_language: str = ""
    localized: Localized = field(default_factory=Localized)
    default_audio_language: str = ""

@dataclass
class RegionRestriction:
    allowed: List[str] = field(default_factory=list)
    blocked: List[str] = field(default_factory=list)

@dataclass
class ContentRating:
    # Includo solo alcuni campi rappresentativi
    acb_rating: str = ""
    mpaa_rating: str = ""
    yt_rating: str = ""
    # Aggiungere gli altri rating secondo necessità

@dataclass
class ContentDetails:
    duration: str = ""
    dimension: str = ""
    definition: str = ""
    caption: str = ""
    licensed_content: bool = False
    region_restriction: RegionRestriction = field(default_factory=RegionRestriction)
    content_rating: ContentRating = field(default_factory=ContentRating)
    projection: str = ""
    has_custom_thumbnail: bool = False

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

@dataclass
class Statistics:
    view_count: str = "0"
    like_count: str = "0"
    dislike_count: str = "0"
    favorite_count: str = "0"
    comment_count: str = "0"

@dataclass
class PaidProductPlacementDetails:
    has_paid_product_placement: bool = False

@dataclass
class Player:
    embed_html: str = ""
    embed_height: int = 0
    embed_width: int = 0

@dataclass
class TopicDetails:
    topic_ids: List[str] = field(default_factory=list)
    relevant_topic_ids: List[str] = field(default_factory=list)
    topic_categories: List[str] = field(default_factory=list)

@dataclass
class RecordingDetails:
    recording_date: Optional[datetime] = None

@dataclass
class VideoStream:
    width_pixels: int = 0
    height_pixels: int = 0
    frame_rate_fps: float = 0.0
    aspect_ratio: float = 0.0
    codec: str = ""
    bitrate_bps: int = 0
    rotation: str = ""
    vendor: str = ""

@dataclass
class AudioStream:
    channel_count: int = 0
    codec: str = ""
    bitrate_bps: int = 0
    vendor: str = ""

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

@dataclass
class ProcessingProgress:
    parts_total: int = 0
    parts_processed: int = 0
    time_left_ms: int = 0

@dataclass
class ProcessingDetails:
    processing_status: str = ""
    processing_progress: ProcessingProgress = field(default_factory=ProcessingProgress)
    processing_failure_reason: str = ""
    file_details_availability: str = ""
    processing_issues_availability: str = ""
    tag_suggestions_availability: str = ""
    editor_suggestions_availability: str = ""
    thumbnails_availability: str = ""

@dataclass
class TagSuggestion:
    tag: str = ""
    category_restricts: List[str] = field(default_factory=list)

@dataclass
class Suggestions:
    processing_errors: List[str] = field(default_factory=list)
    processing_warnings: List[str] = field(default_factory=list)
    processing_hints: List[str] = field(default_factory=list)
    tag_suggestions: List[TagSuggestion] = field(default_factory=list)
    editor_suggestions: List[str] = field(default_factory=list)

@dataclass
class LiveStreamingDetails:
    actual_start_time: Optional[datetime] = None
    actual_end_time: Optional[datetime] = None
    scheduled_start_time: Optional[datetime] = None
    scheduled_end_time: Optional[datetime] = None
    concurrent_viewers: int = 0
    active_live_chat_id: str = ""

@dataclass
class YouTubeVideoResource:
    kind: str = "youtube#video"
    etag: str = ""
    id: str = ""
    snippet: VideoResourceSnippet = field(default_factory=VideoResourceSnippet)
    content_details: ContentDetails = field(default_factory=ContentDetails)
    status: Status = field(default_factory=Status)
    statistics: Statistics = field(default_factory=Statistics)
    paid_product_placement_details: PaidProductPlacementDetails = field(default_factory=PaidProductPlacementDetails)
    player: Player = field(default_factory=Player)
    topic_details: TopicDetails = field(default_factory=TopicDetails)
    recording_details: RecordingDetails = field(default_factory=RecordingDetails)
    file_details: FileDetails = field(default_factory=FileDetails)
    processing_details: ProcessingDetails = field(default_factory=ProcessingDetails)
    suggestions: Suggestions = field(default_factory=Suggestions)
    live_streaming_details: LiveStreamingDetails = field(default_factory=LiveStreamingDetails)
    localizations: Dict[str, Localized] = field(default_factory=dict)

@dataclass
class YouTubeSearchResourceId:
    kind: str = ""
    videoId: str = ""
    channelId: str = ""
    playlistId: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> 'YouTubeSearchResourceId':
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
class YoutubeSearchResource:
    kind: str = "youtube#searchResult"
    etag: str = ""
    id: YouTubeSearchResourceId = field(default_factory=YouTubeSearchResourceId)
    snippet: SearchResourceSnippet = field(default_factory=SearchResourceSnippet)

    @classmethod
    def from_dict(cls, data: dict) -> 'YoutubeSearchResource':
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

        resource_id = YouTubeSearchResourceId.from_dict(data.get('id', {}))
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
    items: List[YoutubeSearchResource] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'YouTubeSearchListResponse':
        """
        Crea un oggetto YouTubeSearchListResponse da un dizionario JSON.

        Args:
            data: Dizionario contenente i dati della risposta di ricerca di YouTube

        Returns:
            Un'istanza di YouTubeSearchListResponse
        """
        # Utilizzo from_dict per PageInfo
        page_info = PageInfo.from_dict(data.get('pageInfo', {}))

        # Elabora gli elementi
        items = []
        for item_data in data.get('items', []):
            # Utilizza from_dict per YoutubeSearchResource
            search_item = YoutubeSearchResource.from_dict(item_data)
            items.append(search_item)

        # Crea e restituisce l'oggetto di risposta
        return cls(
            kind=data.get('kind', 'youtube#searchListResponse'),
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
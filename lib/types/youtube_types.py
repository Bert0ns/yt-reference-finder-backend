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

@dataclass
class Thumbnails:
    default: Optional[Thumbnail] = None
    medium: Optional[Thumbnail] = None
    high: Optional[Thumbnail] = None
    standard: Optional[Thumbnail] = None
    maxres: Optional[Thumbnail] = None

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

@dataclass
class SearchResourceSnippet:
    published_at: Optional[datetime] = None
    channel_id: str = ""
    title: str = ""
    description: str = ""
    thumbnails: Thumbnails = field(default_factory=Thumbnails)
    channel_title: str = ""
    live_broadcast_content: str = ""

@dataclass
class YoutubeSearchResource:
    kind: str = "youtube#searchResult"
    etag: str = ""
    id: YouTubeSearchResourceId = field(default_factory=YouTubeSearchResourceId)
    snippet: VideoResourceSnippet = field(default_factory=SearchResourceSnippet)

@dataclass
class PageInfo:
    total_results: int = 0
    results_per_page: int = 0

@dataclass
class YouTubeSearchListResponse:
    kind: str = "youtube#searchListResponse"
    etag: str = ""
    next_page_token: Optional[str] = None
    prev_page_token: Optional[str] = None
    region_code: Optional[str] = None
    page_info: PageInfo = field(default_factory=PageInfo)
    items: List[YoutubeSearchResource] = field(default_factory=list)
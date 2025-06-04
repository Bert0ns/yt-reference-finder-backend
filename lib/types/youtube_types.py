from dataclasses import dataclass

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
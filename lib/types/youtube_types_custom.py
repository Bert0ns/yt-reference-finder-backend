from dataclasses import dataclass, field

from lib.types.youtube_types import Thumbnails, Thumbnail


@dataclass
class VideoStatistics:
    like_count: int = 0
    view_count: int = 0


@dataclass
class ChannelInfo:
    subscriber_count: int = 0
    language: str = ""

@dataclass
class VideoPartialData:
    title: str
    description: str
    video_id: str
    url: str
    channel_id: str
    thumbnails: Thumbnails = field(default_factory=Thumbnails)

    def get_thumbnail_url(self, definition: str = "high") -> str:
        """
        Returns the thumbnail URL for the specified size.
        """
        all_definitions_thumbnails = self.thumbnails.to_dict().keys()
        if definition not in all_definitions_thumbnails:
            definition = all_definitions_thumbnails[0]

        return Thumbnail.from_dict(self.thumbnails.to_dict()[definition]).url


@dataclass
class Video(VideoPartialData):
    channel_subscribers: int = 0
    like_count: int = 0
    view_count: int = 0
    engagement_score: float = 0.0
    relevance_score: float = 0.0

    def to_dict(self) -> dict:
        """
        Converts the Video object to a dictionary.
        """
        return {
            "title": self.title,
            "description": self.description,
            "video_id": self.video_id,
            "url": self.url,
            "channel_id": self.channel_id,
            "thumbnails": self.thumbnails.to_dict(),
            "channel_subscribers": self.channel_subscribers,
            "like_count": self.like_count,
            "view_count": self.view_count,
            "engagement_score": self.engagement_score,
            "relevance_score": self.relevance_score
        }



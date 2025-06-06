import json
from dataclasses import dataclass
from enum import Enum
from typing import List
from lib.youtube_interactions import Video


class StreamProcessStatus(Enum):
    ERROR = 'error'
    FILE_RECEIVED = 'file_received'
    FILE_PROCESSED = 'file_processed'
    EXTRACTING_KEYWORDS = 'extracting_keywords'
    KEYWORDS_EXTRACTED = 'keywords_extracted'
    GENERATING_QUERIES = 'generating_queries'
    QUERIES_GENERATED = 'queries_generated'
    YOUTUBE_SEARCH_STARTED = 'youtube_search_started'
    YOUTUBE_SEARCH_COMPLETED = 'youtube_search_completed'
    PROCESSING_COMPLETE = 'processing_complete'



@dataclass
class StreamResponse:
    status: str
    message: str = ""
    keywords: list[str] = None
    queries: list[str] = None
    videos: List[Video] = None

    def __init__(self, status: StreamProcessStatus, message: str = "", keywords: list[tuple[str, float]] = None,
                 queries: list[str] = None, videos: list[Video] = None, **kwargs):
        if keywords is None:
            keywords = []
        if queries is None:
            queries = []
        if videos is None:
            videos = []

        self.status = status.value
        self.message = message
        self.keywords = [kw for kw, _ in keywords]
        self.queries = queries
        self.videos = videos

        if status is StreamProcessStatus.ERROR and not message:
            raise ValueError("Stream Response Error status requires a message")

        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        """
        Converts the StreamResponse object to a dictionary.
        """
        return {
            "status": self.status,
            "message": self.message,
            "keywords": self.keywords,
            "queries": self.queries,
            "videos": [video.to_dict() for video in self.videos] if self.videos else []
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict()) + '\n'
import json
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


class StreamResponse:
    def __init__(self, status: StreamProcessStatus, message: str = "", keywords: List[tuple[str, float]] = None,
                 queries: List[str] = None, videos: List[Video] = None, **kwargs):
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
        self.videos = [video.__dict__ for video in videos]

        if status is StreamProcessStatus.ERROR and not message:
            raise ValueError("Stream Response Error status requires a message")

        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self) -> str:
        return json.dumps(self.__dict__) + '\n'
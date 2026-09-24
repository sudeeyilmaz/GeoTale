from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from datetime import datetime

class MediaAsset(ABC):
    #For all media types
    def __init__(self, file_path: str, filename: str):
        self.file_path = file_path
        self.filename = filename
        self.timestamp: Optional[datetime] = None
        self.location: Optional[Dict[str, Any]] = None
        self.tags: List[str] = []

    @abstractmethod
    def extract_metadata(self) -> dict:
        pass

class PhotoAsset(MediaAsset):
    #for only photos
    def extract_metadata(self) -> dict:
        print(f"Extracting metadata for{self.filename}")
        self.location = { "lat": 0.0,"lon":0.0}
        self.timestamp = datetime.now()
        return {
            "file_path": self.file_path,
            "filename": self.filename,
            "timestamp": self.timestamp,
            "location": self.location
        }

class VideoAsset(MediaAsset):
    #for only videos
    def extract_metadata(self) -> dict:
        print(f"Extracting metadata for{self.filename}")
        self.location = { "lat": 0.0,"lon":0.0}
        self.timestamp = datetime.now()
        return {
            "file_path": self.file_path,
            "filename": self.filename,
            "timestamp": self.timestamp,
            "location": self.location
        }
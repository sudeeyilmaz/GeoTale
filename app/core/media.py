from ast import List
from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

class MediaAsset(ABC):
    #For all media types
    def __init__(self,file_path:str,filename:str):
        self.file_path = file_path
        self.filename = filename
        self.timestamp: Optional[datetime]= None
        self.location = Optional[dict] = None
        self.tags: List = []

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
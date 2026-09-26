from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class LocationSchema(BaseModel):
    lat: float = Field(..., description="Latitude (Enlem)")
    lon: float = Field(..., description="Longitude (Boylam)")
    altitude: Optional[float] = Field(None, description="Rakım (metre)")

class MediaProcessResponse(BaseModel):
    message: str
    filename: str
    timestamp: Optional[datetime] = None
    location: Optional[LocationSchema] = None
    tags: List[str] = []

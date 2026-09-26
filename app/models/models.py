import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Text, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
    media = relationship("MediaItem", back_populates="user", cascade="all, delete-orphan")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    cover_image_url = Column(String(500), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="trips")
    pins = relationship("Pin", back_populates="trip", cascade="all, delete-orphan", order_by="Pin.visited_at")
    media = relationship("MediaItem", back_populates="trip")


class Pin(Base):
    __tablename__ = "pins"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id = Column(String, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = Column(String(255), nullable=True)
    story_text = Column(Text, nullable=True)
    place_name = Column(String(255), nullable=True) # Örn: "Karaköy Güllüoğlu, İstanbul"
    
    # Coğrafi Koordinatlar (WGS84)
    lat = Column(Float, nullable=False, index=True)
    lon = Column(Float, nullable=False, index=True)
    altitude = Column(Float, nullable=True)
    
    visited_at = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    trip = relationship("Trip", back_populates="pins")
    media = relationship("MediaItem", back_populates="pin")


class MediaItem(Base):
    __tablename__ = "media_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    trip_id = Column(String, ForeignKey("trips.id", ondelete="SET NULL"), nullable=True, index=True)
    pin_id = Column(String, ForeignKey("pins.id", ondelete="SET NULL"), nullable=True, index=True)
    
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_url = Column(String(500), nullable=True)
    
    # EXIF & Konum
    timestamp = Column(DateTime, nullable=True, index=True)
    lat = Column(Float, nullable=True, index=True)
    lon = Column(Float, nullable=True, index=True)
    altitude = Column(Float, nullable=True)
    
    # Etiketler & AI Analizi
    tags = Column(JSON, default=list) # ["outdoor", "city", "coffee"]
    
    # pgvector: Semantik arama / Görsel embedding (Örn: CLIP 512-dim vektör)
    embedding = Column(Vector(512), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="media")
    trip = relationship("Trip", back_populates="media")
    pin = relationship("Pin", back_populates="media")

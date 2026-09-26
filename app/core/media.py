from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from datetime import datetime
import os
from PIL import Image, ExifTags

class MediaAsset(ABC):
    # For all media types
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
    # For photos (JPEG, PNG, WEBP, etc.)
    
    @staticmethod
    def _dms_to_decimal(dms_tuple, reference: str) -> Optional[float]:
        """Convert degrees, minutes, seconds tuple to decimal degrees."""
        if not dms_tuple or len(dms_tuple) < 3:
            return None
        try:
            degrees = float(dms_tuple[0])
            minutes = float(dms_tuple[1])
            seconds = float(dms_tuple[2])
            decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
            if reference in ["S", "W"]:
                decimal = -decimal
            return round(decimal, 6)
        except (TypeError, ValueError, ZeroDivisionError):
            return None

    def extract_metadata(self) -> dict:
        print(f"Extracting metadata for {self.filename}")
        lat = None
        lon = None
        altitude = None
        extracted_time = None

        try:
            with Image.open(self.file_path) as img:
                exif = img.getexif()
                if exif:
                    # 1. GPS Bilgilerini Çıkarma
                    gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
                    if gps_ifd:
                        gps_lat = gps_ifd.get(ExifTags.GPS.GPSLatitude.value)
                        gps_lat_ref = gps_ifd.get(ExifTags.GPS.GPSLatitudeRef.value, "N")
                        gps_lon = gps_ifd.get(ExifTags.GPS.GPSLongitude.value)
                        gps_lon_ref = gps_ifd.get(ExifTags.GPS.GPSLongitudeRef.value, "E")
                        gps_alt = gps_ifd.get(ExifTags.GPS.GPSAltitude.value)

                        if gps_lat and gps_lon:
                            lat = self._dms_to_decimal(gps_lat, gps_lat_ref)
                            lon = self._dms_to_decimal(gps_lon, gps_lon_ref)
                        
                        if gps_alt is not None:
                            try:
                                altitude = float(gps_alt)
                            except (TypeError, ValueError):
                                altitude = None

                    # 2. Tarih / Saat Bilgisini Çıkarma
                    exif_ifd = exif.get_ifd(ExifTags.IFD.Exif)
                    date_str = (
                        exif_ifd.get(ExifTags.Base.DateTimeOriginal.value)
                        or exif_ifd.get(ExifTags.Base.DateTimeDigitized.value)
                        or exif.get(ExifTags.Base.DateTime.value)
                    )
                    
                    if date_str:
                        for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
                            try:
                                extracted_time = datetime.strptime(str(date_str).strip(), fmt)
                                break
                            except ValueError:
                                continue
        except Exception as e:
            print(f"EXIF okuma hatası ({self.filename}): {e}")

        # Eğer GPS verisi bulunduysa location objesi oluştur
        if lat is not None and lon is not None:
            self.location = {
                "lat": lat,
                "lon": lon,
                "altitude": altitude
            }
        else:
            self.location = None

        # Tarih bulunamadıysa dosyanın oluşturulma/değiştirilme zamanını fallback olarak al
        if extracted_time:
            self.timestamp = extracted_time
        else:
            try:
                mtime = os.path.getmtime(self.file_path)
                self.timestamp = datetime.fromtimestamp(mtime)
            except Exception:
                self.timestamp = datetime.now()

        return {
            "file_path": self.file_path,
            "filename": self.filename,
            "timestamp": self.timestamp,
            "location": self.location
        }

class VideoAsset(MediaAsset):
    # For videos (MP4, MOV, etc.)
    def extract_metadata(self) -> dict:
        print(f"Extracting metadata for {self.filename}")
        self.location = None
        try:
            mtime = os.path.getmtime(self.file_path)
            self.timestamp = datetime.fromtimestamp(mtime)
        except Exception:
            self.timestamp = datetime.now()
            
        return {
            "file_path": self.file_path,
            "filename": self.filename,
            "timestamp": self.timestamp,
            "location": self.location
        }
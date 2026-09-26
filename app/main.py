from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import os

from app.core.config import settings
from app.core.database import init_db, get_db
from app.core.pipeline import MediaPipeline, MetadataExtractorNode, AIAnalyzerNode
from app.core.media import PhotoAsset
from app.schemas.media_schema import MediaProcessResponse
import app.models # Modellerin Base.metadata'ya kaydolması için

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Uygulama başlarken DB ve tabloları hazırla
    try:
        init_db()
    except Exception as e:
        print(f"Database connection warning: {e}")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Geo-aware media processing & travel story engine with pgvector",
    version=settings.VERSION,
    lifespan=lifespan
)

pipeline = MediaPipeline()
pipeline.add_node(MetadataExtractorNode())
pipeline.add_node(AIAnalyzerNode())

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/v1/process-media", response_model=MediaProcessResponse)
async def process_media(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    asset = PhotoAsset(file_path=file_path, filename=file.filename) 
    processed_asset = pipeline.execute(asset)

    return {
        "message": "success",
        "filename": processed_asset.filename,
        "tags": processed_asset.tags,
        "timestamp": processed_asset.timestamp,
        "location": processed_asset.location
    }
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
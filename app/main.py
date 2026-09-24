from fastapi import FastAPI, UploadFile,File
from app.core.pipeline import MediaPipeline,MetadataExtractorNode,AIAnalyzerNode
from app.core.media import MediaAsset,PhotoAsset
import shutil
import os

app = FastAPI(title="GeoTale Media Services")

pipeline = MediaPipeline()
pipeline.add_node(MetadataExtractorNode())
pipeline.add_node(AIAnalyzerNode())

UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)

@app.post("/api/v1/process-media")
async def process_media(file:UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    
    asset = PhotoAsset(file_path = file_path,filename = file.filename) 
    processed_asset = pipeline.execute(asset)

    return {
        "message":"success",
        "filename":processed_asset.filename,
        "tags":processed_asset.tags,
        "timestamp":processed_asset.timestamp,
        "location":processed_asset.location
    }
        
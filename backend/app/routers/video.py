from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
import shutil
import os
import uuid
from ..services.video_processor import process_video_file

router = APIRouter(
    prefix="/api/video",
    tags=["Video Processing"]
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Upload a video file for async YOLO processing.
    """
    if not file.filename.lower().endswith(('.mp4', '.mov', '.avi')):
         raise HTTPException(status_code=400, detail="Invalid file type. Only video files allowed.")
    
    # Generate unique filename
    safe_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
        
    # Trigger background processing
    # Use safe_filename to ensure output is unique and matches what we return
    background_tasks.add_task(process_video_file, file_path, safe_filename)
    
    # Construct the URL where the video will be available (once processed)
    # The frontend can poll this or just display it (it might take a moment to appear)
    output_url = f"/static/videos/processed_{safe_filename}"
    
    return {
        "message": "Video uploaded successfully. Processing started.",
        "filename": safe_filename,
        "original_filename": file.filename,
        "status": "processing",
        "output_video_url": output_url
    }

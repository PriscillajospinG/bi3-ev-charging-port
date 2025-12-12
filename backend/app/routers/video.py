from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from typing import List, Optional
import shutil
import os
import uuid
from sqlalchemy import select, func
from ..services.video_processor import (
    process_video_file, 
    get_processing_status, 
    get_all_processing_status,
    update_status,
    reset_processing_status
)
from ..database import AsyncSessionLocal
from ..models.events import VehicleEvent
from sqlalchemy import delete

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
    
    # Initialize status as pending
    update_status(file.filename, status="pending")
    
    # Trigger background processing
    background_tasks.add_task(process_video_file, file_path, file.filename)
    
    return {
        "message": "Video uploaded successfully. Processing started.",
        "filename": file.filename,
        "status": "processing"
    }

@router.get("/status/{filename}")
async def get_video_status(filename: str):
    """
    Get the processing status of a specific video file.
    """
    status = get_processing_status(filename)
    return {
        "filename": filename,
        **status
    }

@router.get("/status")
async def get_all_video_status():
    """
    Get the processing status of all video files.
    """
    all_status = get_all_processing_status()
    return {
        "total": len(all_status),
        "jobs": [{"filename": k, **v} for k, v in all_status.items()]
    }

@router.post("/reset")
async def reset_video_processing():
    """
    Reset all video processing data (status and database records).
    """
    # Clear in-memory status
    reset_processing_status()
    
    # Clear database records
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(delete(VehicleEvent))
            await session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear database: {e}")
        
    return {"message": "All video processing data reset successfully"}

@router.get("/results")
async def get_all_detection_results(limit: int = 100, offset: int = 0):
    """
    Get all vehicle detection results from the database.
    """
    try:
        async with AsyncSessionLocal() as session:
            # Get total count
            count_result = await session.execute(
                select(func.count()).select_from(VehicleEvent)
            )
            total_count = count_result.scalar()
            
            # Get results with pagination
            result = await session.execute(
                select(VehicleEvent)
                .order_by(VehicleEvent.timestamp.desc())
                .limit(limit)
                .offset(offset)
            )
            events = result.scalars().all()
            
            # Get summary by video source
            summary_result = await session.execute(
                select(
                    VehicleEvent.video_source,
                    VehicleEvent.class_name,
                    func.count().label('count')
                )
                .group_by(VehicleEvent.video_source, VehicleEvent.class_name)
            )
            summary_data = summary_result.all()
            
            # Organize summary by video
            video_summaries = {}
            for video_source, class_name, count in summary_data:
                if video_source not in video_summaries:
                    video_summaries[video_source] = {"total": 0, "by_class": {}}
                video_summaries[video_source]["by_class"][class_name] = count
                video_summaries[video_source]["total"] += count
            
            return {
                "total_detections": total_count,
                "limit": limit,
                "offset": offset,
                "video_summaries": video_summaries,
                "detections": [
                    {
                        "id": e.id,
                        "timestamp": e.timestamp.isoformat() if e.timestamp else None,
                        "video_source": e.video_source,
                        "class_name": e.class_name,
                        "confidence": round(e.confidence, 3) if e.confidence else None,
                        "event_type": e.event_type
                    } for e in events
                ]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/results/{video_source}")
async def get_video_detection_results(video_source: str):
    """
    Get detection results for a specific video.
    """
    try:
        async with AsyncSessionLocal() as session:
            # Get all detections for this video
            result = await session.execute(
                select(VehicleEvent)
                .where(VehicleEvent.video_source == video_source)
                .order_by(VehicleEvent.timestamp.desc())
            )
            events = result.scalars().all()
            
            if not events:
                return {
                    "video_source": video_source,
                    "total_detections": 0,
                    "summary": {},
                    "detections": []
                }
            
            # Build summary
            summary = {}
            for e in events:
                summary[e.class_name] = summary.get(e.class_name, 0) + 1
            
            return {
                "video_source": video_source,
                "total_detections": len(events),
                "summary": summary,
                "detections": [
                    {
                        "id": e.id,
                        "timestamp": e.timestamp.isoformat() if e.timestamp else None,
                        "class_name": e.class_name,
                        "confidence": round(e.confidence, 3) if e.confidence else None,
                        "event_type": e.event_type
                    } for e in events
                ]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

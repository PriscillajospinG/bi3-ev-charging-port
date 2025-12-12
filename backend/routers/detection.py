from fastapi import APIRouter, BackgroundTasks
import subprocess
import os

router = APIRouter(prefix="/detection", tags=["detection"])

# Global process reference (simple for this scope)
process = None

@router.post("/start")
async def start_detection(background_tasks: BackgroundTasks):
    global process
    if process and process.poll() is None:
        return {"status": "already_running"}
    
    # Path to traffic script
    script_path = os.path.join(os.getcwd(), "backend/models/dedection/traf1.py")
    
    # Run as subprocess
    # Note: simple execution, logs to stdout
    try:
        process = subprocess.Popen(["python3", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {"status": "started", "pid": process.pid}
    except Exception as e:
        return {"status": "error", "details": str(e)}

@router.post("/stop")
def stop_detection():
    global process
    if process and process.poll() is None:
        process.terminate()
        process = None
        return {"status": "stopped"}
    return {"status": "not_running"}

@router.get("/status")
def get_status():
    global process
    is_running = process is not None and process.poll() is None
    return {"status": "running" if is_running else "stopped"}

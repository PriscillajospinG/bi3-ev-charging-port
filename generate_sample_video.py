#!/usr/bin/env python3
"""
Sample Video Generator
Creates a test video with moving rectangles (simulating vehicles)
"""

import cv2
import numpy as np
from pathlib import Path

def generate_sample_video():
    """Generate a sample video with moving objects"""
    
    # Video properties
    width, height = 640, 480
    fps = 30
    duration = 5  # seconds
    total_frames = fps * duration
    
    # Create output directory
    Path('data/videos').mkdir(parents=True, exist_ok=True)
    
    output_path = 'data/videos/sample.mp4'
    
    # Define codec and create VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"📹 Generating sample video: {output_path}")
    print(f"   Duration: {duration}s @ {fps}fps = {total_frames} frames")
    
    # Generate frames
    for frame_num in range(total_frames):
        # Create blank frame (road scene)
        frame = np.ones((height, width, 3), dtype=np.uint8) * 200  # Light gray background
        
        # Draw road lines
        cv2.line(frame, (width//2, 0), (width//2, height), (255, 255, 0), 2)  # Yellow center line
        cv2.line(frame, (0, height//3), (width, height//3), (200, 200, 200), 1)  # Top line
        cv2.line(frame, (0, 2*height//3), (width, 2*height//3), (200, 200, 200), 1)  # Bottom line
        
        # Simulate moving vehicles (cars as rectangles)
        time = frame_num / fps  # Time in seconds
        
        # Car 1 - moving from left to right (top lane)
        car1_x = int((time * 100) % width)
        cv2.rectangle(frame, (car1_x, height//4 - 20), (car1_x + 80, height//4 + 20), (0, 0, 255), -1)  # Red car
        cv2.putText(frame, 'CAR', (car1_x + 10, height//4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Car 2 - moving from right to left (top lane)
        car2_x = int(width - (time * 80) % width)
        cv2.rectangle(frame, (car2_x, height//4 + 30), (car2_x + 70, height//4 + 70), (255, 0, 0), -1)  # Blue car
        cv2.putText(frame, 'CAR', (car2_x + 10, height//4 + 55), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Truck - moving from left to right (middle lane)
        truck_x = int((time * 60 + 100) % (width + 150))
        cv2.rectangle(frame, (truck_x, 2*height//4 - 30), (truck_x + 100, 2*height//4 + 30), (0, 165, 255), -1)  # Orange truck
        cv2.putText(frame, 'TRUCK', (truck_x + 15, 2*height//4 + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Car 3 - moving from left to right (bottom lane)
        car3_x = int((time * 90 + 50) % width)
        cv2.rectangle(frame, (car3_x, 3*height//4 - 20), (car3_x + 75, 3*height//4 + 20), (0, 255, 0), -1)  # Green car
        cv2.putText(frame, 'CAR', (car3_x + 10, 3*height//4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Add frame counter
        cv2.putText(frame, f'Frame: {frame_num}/{total_frames}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(frame, f'Time: {time:.1f}s', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        # Write frame
        out.write(frame)
        
        # Progress
        if frame_num % (fps * 1) == 0:
            print(f"   Progress: {frame_num}/{total_frames} frames written...")
    
    out.release()
    print(f"✅ Sample video created: {output_path}")
    print(f"   Ready to process with video_vehicle_counter.py\n")

if __name__ == "__main__":
    generate_sample_video()

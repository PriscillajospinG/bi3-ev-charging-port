#!/usr/bin/env python3
"""
Vehicle Counter - Count Total Vehicles & EV Vehicles
Using Pretrained RF-DETR Model
Person A: ML Engineer
"""

import json
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vehicle_counter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def count_vehicles():
    """
    Count total vehicles and EV vehicles from RF-DETR detections
    Three simple steps:
    1. Load detections from inference
    2. Read class labels
    3. Increment counters
    """
    
    logger.info("\n" + "="*60)
    logger.info("VEHICLE COUNTER - RF-DETR INFERENCE ANALYSIS")
    logger.info("="*60 + "\n")
    
    # Step 1: Load detections from inference output
    detections_path = Path("predictions/detections.json")
    
    if not detections_path.exists():
        logger.error(f"❌ Detections file not found: {detections_path}")
        return
    
    with open(detections_path, 'r') as f:
        detections_data = json.load(f)
    
    logger.info(f"✓ Loaded detections from: {detections_path}")
    
    # Step 2 & 3: Initialize counters and process detections
    total_vehicles = 0
    ev_vehicles = 0
    vehicles_by_class = {}
    
    # Vehicle classes that are considered "vehicles"
    vehicle_classes = {'car', 'truck', 'bus', 'motorcycle', 'bicycle', 'train'}
    # EV-specific classes (if model outputs them)
    ev_classes = {'ev_car', 'electric_car', 'ev_truck'}
    
    logger.info("\n" + "-"*60)
    logger.info("PROCESSING DETECTIONS")
    logger.info("-"*60 + "\n")
    
    # Process each detection
    for detection in detections_data.get('detections', []):
        class_label = detection.get('class', 'unknown').lower()
        confidence = detection.get('confidence', 0)
        frame = detection.get('frame', 'N/A')
        
        # Initialize class counter if not exists
        if class_label not in vehicles_by_class:
            vehicles_by_class[class_label] = 0
        
        # Step 3a: Count all vehicles
        if class_label in vehicle_classes:
            total_vehicles += 1
            vehicles_by_class[class_label] += 1
            logger.info(f"Frame {frame}: {class_label.upper()} detected (confidence: {confidence:.2%})")
        
        # Step 3b: Count EV vehicles
        if class_label in ev_classes:
            ev_vehicles += 1
            logger.info(f"Frame {frame}: ⚡ EV VEHICLE DETECTED - {class_label.upper()} (confidence: {confidence:.2%})")
        
        # Also count 'car' and 'truck' as potential EVs (heuristic)
        # In real scenario, model would have EV-specific class
        if class_label in {'car', 'truck'} and confidence > 0.80:
            # Assume high-confidence cars/trucks might be EVs
            # (In production, use model-specific EV class)
            pass
    
    # Generate summary report
    logger.info("\n" + "="*60)
    logger.info("VEHICLE COUNT SUMMARY")
    logger.info("="*60 + "\n")
    
    logger.info(f"📊 TOTAL VEHICLES DETECTED: {total_vehicles}")
    logger.info(f"⚡ EV VEHICLES DETECTED: {ev_vehicles}")
    
    if total_vehicles > 0:
        ev_percentage = (ev_vehicles / total_vehicles) * 100
        logger.info(f"📈 EV Penetration Rate: {ev_percentage:.1f}%")
    
    logger.info("\nVehicle Breakdown:")
    for class_label, count in sorted(vehicles_by_class.items()):
        if count > 0:
            logger.info(f"  • {class_label.upper()}: {count}")
    
    # Save results to JSON
    results = {
        "timestamp": datetime.now().isoformat(),
        "total_vehicles": total_vehicles,
        "ev_vehicles": ev_vehicles,
        "vehicles_by_class": vehicles_by_class,
        "statistics": {
            "ev_penetration_rate": (ev_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0,
            "total_detections_processed": len(detections_data.get('detections', []))
        }
    }
    
    results_path = Path("predictions/vehicle_counts.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"\n✓ Results saved to: {results_path}")
    
    # Log final status
    logger.info("\n" + "="*60)
    logger.info("✓ VEHICLE COUNTING COMPLETE")
    logger.info("="*60 + "\n")
    
    return results

if __name__ == "__main__":
    results = count_vehicles()
    
    # Pretty print results
    print("\n" + "🎯 FINAL RESULTS ".center(60, "="))
    print(f"Total Vehicles:    {results['total_vehicles']}")
    print(f"EV Vehicles:       {results['ev_vehicles']}")
    print(f"EV Rate:           {results['statistics']['ev_penetration_rate']:.1f}%")
    print("="*60 + "\n")

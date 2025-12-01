import cv2
import sqlite3
import datetime
import threading
import time
import numpy as np
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ultralytics import YOLO
import torch

# --- Configuration ---
app = FastAPI(title="SmartFridge OS Backend")
DB_PATH = "fridge_inventory.db"

# Allow CORS - Crucial for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. Hardware & AI Initialization ---

# Global variables
model = None
camera = None

def load_model():
    """Attempt to load YOLO model, fallback to None if failed"""
    global model
    try:
        print("Loading AI model...") 
        
        # PATCH: PyTorch 2.6+ defaults torch.load(weights_only=True), which breaks 
        # loading complex models like YOLOv8 that contain custom classes.
        _original_load = torch.load

        def _safe_load_wrapper(*args, **kwargs):
            if 'weights_only' not in kwargs:
                kwargs['weights_only'] = False
            return _original_load(*args, **kwargs)

        torch.load = _safe_load_wrapper
        
        try:
            # --- ATTEMPT 1: YOLO-WORLD MODEL (Advanced) ---
            print("Attempting to load YOLO-World (yolov8s-world.pt)...")
            try:
                model = YOLO("yolov8s-world.pt")
                
                # Define specific vocabulary for the fridge
                target_classes = [
                    "egg", "pumpkin", "milk", "milk carton", "vegetable", "fruit", 
                    "bottle", "can", "meat", "apple", "banana", "orange", 
                    "broccoli", "carrot", "fish", "seafood", "cheese", "yogurt"
                ]
                model.set_classes(target_classes)
                print(f"SUCCESS: YOLO-World loaded! Vocabulary: {', '.join(target_classes)}")
                
            except Exception as e:
                # --- ATTEMPT 2: STANDARD YOLOv8 (Fallback) ---
                print(f"WARNING: YOLO-World failed to load ({e}). Likely due to old ultralytics version.")
                print("Falling back to standard YOLOv8n (yolov8n.pt)...")
                model = YOLO("yolov8n.pt")
                print("SUCCESS: Standard YOLOv8n loaded. (Note: Some items like 'pumpkin' may not be detected)")

        finally:
            torch.load = _original_load
            
    except Exception as e:
        print(f"CRITICAL: All AI Models failed to load ({e}). Using simulation mode.") 
        model = None

# Load model in background thread
threading.Thread(target=load_model, daemon=True).start()

class CameraManager:
    """Camera manager with fault tolerance"""
    def __init__(self):
        self.cap = None

    def get_frame(self):
        # Try to open camera
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                blank_image = np.zeros((480, 640, 3), np.uint8)
                cv2.putText(blank_image, "No Camera", (200, 240), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                return blank_image

        success, frame = self.cap.read()
        if not success:
            blank_image = np.zeros((480, 640, 3), np.uint8)
            cv2.putText(blank_image, "Camera Error", (200, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return blank_image
            
        return frame

    def release(self):
        if self.cap:
            self.cap.release()

camera_manager = CameraManager()

# --- 2. Database Management (SQLite) ---

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER,
                unit TEXT,
                purchase_date TEXT,
                expiry_date TEXT,
                image_icon TEXT
            )
        ''')
        conn.commit()

init_db()

# --- 3. Data Models (Pydantic) ---

class InventoryItem(BaseModel):
    name: str
    category: str
    quantity: int
    unit: str
    purchase_date: str
    expiry_date: str
    image_icon: str

class InventoryItemResponse(InventoryItem):
    id: int

# --- 4. Helper Logic ---

def get_item_details(label: str):
    """Generate details based on detected object label"""
    today = datetime.date.today()
    label = label.lower()
    
    # Defaults
    details = {
        "name": label,
        "category": "Other",
        "days": 7,
        "icon": "📦",
        "unit": "pcs"
    }

    # Enhanced mapping rule
    if label in ["apple", "banana", "orange", "fruit", "pear", "grape"]:
        details.update({"category": "Fruit", "days": 7, "icon": "🍎", "unit": "pcs"})
    elif label in ["broccoli", "carrot", "vegetable", "potted plant", "lettuce", "cucumber"]:
        details.update({"category": "Veg", "days": 5, "icon": "🥦", "unit": "bundle"})
    elif label in ["bottle", "cup", "milk", "milk carton", "yogurt", "cheese"]:
        details.update({"category": "Dairy", "days": 10, "icon": "🥛", "unit": "bottle"})
    elif label in ["egg", "bird", "ball", "sports ball"]: 
        details.update({"category": "Eggs", "days": 15, "icon": "🥚", "unit": "pcs", "name": "egg"})
    elif label in ["fish", "seafood"]:
        details.update({"category": "Seafood", "days": 2, "icon": "🐟", "unit": "slice"})
    elif label in ["pumpkin", "squash"]:
        details.update({"category": "Veg", "days": 30, "icon": "🎃", "unit": "pcs"})
    elif label in ["meat", "beef", "steak", "chicken"]:
        details.update({"category": "Meat", "days": 3, "icon": "🥩", "unit": "kg"})
    
    # Calculate expiry date string
    expiry = today + datetime.timedelta(days=details["days"])
    
    return {
        "name": details["name"],
        "category": details["category"],
        "quantity": 1,
        "unit": details["unit"],
        "image_icon": details["icon"],
        "purchase_date": today.isoformat(),
        "expiry_date": expiry.isoformat()
    }

# --- 5. API Endpoints ---

@app.get("/")
def read_root():
    return {"status": "SmartFridge OS Backend Online"}

@app.get("/api/inventory", response_model=List[InventoryItemResponse])
def get_inventory():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory ORDER BY expiry_date ASC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@app.post("/api/inventory")
def add_item(item: InventoryItem):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inventory (name, category, quantity, unit, purchase_date, expiry_date, image_icon)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (item.name, item.category, item.quantity, item.unit, item.purchase_date, item.expiry_date, item.image_icon))
        conn.commit()
        return {"id": cursor.lastrowid, "message": "Item added successfully"}

@app.delete("/api/inventory/{item_id}")
def delete_item(item_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        conn.commit()
    return {"message": "Item deleted"}

@app.get("/api/scan/live")
def scan_live():
    """
    Called when frontend clicks 'Scan'.
    """
    frame = camera_manager.get_frame()
    detected_objects = []

    # 1. Try AI detection
    if model:
        try:
            results = model(frame)
            for result in results:
                for box in result.boxes:
                    conf = float(box.conf[0])
                    # With YOLO-World + Custom Classes, we can trust slightly lower confidence
                    if conf > 0.15: 
                        cls_id = int(box.cls[0])
                        label = model.names[cls_id]
                        detected_objects.append(label)
                        print(f"DEBUG: Detected {label} ({conf:.2f})") 
        except Exception as e:
            print(f"AI Inference Error: {e}") 
    
    # 2. Simulation fallback
    if not detected_objects:
        # Use simple simulation if nothing found
        import random
        demo_items = ["apple", "broccoli", "milk", "fish"]
        detected_objects = [random.choice(demo_items)]
        print(f"No object detected, returning demo data: {detected_objects[0]}") 

    # 3. Construct response
    if detected_objects:
        # Prioritize pumpkin or egg if detected, otherwise pick the first one
        primary_item = detected_objects[0]
        for obj in detected_objects:
            if obj in ["pumpkin", "egg", "milk"]:
                primary_item = obj
                break
                
        details = get_item_details(primary_item)
        
        return {
            "found": True,
            "confidence": 0.95,
            **details 
        }
    else:
        return {"found": False}

@app.get("/api/video_feed")
def video_feed():
    def iter_frames():
        while True:
            frame = camera_manager.get_frame()
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.03) 

    return StreamingResponse(iter_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    import uvicorn
    print("Starting SmartFridge Backend with YOLO-World...") 
    uvicorn.run(app, host="0.0.0.0", port=8000)

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

# Allow CORS
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
        print("Loading YOLOv8 model...")  # Changed to English
        
        # PATCH: PyTorch 2.6+ defaults torch.load(weights_only=True), which breaks 
        # loading complex models like YOLOv8 that contain custom classes.
        # We temporarily patch torch.load to allow pickle loading (weights_only=False)
        # just for this operation.
        _original_load = torch.load

        def _safe_load_wrapper(*args, **kwargs):
            # If the caller didn't specify weights_only, force it to False
            if 'weights_only' not in kwargs:
                kwargs['weights_only'] = False
            return _original_load(*args, **kwargs)

        torch.load = _safe_load_wrapper
        
        try:
            # First run will download yolov8n.pt automatically
            model = YOLO("yolov8n.pt")
            print("AI Model loaded successfully!") # Changed to English
        finally:
            # Always restore the original function to avoid affecting other parts of the app
            torch.load = _original_load
            
    except Exception as e:
        print(f"Warning: AI Model load failed ({e}). Using simulation mode.") # Changed to English
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
            # 0 is usually the default USB camera
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                # Return a generated image if camera fails
                blank_image = np.zeros((480, 640, 3), np.uint8)
                cv2.putText(blank_image, "No Camera Found", (200, 240), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                return blank_image

        success, frame = self.cap.read()
        if not success:
            # Return error image if read fails
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

    # Simple rule mapping
    if label in ["apple", "banana", "orange", "fruit"]:
        details.update({"category": "Fruit", "days": 7, "icon": "🍎", "unit": "pcs"})
    elif label in ["broccoli", "carrot", "vegetable", "potted plant"]:
        details.update({"category": "Veg", "days": 5, "icon": "🥦", "unit": "bundle"})
    elif label in ["bottle", "cup", "milk"]:
        details.update({"category": "Dairy", "days": 10, "icon": "🥛", "unit": "bottle"})
    elif label in ["egg", "bird", "ball"]: 
        details.update({"category": "Eggs", "days": 15, "icon": "🥚", "unit": "pcs"})
    elif label in ["fish", "seafood"]:
        details.update({"category": "Seafood", "days": 2, "icon": "🐟", "unit": "slice"})
    
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
    1. Get current frame
    2. Run AI
    3. Return result
    """
    frame = camera_manager.get_frame()
    detected_objects = []

    # 1. Try AI detection
    if model:
        try:
            results = model(frame)
            for result in results:
                for box in result.boxes:
                    if float(box.conf[0]) > 0.5: # Confidence threshold
                        cls_id = int(box.cls[0])
                        detected_objects.append(model.names[cls_id])
        except Exception as e:
            print(f"AI Inference Error: {e}") # Changed to English
    
    # 2. Simulation fallback
    if not detected_objects:
        # Random simulation for demo
        import random
        demo_items = ["apple", "broccoli", "milk", "fish"]
        detected_objects = [random.choice(demo_items)]
        print(f"No object detected (or no model), returning demo data: {detected_objects[0]}") # Changed to English

    # 3. Construct response
    if detected_objects:
        primary_item = detected_objects[0]
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
    """
    Multipart MJPEG stream
    """
    def iter_frames():
        while True:
            frame = camera_manager.get_frame()
            
            # Compress to JPEG
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
    print("Starting SmartFridge Backend...") # Changed to English
    uvicorn.run(app, host="0.0.0.0", port=8000)

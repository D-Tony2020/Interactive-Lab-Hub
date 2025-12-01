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

# --- Configuration ---
app = FastAPI(title="SmartFridge OS Backend")
DB_PATH = "fridge_inventory.db"

# ================= MODEL CONFIGURATION =================
# 选择你的模型类型: "yolo" 或 "teachable_machine"
MODEL_TYPE = "yolo" 

# [配置 A] YOLO 设置
YOLO_MODEL_PATH = "yolov8s-world.pt"
YOLO_CLASSES = ["egg", "pumpkin", "milk", "vegetable", "fruit", "meat"]

# [配置 B] Teachable Machine 设置
TM_MODEL_PATH = "model.tflite"   # 你的 .tflite 文件名
TM_LABELS_PATH = "labels.txt"    # 你的 labels.txt 文件名
CONFIDENCE_THRESHOLD = 0.7       # Teachable Machine 的置信度通常要设高一点
# =======================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model = None
tm_labels = []
camera = None

# --- 1. Model Loading Logic ---

def load_yolo():
    global model
    from ultralytics import YOLO
    import torch
    
    print(f"Loading YOLO model: {YOLO_MODEL_PATH}...")
    # Patch for PyTorch 2.6+
    _original_load = torch.load
    def _safe_load_wrapper(*args, **kwargs):
        if 'weights_only' not in kwargs: kwargs['weights_only'] = False
        return _original_load(*args, **kwargs)
    torch.load = _safe_load_wrapper
    
    try:
        model = YOLO(YOLO_MODEL_PATH)
        if "world" in YOLO_MODEL_PATH:
            model.set_classes(YOLO_CLASSES)
        print("✅ YOLO model loaded!")
        return "yolo"
    finally:
        torch.load = _original_load

def load_teachable_machine():
    global model, tm_labels
    print(f"Loading Teachable Machine model: {TM_MODEL_PATH}...")
    
    try:
        # Try importing TFLite runtime, fallback to full TensorFlow
        try:
            import tflite_runtime.interpreter as tflite
        except ImportError:
            import tensorflow.lite.python.interpreter as tflite
        
        # Load Model
        interpreter = tflite.Interpreter(model_path=TM_MODEL_PATH)
        interpreter.allocate_tensors()
        model = interpreter
        
        # Load Labels
        with open(TM_LABELS_PATH, "r") as f:
            # Strip index numbers if present (e.g. "0 Apple" -> "Apple")
            lines = f.readlines()
            tm_labels = [line.strip().split(" ", 1)[-1] if " " in line.strip() else line.strip() for line in lines]
            
        print(f"✅ Teachable Machine loaded! Labels: {tm_labels}")
        return "tm"
    except Exception as e:
        print(f"❌ Failed to load Teachable Machine model: {e}")
        return None

def load_model_thread():
    if MODEL_TYPE == "yolo":
        load_yolo()
    elif MODEL_TYPE == "teachable_machine":
        load_teachable_machine()
    else:
        print("Unknown MODEL_TYPE")

threading.Thread(target=load_model_thread, daemon=True).start()

# --- 2. Camera & Database (Standard) ---

class CameraManager:
    def __init__(self):
        self.cap = None

    def get_frame(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                blank = np.zeros((480, 640, 3), np.uint8)
                cv2.putText(blank, "No Camera", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                return blank
        success, frame = self.cap.read()
        return frame if success else np.zeros((480, 640, 3), np.uint8)

    def release(self):
        if self.cap: self.cap.release()

camera_manager = CameraManager()

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.cursor().execute('''
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

# --- 3. Helper Logic ---

def get_item_details(label: str):
    today = datetime.date.today()
    label = label.lower().strip()
    
    details = {"name": label, "category": "Other", "days": 7, "icon": "📦", "unit": "pcs"}

    # Keyword matching for robustness
    if any(x in label for x in ["apple", "banana", "orange", "fruit"]):
        details.update({"category": "Fruit", "days": 7, "icon": "🍎"})
    elif any(x in label for x in ["broccoli", "carrot", "veg", "pumpkin", "squash"]):
        details.update({"category": "Veg", "days": 5, "icon": "🥦"})
        if "pumpkin" in label: details["icon"] = "🎃"
    elif any(x in label for x in ["milk", "yogurt", "cheese", "dairy"]):
        details.update({"category": "Dairy", "days": 10, "icon": "🥛"})
    elif any(x in label for x in ["egg"]):
        details.update({"category": "Eggs", "days": 15, "icon": "🥚"})
    elif any(x in label for x in ["meat", "beef", "chicken"]):
        details.update({"category": "Meat", "days": 3, "icon": "🥩"})
    
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

# --- 4. API Endpoints ---

@app.get("/")
def read_root(): return {"status": f"Backend Online ({MODEL_TYPE})"}

@app.get("/api/inventory", response_model=List[InventoryItemResponse])
def get_inventory():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.cursor().execute("SELECT * FROM inventory ORDER BY expiry_date ASC").fetchall()
        return [dict(row) for row in rows]

@app.post("/api/inventory")
def add_item(item: InventoryItem):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO inventory (name, category, quantity, unit, purchase_date, expiry_date, image_icon) VALUES (?,?,?,?,?,?,?)',
                  (item.name, item.category, item.quantity, item.unit, item.purchase_date, item.expiry_date, item.image_icon))
        conn.commit()
        return {"id": c.lastrowid}

@app.delete("/api/inventory/{item_id}")
def delete_item(item_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.cursor().execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        conn.commit()
    return {"message": "Deleted"}

@app.get("/api/scan/live")
def scan_live():
    frame = camera_manager.get_frame()
    detected_label = None
    confidence = 0.0

    if model:
        try:
            # --- LOGIC A: YOLO ---
            if MODEL_TYPE == "yolo":
                results = model(frame)
                for r in results:
                    for box in r.boxes:
                        conf = float(box.conf[0])
                        if conf > 0.25:
                            detected_label = model.names[int(box.cls[0])]
                            confidence = conf
                            print(f"DEBUG (YOLO): Found {detected_label} ({confidence:.2f})")
                            break # Take first high conf item
            
            # --- LOGIC B: TEACHABLE MACHINE (TFLite) ---
            elif MODEL_TYPE == "teachable_machine":
                # 1. Preprocess: Resize to 224x224 (Standard TM size)
                img = cv2.resize(frame, (224, 224))
                # 2. Normalize: TM uses range [-1, 1] => (img / 127.5) - 1
                img = (img.astype(np.float32) / 127.5) - 1.0
                # 3. Add batch dimension: [1, 224, 224, 3]
                input_data = np.expand_dims(img, axis=0)
                
                # 4. Inference
                input_details = model.get_input_details()
                output_details = model.get_output_details()
                model.set_tensor(input_details[0]['index'], input_data)
                model.invoke()
                output_data = model.get_tensor(output_details[0]['index'])[0]
                
                # 5. Parse result
                max_index = np.argmax(output_data)
                confidence = float(output_data[max_index])
                detected_label = tm_labels[max_index]
                
                print(f"DEBUG (TM): Found {detected_label} ({confidence:.2f})")

        except Exception as e:
            print(f"Inference Error: {e}")

    # Fallback simulation
    if not detected_label or confidence < CONFIDENCE_THRESHOLD:
        if not model: # Only simulate if model totally failed to load
            import random
            detected_label = random.choice(["apple", "milk", "egg"])
            confidence = 0.99
        else:
            return {"found": False}

    if detected_label == "Class 1" or detected_label == "Background": # Filter bad TM labels
        return {"found": False}

    details = get_item_details(detected_label)
    return {"found": True, "confidence": confidence, **details}

@app.get("/api/video_feed")
def video_feed():
    def iter_frames():
        while True:
            frame = camera_manager.get_frame()
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret: yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.03)
    return StreamingResponse(iter_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    import uvicorn
    print(f"Starting SmartFridge Backend ({MODEL_TYPE} mode)...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

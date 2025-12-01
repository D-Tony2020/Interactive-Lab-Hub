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

# [配置 A] YOLO 设置 (YOLO-World Open Vocabulary)
YOLO_MODEL_PATH = "yolov8s-world.pt"
YOLO_CLASSES = [
    "bright green lettuce leaves",
    "dark green spinach bunch",
    "orange carrot sticks",
    "smooth green cucumber slices",
    "purple round onion",
    "white sliced mushrooms",
    "light green celery stalks",
    "dark purple eggplant pieces",
    "pale green cabbage head",
    "bright red tomato",

    "shiny red apple",
    "ripe yellow banana",
    "pale yellow pear",
    "green seedless grape bunch",
    "deep orange mandarin",
    "fuzzy-skinned peach",
    "dark purple blueberry box",
    "bright yellow lemon",
    "green lime",
    "light green melon cubes",

    "pink raw chicken breast",
    "red lean beef chunks",
    "pale pink pork loin slices",
    "white fish fillet",
    "orange salmon slices",
    "brown cooked steak slices",
    "white-shelled egg",
    "brown-shelled egg",

    "yellow cheddar cheese block",
    "white mozzarella cheese balls",
    "pale yellow butter block",
    "blue-capped milk bottle",
    "white yogurt cup",
    "light pink strawberry milkshake bottle",

    "silver soda can",
    "clear bottled water",
    "red ketchup bottle",
    "yellow mustard bottle",
    "clear ice cubes in tray",
    "green glass pickle jar",
    "blue-white packaged tofu box"
]

# [配置 B] Teachable Machine 设置
TM_MODEL_PATH = "model.tflite"   # 你的 .tflite 文件名
TM_LABELS_PATH = "labels.txt"    # 你的 labels.txt 文件名
CONFIDENCE_THRESHOLD = 0.15      # YOLO-World 对于长描述可能置信度偏低，适当降低阈值
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
            print(f"Setting custom classes ({len(YOLO_CLASSES)} items)...")
            model.set_classes(YOLO_CLASSES)
        print("YOLO model loaded!")
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
            
        print(f"Teachable Machine loaded! Labels: {tm_labels}")
        return "tm"
    except Exception as e:
        print(f"Failed to load Teachable Machine model: {e}")
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
    
    # Default fallback
    details = {"name": label, "category": "Other", "days": 7, "icon": "📦", "unit": "pcs"}

    # Keyword mapping based on your specific YOLO_CLASSES
    # Fruit
    if any(x in label for x in ["apple", "banana", "pear", "grape", "mandarin", "peach", "blueberry", "lemon", "lime", "melon", "fruit"]):
        details.update({"category": "Fruit", "days": 7, "icon": "🍎"})
        if "banana" in label: details["icon"] = "🍌"
        elif "grape" in label: details["icon"] = "🍇"
        elif "lemon" in label: details["icon"] = "🍋"
    
    # Veg
    elif any(x in label for x in ["lettuce", "spinach", "carrot", "cucumber", "onion", "mushroom", "celery", "eggplant", "cabbage", "tomato", "pumpkin", "tofu", "pickle"]):
        details.update({"category": "Veg", "days": 5, "icon": "🥦"})
        if "carrot" in label: details["icon"] = "🥕"
        elif "tomato" in label: details["icon"] = "🍅"
        elif "pumpkin" in label: details["icon"] = "🎃"
        elif "mushroom" in label: details["icon"] = "🍄"
        elif "onion" in label: details["icon"] = "🧅"
    
    # Meat & Seafood
    elif any(x in label for x in ["chicken", "beef", "pork", "steak", "meat"]):
        details.update({"category": "Meat", "days": 3, "icon": "🥩", "unit": "pkg"})
    elif any(x in label for x in ["fish", "salmon", "seafood"]):
        details.update({"category": "Seafood", "days": 2, "icon": "🐟", "unit": "pkg"})
    
    # Dairy & Eggs
    elif any(x in label for x in ["cheese", "butter", "milk", "yogurt", "cheddar", "mozzarella"]):
        details.update({"category": "Dairy", "days": 14, "icon": "🥛", "unit": "item"})
        if "cheese" in label: details["icon"] = "🧀"
        elif "butter" in label: details["icon"] = "🧈"
    elif "egg" in label: # matches white-shelled egg, brown-shelled egg
        details.update({"category": "Eggs", "days": 21, "icon": "🥚", "unit": "pcs"})
        
    # Pantry / Drinks
    elif any(x in label for x in ["soda", "water", "juice"]):
        details.update({"category": "Drinks", "days": 180, "icon": "🥤", "unit": "can/bottle"})
    elif any(x in label for x in ["ketchup", "mustard", "sauce"]):
        details.update({"category": "Pantry", "days": 365, "icon": "🧂", "unit": "bottle"})
    elif "ice" in label:
        details.update({"category": "Freezer", "days": 365, "icon": "🧊", "unit": "tray"})
    
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
                        if conf > CONFIDENCE_THRESHOLD:
                            # With YOLO-World, the class ID maps to our custom list index
                            # or model.names which has been updated
                            cls_id = int(box.cls[0])
                            detected_label = model.names[cls_id]
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

    # Fallback simulation (only if model broken/missing)
    if not detected_label or confidence < CONFIDENCE_THRESHOLD:
        if not model: 
            import random
            detected_label = random.choice(["shiny red apple", "blue-capped milk bottle", "white-shelled egg"])
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

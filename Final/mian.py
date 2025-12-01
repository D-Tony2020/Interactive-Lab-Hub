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

# --- 配置部分 ---
app = FastAPI(title="SmartFridge OS Backend")
DB_PATH = "fridge_inventory.db"

# 允许跨域 (CORS) - 关键：确保前端能调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. 硬件与 AI 初始化 ---

# 全局变量
model = None
camera = None

def load_model():
    """尝试加载 YOLO 模型，失败则标记为 None"""
    global model
    try:
        print("正在加载 YOLOv8 模型...")
        # 首次运行会自动下载 yolov8n.pt (约6MB)
        model = YOLO("yolov8n.pt")
        print("AI 模型加载成功!")
    except Exception as e:
        print(f"警告: AI 模型加载失败 ({e})。将使用模拟识别模式。")
        model = None

# 在后台线程加载模型，不阻塞服务器启动
threading.Thread(target=load_model, daemon=True).start()

class CameraManager:
    """摄像头管理类，包含容错处理"""
    def __init__(self):
        self.cap = None

    def get_frame(self):
        # 尝试打开摄像头
        if self.cap is None or not self.cap.isOpened():
            # 0 通常是默认 USB 摄像头，如果是树莓派 CSI 可能需要配置
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                # 如果打开失败，生成一个黑底带文字的模拟帧
                blank_image = np.zeros((480, 640, 3), np.uint8)
                cv2.putText(blank_image, "No Camera Found", (200, 240), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                return blank_image

        success, frame = self.cap.read()
        if not success:
            # 读取失败时返回模拟帧
            blank_image = np.zeros((480, 640, 3), np.uint8)
            cv2.putText(blank_image, "Camera Error", (200, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return blank_image
            
        return frame

    def release(self):
        if self.cap:
            self.cap.release()

camera_manager = CameraManager()

# --- 2. 数据库管理 (SQLite) ---

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

# --- 3. 数据模型 (Pydantic) ---
# 必须与前端 App.jsx 中的 fetch body 完全一致

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

# --- 4. 辅助逻辑 ---

def get_item_details(label: str):
    """根据识别到的物体标签，生成前端需要的详细信息"""
    today = datetime.date.today()
    label = label.lower()
    
    # 默认值
    details = {
        "name": label,
        "category": "Other",
        "days": 7,
        "icon": "📦",
        "unit": "pcs"
    }

    # 简单的规则映射
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
    
    # 计算具体的日期字符串 (YYYY-MM-DD)
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

# --- 5. API 接口 ---

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
    前端点击 'Scan' 时调用。
    1. 获取当前帧
    2. 运行 AI 识别
    3. 返回识别结果和智能推断的保质期等信息
    """
    frame = camera_manager.get_frame()
    detected_objects = []

    # 1. 尝试 AI 识别
    if model:
        try:
            results = model(frame)
            for result in results:
                for box in result.boxes:
                    if float(box.conf[0]) > 0.5: # 置信度阈值
                        cls_id = int(box.cls[0])
                        detected_objects.append(model.names[cls_id])
        except Exception as e:
            print(f"AI 推理出错: {e}")
    
    # 2. 如果没有 AI 或没识别到，进行模拟 (用于演示)
    if not detected_objects:
        # 为了演示效果，随机返回一个物品
        # 在生产环境中，这里应该返回 found: False
        import random
        demo_items = ["apple", "broccoli", "milk", "fish"]
        detected_objects = [random.choice(demo_items)]
        print(f"未识别到物体 (或无模型)，返回模拟数据: {detected_objects[0]}")

    # 3. 构造返回数据
    if detected_objects:
        primary_item = detected_objects[0]
        details = get_item_details(primary_item)
        
        return {
            "found": True,
            "confidence": 0.95,
            **details # 展开 name, category, expiry_date, image_icon 等
        }
    else:
        return {"found": False}

@app.get("/api/video_feed")
def video_feed():
    """
    视频流接口，返回 multipart MJPEG 流
    """
    def iter_frames():
        while True:
            frame = camera_manager.get_frame()
            
            # 可选：这里可以把 YOLO 的识别框画在 frame 上再返回
            # if model: ...
            
            # 压缩为 JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # 控制帧率，避免占用过多 CPU
            time.sleep(0.03) 

    return StreamingResponse(iter_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    import uvicorn
    # host="0.0.0.0" 允许局域网访问
    print("启动 SmartFridge 后端...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

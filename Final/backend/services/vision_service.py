import cv2
import time
import threading
import numpy as np
import collections
import os

# Try importing TFLite runtime, fallback to full TensorFlow
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    try:
        import tensorflow.lite.python.interpreter as tflite
    except ImportError:
        tflite = None

from services.led_service import led_service

# Configuration
TM_MODEL_PATH = "/home/pi/Interactive-Lab-Hub/Final/model/model_unquant.tflite"
TM_LABELS_PATH = "/home/pi/Interactive-Lab-Hub/Final/model/labels.txt"
CONFIDENCE_THRESHOLD = 0.7  # High confidence for TM
HISTORY_SIZE = 20           # Number of frames to keep for smoothing
VOTE_THRESHOLD = 15         # How many frames must match to confirm detection

class VisionService:
    def __init__(self):
        self.model = None
        self.labels = []
        self.running = True
        self.current_frame = None
        self.lock = threading.Lock()
        
        # State
        self.is_scanning = False # If True, actively processing. If False, just camera feed.
        self.last_stable_label = None
        self.history = collections.deque(maxlen=HISTORY_SIZE)
        
        self.last_accessed = 0 # Timestamp of last API call
        
        # Load Model
        self._load_model()
        
        # Camera Setup
        self.cap = cv2.VideoCapture(0)
        
        # Start Thread
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def _load_model(self):
        print(f"[Vision] Loading Teachable Machine model: {TM_MODEL_PATH}...")
        if not os.path.exists(TM_MODEL_PATH):
            print(f"[Vision] Error: Model file not found at {TM_MODEL_PATH}")
            return

        try:
            # Load Model
            self.interpreter = tflite.Interpreter(model_path=TM_MODEL_PATH)
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            # Load Labels
            with open(TM_LABELS_PATH, "r") as f:
                lines = f.readlines()
                self.labels = [line.strip().split(" ", 1)[-1] if " " in line.strip() else line.strip() for line in lines]
            
            print(f"[Vision] Loaded Labels: {self.labels}")
            self.model = self.interpreter # Marker that model is ready
            
        except Exception as e:
            print(f"[Vision] Failed to load model: {e}")

    def _loop(self):
        while self.running:
            if not self.cap or not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)
                time.sleep(1)
                continue

            success, frame = self.cap.read()
            if not success:
                time.sleep(0.1)
                continue
            
            # Update frame safely for video feed
            with self.lock:
                self.current_frame = frame.copy()

            # --- Watchdog Check ---
            # Only run inference if API was accessed recently (e.g. last 2 seconds)
            if time.time() - self.last_accessed > 2.0:
                if led_service.state == "SCANNING" or led_service.state == "SUCCESS":
                    led_service.set_state("IDLE")
                # Sleep a bit longer when idle to save CPU
                time.sleep(0.2)
                continue

            # --- Inference Logic ---
            if self.model:
                try:
                    # Preprocess for TM (224x224, normalized -1 to 1)
                    img = cv2.resize(frame, (224, 224))
                    img = (img.astype(np.float32) / 127.5) - 1.0
                    input_data = np.expand_dims(img, axis=0)

                    self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
                    self.interpreter.invoke()
                    output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]

                    max_index = np.argmax(output_data)
                    confidence = float(output_data[max_index])
                    label = self.labels[max_index]

                    # Filter "nothing" or low confidence
                    if label.lower() == "nothing" or label == "Class 1" or label == "Background" or confidence < CONFIDENCE_THRESHOLD:
                        current_result = None
                    else:
                        current_result = label

                    # Add to history
                    self.history.append(current_result)
                    
                    # --- Smoothing / Voting ---
                    # Count non-None votes
                    valid_votes = [x for x in self.history if x is not None]
                    if valid_votes:
                        most_common_label, count = collections.Counter(valid_votes).most_common(1)[0]
                        
                        # Decision Logic
                        if count >= VOTE_THRESHOLD:
                            # STABLE DETECTION
                            if self.last_stable_label != most_common_label:
                                print(f"[Vision] Stable Detection: {most_common_label} (Votes: {count}/{HISTORY_SIZE})")
                                self.last_stable_label = most_common_label
                                led_service.set_state("SUCCESS")
                            
                        else:
                            # Not stable yet
                            if self.last_stable_label is not None:
                                print("[Vision] Lost detection...")
                                self.last_stable_label = None
                                led_service.set_state("SCANNING") # Back to scanning
                            else:
                                if led_service.state == "IDLE":
                                    led_service.set_state("SCANNING")

                    else:
                        # History is full of Nones (Nothing)
                        if self.last_stable_label is not None:
                             self.last_stable_label = None
                             led_service.set_state("SCANNING")
                        
                except Exception as e:
                    print(f"[Vision] Inference Error: {e}")
                    time.sleep(0.5)
            
            # FPS Limiter for inference loop (approx 10-15 FPS is enough for sensing)
            time.sleep(0.05) 

    def get_frame(self):
        with self.lock:
             return self.current_frame.copy() if self.current_frame is not None else np.zeros((480, 640, 3), np.uint8)

    def get_stable_result(self):
        self.last_accessed = time.time() # Reset watchdog
        return self.last_stable_label

vision_service = VisionService()

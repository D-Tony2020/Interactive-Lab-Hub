import threading
import time
import random

# Default mock for non-Pi or import errors
IS_RPI = False
try:
    import board
    import neopixel
    IS_RPI = True
except (ImportError, NotImplementedError):
    print("[LED] NeoPixel libraries not found or not on Pi. Using Mock mode.")

class LEDService:
    def __init__(self, pin=None, num_pixels=7):
        self.state = "IDLE"
        self.num_pixels = num_pixels
        self.pixels = None
        self.running = True
        self.current_thread = None

        if IS_RPI:
            try:
                # D18 is the standard pin (GPIO 18)
                pixel_pin = board.D18
                self.pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False)
                print("[LED] NeoPixel initialized on D18.")
            except Exception as e:
                print(f"[LED] Verification Error: {e}")
                print("[LED] (Did you run with sudo? Root is often required for GPIO 18/PWM)")
                self.pixels = None
        
        # Start background loop in a separate thread
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def set_state(self, state):
        """
        States: 
        - 'IDLE': Dim White/Off
        - 'SCANNING': Blue Spin
        - 'SUCCESS': Green Flash
        - 'ERROR': Red Flash
        - 'EXPIRING': Yellow Flash/Pulse
        - 'THINKING': Purple Pulse
        """
        if self.state != state:
            self.state = state
            print(f"[LED] State changed to: {state}")
            # Reset pixels on state change for clean transition
            if self.pixels:
                self.pixels.fill((0, 0, 0))
                self.pixels.show()

    def _loop(self):
        while self.running:
            if not self.pixels:
                print("[LED DEBUG] No pixels object", flush=True)
                time.sleep(1)
                continue

            try:
                # print(f"[LED DEBUG] Loop running, State: {self.state}", flush=True)
                if self.state == "IDLE":
                    # Dim warm white breathing or static
                    self.pixels.fill((10, 10, 10))
                    self.pixels.show()
                    time.sleep(0.5)

                elif self.state == "SCANNING":
                    # Blue spinning (0, 0, 255)
                    for i in range(self.num_pixels):
                        self.pixels.fill((0, 0, 0))
                        self.pixels[i] = (0, 0, 255)
                        self.pixels.show()
                        time.sleep(0.1)
                
                elif self.state == "SUCCESS":
                    # Green Flash (0, 255, 0)
                    for _ in range(3):
                        self.pixels.fill((0, 255, 0))
                        self.pixels.show()
                        time.sleep(0.2)
                        self.pixels.fill((0, 0, 0))
                        self.pixels.show()
                        time.sleep(0.2)
                    self.set_state("IDLE") # Auto revert

                elif self.state == "EXPIRING":
                    # Yellow Flash (255, 255, 0)
                    for _ in range(3):
                        self.pixels.fill((200, 200, 0)) # Slightly dimmed yellow
                        self.pixels.show()
                        time.sleep(0.3)
                        self.pixels.fill((0, 0, 0))
                        self.pixels.show()
                        time.sleep(0.3)
                    self.set_state("IDLE")

                elif self.state == "ERROR":
                    # Red Flash (255, 0, 0)
                    for _ in range(3):
                        self.pixels.fill((255, 0, 0))
                        self.pixels.show()
                        time.sleep(0.2)
                        self.pixels.fill((0, 0, 0))
                        self.pixels.show()
                        time.sleep(0.2)
                    self.set_state("IDLE")

                elif self.state == "LISTENING":
                    # Cyan Breathing (0, 255, 255)
                    for b in range(10, 100, 5): 
                        if self.state != "LISTENING": break
                        self.pixels.fill((0, b, b))
                        self.pixels.show()
                        time.sleep(0.02)
                    for b in range(100, 10, -5):
                        if self.state != "LISTENING": break
                        self.pixels.fill((0, b, b))
                        self.pixels.show()
                        time.sleep(0.02)

                elif self.state == "SPEAKING":
                    # Simulate Voice Waveform (White/Purple flicker)
                    # Random brightness to mimic speech amplitude
                    import random
                    brightness = random.randint(10, 200)
                    # Using Purple/Blueish tint for AI voice
                    self.pixels.fill((brightness // 2, 0, brightness)) 
                    self.pixels.show()
                    time.sleep(random.uniform(0.05, 0.15))
                
                elif self.state == "THINKING":
                    # White/Blue Rotating Spinner (classic loading)
                    for i in range(self.num_pixels):
                        if self.state != "THINKING": break
                        self.pixels.fill((0, 0, 0))
                        # weak background
                        # pixel i is bright white
                        self.pixels[i] = (200, 200, 200) 
                        self.pixels.show()
                        time.sleep(0.1)
                
                else:
                    time.sleep(0.5)

            except Exception as e:
                print(f"[LED Loop Error] {e}")
                time.sleep(1)

led_service = LEDService()

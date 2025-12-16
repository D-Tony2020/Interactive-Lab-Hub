# FridgeMind – Interactive Device Design Final Project

FridgeMind is an interactive smart hardware system designed to help users naturally track food storage, manage refrigerator inventory, and make better meal decisions.  
The project explores how AI-powered perception and generation can be embedded into everyday behaviors through a low-friction, device-centered interaction design.

---

## Team Members
- Xiaocheng Li  
- Haotian Xu  
- Xiang Chang  

## Course
Interactive Device Design

---

## Big Idea
<img width="861" height="1220" alt="51cb3eee2ea4be7ff0700f963a418a3c" src="https://github.com/user-attachments/assets/14f5a484-b9f9-41ea-ad6f-b061d5d4af1e" />

FridgeMind is designed around a simple insight:  
**the best moment to understand food is when people are already interacting with it.**

Rather than asking users to manually scan items or log food through an app, FridgeMind integrates directly into the act of opening the refrigerator and placing food inside. Mounted on the refrigerator door, the device observes food placement, updates inventory automatically, and provides contextual guidance only when needed.

The system combines vision-based recognition, a touchscreen interface, ambient LED feedback, and conversational AI to create a smart assistant that feels more like a part of the refrigerator than a separate device.
<p align="center">
  <img src="https://github.com/user-attachments/assets/b6038c27-4a68-45b2-ab24-e20defa7906e" width="48%" />
  <img src="https://github.com/user-attachments/assets/63a42740-39ef-4180-99f1-3bc9cb0e43e0" width="48%" />
</p>



At the system level, FridgeMind adopts a **hybrid framework combining locally deployed models trained with Teachable Machine and AI APIs with language models**.  
Food recognition models are trained using Teachable Machine and deployed locally on a Raspberry Pi, enabling real-time recognition and inventory logging with low latency and reliability. On top of this local perception layer, AI APIs and language models are used to reason over inventory data and generate meal suggestions. This design keeps core interactions fast and self-contained, while leveraging AI for higher-level reasoning only when appropriate.

---

## Timeline

### Week 1 – Concept Definition & System Architecture
- Identified food waste and food forgetting as core problems
- Explored kitchen interaction scenarios
- Selected the refrigerator door as the primary intervention point
- Defined system architecture and interaction roles
- Conducted early food recognition feasibility tests

### Week 2 – Hardware Setup & Core Interaction Flow
- Integrated camera, touchscreen, Raspberry Pi, LED strip, and audio components
- Implemented recognition → confirmation → inventory update loop
- Built initial UI structure and inventory logic

### Week 3 – Physical Design & AI Integration
- Designed enclosure and refined physical layout
- Integrated conversational AI for meal guidance
- Redesigned LED feedback system to support new interaction states

### Week 4 – Integration, Testing & Final Presentation
- Conducted placement and behavior testing
- Refined interaction timing and feedback
- Recorded final demo video and prepared documentation

---

## Key Interaction Design

### 1. Screen Interaction (UI)

The touchscreen serves as an **information confirmation and visualization layer**, rather than a primary control surface.

Users can:
- Confirm recognized food items
- View current inventory and freshness status
- Read AI-generated meal suggestions

The interface is intentionally minimal to reduce cognitive load and allow quick, glance-based interaction.
<p align="center">
  <img src="https://github.com/user-attachments/assets/239f897b-0a90-4cbb-99b1-8154c3a9709b" width="30%" />
  <img src="https://github.com/user-attachments/assets/0cb5ac94-63f8-4172-b03b-d54dce0ecf10" width="30%" />
  <img src="https://github.com/user-attachments/assets/d26612f9-c5cb-4af6-94e6-af2ffcaaf7a3" width="30%" />
</p>


---

### 2. Visual Recognition (Scanning)

FridgeMind does not continuously scan the inside of the refrigerator.  
Instead, recognition is **triggered by user behavior**—specifically when food is placed in front of the device during normal fridge use.

When an item enters the camera’s field of view:
1. The locally deployed recognition model identifies the food category
2. The detected item appears on the screen
3. The user confirms the result
4. The item is added to inventory

This approach:
- Aligns with natural user behavior
- Reduces privacy concerns
- Avoids unnecessary system noise

Scanning is not treated as a task, but as a natural consequence of everyday action.
<img width="1371" height="840" alt="微信图片_20251201015548_120_1175" src="https://github.com/user-attachments/assets/b64f3f72-f626-4fc0-bc27-f07757556b00" />

---

### 3. Conversational AI Interaction (Language Model)

FridgeMind supports **direct, open-ended user queries through voice interaction**.  
Users can ask questions such as:
- “What can I cook tonight?”
- “Which foods are expiring soon?”
- “What should I use first?”

The system responds using a **combination of spoken feedback and on-screen text**, ensuring accessibility and clarity.  
Voice interaction is used exclusively for **high-level reasoning and guidance**, not for food logging or inventory modification, which helps maintain system reliability and reduces recognition errors.

This design positions the language model as a **decision-support layer**, rather than a control mechanism.

---

### 4. LED Feedback (Ambient Interaction)

An RGB LED strip provides immediate, low-cognitive-load feedback about system state:

- **Blue (dynamic):** AI is listening
- **White (rotating):** AI is processing
- **Purple:** AI is responding
- **Green:** Food recognition successful
- **Red:** Recognition failed

The LED system allows users to understand what the device is doing without reading instructions or focusing on the screen.

---

## Model Making

The physical prototype was developed through iterative stages.

### Stage 1 – Visual Feasibility Testing
The camera was first connected directly to a computer and tested in multiple refrigerator positions.  
Teachable Machine was used to train early recognition models and validate performance under real lighting conditions.
<p align="center">
  <img src="https://github.com/user-attachments/assets/077a563c-bf09-4759-b458-eeb94cd9d161" width="30%" />
  <img src="https://github.com/user-attachments/assets/1ec8c485-1564-449e-bd36-da01e34e40d6" width="30%" />
  <img src="https://github.com/user-attachments/assets/a653bab2-e234-4dd8-8ec6-93e0bbcd2360" width="30%" />
</p>

### Stage 2 – Hardware System Assembly
After confirming visual feasibility, the Raspberry Pi, touchscreen, LED strip, speaker, and camera were integrated into a complete working system.  
The focus at this stage was functional continuity rather than visual polish.
<img width="994" height="743" alt="23a94fc561b93ba4cbe3f63447eb311b" src="https://github.com/user-attachments/assets/8159b393-3ed8-4a1f-aadf-1363babb60d8" />

### Stage 3 – Enclosure and Form Design
With hardware dimensions fixed, enclosure design began. The goal was to keep the device thin and unobtrusive when mounted on a refrigerator door.

Because the camera required physical depth, a **ripple-inspired form language** was used to reinterpret the protrusion.  
The camera area became a visual focal point, symbolizing the system’s primary input rather than appearing as an awkward structural necessity.
![f766d0c51a0f83fe02691161360bcd0f](https://github.com/user-attachments/assets/95f193c4-d7ff-42db-a821-f48b1954027c)
<img width="793" height="1255" alt="6ff5863bf6449f625cee83eab065f71b1" src="https://github.com/user-attachments/assets/e0dd67df-aaff-4a9b-8f9e-2547c80d351f" />

---

## Code & System Implementation

The system is engineered as a tightly integrated hardware-software hybrid, designed for low latency and robust offline capability for core functions.

### 1. Backend Architecture (Python & FastAPI)
The central nervous system is a multi-threaded **FastAPI** server running on the Raspberry Pi.
*   **Vision Service (`vision_service.py`)**: Runs a dedicated background thread for camera capture and inference, decoupling frame acquisition from the API. It utilizes **TensorFlow Lite** for efficient local object detection. To handle real-world noise, it implements a **temporal voting algorithm**—an item must be consistently detected across 15 consecutive frames to be confirmed, ensuring zero false positives from fleeting movements.
*   **Audio Service (`audio_service.py`)**: Manages voice interaction using `SpeechRecognition` and `Pygame` for non-blocking playback. It dynamically adjusts energy thresholds for ambient noise calibration.
*   **Inventory Database**: A persistent **SQLite** database tracks items, expiry dates, and categories, capable of withstanding power cycles.
*   **Hardware Logic**: Custom service modules manage GPIO pins for the LED strip asynchronously, allowing the system to provide physical feedback ("Listening", "Thinking", "Success") without blocking web server responses.

### 2. AI & Voice Pipeline
Cloud and local compute are balanced for optimal performance:
*   **Perception (Local)**: Visual recognition is performed entirely on-device (Edge AI) for privacy and speed.
*   **Reasoning (Cloud)**: Complex queries ("What can I cook?") are routed to **OpenAI GPT-4**, injected with the current inventory/context as a system prompt.
*   **Voice Interaction**: 
    1.  User speaks → **Whisper API** (Speech-to-Text)
    2.  Text processed by **LLM Agent** (Intent Understanding)
    3.  Response generated → **OpenAI TTS-1** (Text-to-Speech) for natural voice feedback.

### 3. Frontend Interface
The display runs a modern **React** Single Page Application (SPA), accessible via the touch screen.
*   **Real-time Polling**: It actively polls the `/api/scan/live` endpoint (800ms intervals) to update the UI instantly when food is recognized.
*   **Visual Logic**: Dynamic CSS animations mirror the physical LED states, creating a unified physical-digital experience.
*   **Dashboard**: Calculates freshness metrics locally (`getDaysRemaining`) to offer instant visual cues (Red/Yellow/Green status indicators).

---

## Placement Testing

FridgeMind was tested on real refrigerators as well as within a simulated fridge structure.

Testing focused on:
- Whether the device interfered with door operation
- Whether users naturally noticed or ignored the device
- Visibility of LED feedback under typical kitchen lighting
- Whether food placement triggered system responses without extra user effort

Results showed that linking system activation to the moment when users open the fridge and move food inward created an intuitive, low-friction interaction that users quickly understood.

---

## Final Video & Demo

The final demo video presents FridgeMind through a complete real-world usage flow, including: https://youtube.com/shorts/d3GhI3BP0K0
- Device placement on a refrigerator door
- Food recognition and inventory updates
- Conversational AI queries and responses
- LED-based system feedback

https://youtube.com/shorts/d3GhI3BP0K0

![9149d43b3cbd2fc510114bd323081ff0](https://github.com/user-attachments/assets/5290b0c6-fafb-4378-b6f4-6b3533e6ff4b)
![4bca42d6caa55e7e554694b8ecaeb825](https://github.com/user-attachments/assets/93b5f447-c62d-492b-a0a4-357caa8177d1)

---

## Reflections on Process

The most challenging aspect of FridgeMind was not implementing individual features, but ensuring that the overall interaction felt **natural, behavior-driven, and unobtrusive**.

As a device-centered design project, this raised a key question:
> How can interaction design help users understand system input and output without demanding attention?

Through this project, our understanding of “AI + Device” design evolved.  
Effective AI does not need to be loud or constantly interactive. Instead, it should work quietly in the background—recognizing food when it is placed down, updating inventory automatically, and offering guidance only when it is useful.

If we were to restart the project, we would explore deeper automation and potentially extend the system boundary to include food purchasing decisions, allowing the device to influence not only storage behavior but longer-term consumption patterns.

---

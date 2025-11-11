# Distributed Interaction

**NAMES OF COLLABORATORS HERE**

For submission, replace this section with your documentation!

---

## Prep

1. Pull the new changes
2. Read: [The Presence Table](https://dl.acm.org/doi/10.1145/1935701.1935800) ([video](https://vimeo.com/15932020))

## Overview

Build interactive systems where **multiple devices communicate over a network** using MQTT messaging. Work in teams of 3+ with Raspberry Pis.

**Parts:**
- A: Learn MQTT messaging
- B: Try collaborative pixel grid demo  
- C: Build your own distributed system

---

## Part A: MQTT Messaging

MQTT = lightweight messaging for IoT. Publish/subscribe model with central broker.

**Concepts:**
- **Broker**: `farlab.infosci.cornell.edu:1883`
- **Topic**: Like `IDD/bedroom/temperature` (use `#` wildcard)
- **Publish/Subscribe**: Send and receive messages

**Install MQTT tools on your Pi:**
```bash
sudo apt-get update
sudo apt-get install -y mosquitto-clients
```
<img width="870" height="576" alt="image" src="https://github.com/user-attachments/assets/a21c69e4-17fd-40c1-8a22-1ae1a7ff48a7" />

**Test it:**

**Subscribe to messages (listener):**
```bash
mosquitto_sub -h farlab.infosci.cornell.edu -p 1883 -t 'IDD/#' -u idd -P 'device@theFarm'
```

**Publish a message (sender):**
```bash
mosquitto_pub -h farlab.infosci.cornell.edu -p 1883 -t 'IDD/test/yourname' -m 'Hello!' -u idd -P 'device@theFarm'
```

> **💡 Tips:**
> - Replace `yourname` with your actual name in the topic
> - Use single quotes around the password: `'device@theFarm'`

**🔧 Debug Tool:** View all MQTT messages in real-time at `http://farlab.infosci.cornell.edu:5001`

<img width="878" height="946" alt="image" src="https://github.com/user-attachments/assets/22ae5e45-5ee6-4c9b-ae5b-4635376f7469" />

**💡 Brainstorm 5 ideas for messaging between devices**
1. Distributed Classroom Emotion Wall
Each desk is equipped with a strip of LEDs and a simple input device (such as buttons or touch sensors). Students can press buttons to express their current state (e.g., ✅ “Understood,” ❓ “Confused,” 😴 “Tired”). The device broadcasts these signals via MQTT, and a central server (or display) calculates the real-time emotional heatmap of the class. The system visualizes this using a color spectrum — green for high comprehension, yellow for neutral, and red for widespread confusion.

2. Cloud-Based Ecological Co-Nurturing System
Each device is connected to a plant or environmental sensors (for light, humidity, temperature, etc.). Devices share their local environmental parameters through MQTT to compute a Collective Ecological Balance Index. When one location becomes too dry or too dark, others automatically adjust their water pumps or lighting to compensate — creating a “mutual-aid ecosystem” that dynamically maintains group equilibrium.

3. Sensory Symphony
Each device acts as a sensory instrument:

One controls sound (speaker/buzzer)

One controls light (RGB LED ring)

One controls airflow (small fan or motor)

These devices exchange sensory events through MQTT. For example, light intensity may trigger pitch changes; wind speed may control light flicker frequency; the sound spectrum may modulate wind strength. The result is a real-time, interdependent symphony of physical, visual, and auditory interactions.

4. Random Narrative Machine
Each device continuously generates short “fragmented verses” or “audio snippets” and sends them via MQTT to another randomly selected device. The receiving device remixes or rearranges the fragments into new sentences or noise patterns, then retransmits them. The messages never disappear — they keep transforming, circulating, and regenerating across the network, forming an endless web of evolving narratives.

5. Phantom Swarm
Each device drives a small mechanical module (e.g., a servo motor + LED) that simulates a “luminous insect.” Through MQTT, these modules sense their neighbors’ motion states and energy levels. When one device flashes, nearby ones react instantly with startled flickers, producing a spatially dynamic electric swarm. In a dark room, dozens of tiny lights will pulse, ripple, and echo in intricate rhythms — like a colony of breathing electronic organisms.
---

## Part B: Collaborative Pixel Grid

Each Pi = one pixel, controlled by RGB sensor, displayed in real-time grid.

**Architecture:** `Pi (sensor) → MQTT → Server → Web Browser`

**Setup:**

1. **Sensor**

#### Light/Proximity/Gesture sensor (APDS-9960)
We use this sensor [Adafruit APDS-9960](https://www.adafruit.com/product/3595) for this exmaple to detect light (also RGB)
 
<img src="https://cdn-shop.adafruit.com/970x728/3595-06.jpg" width=200>

Connect it to your pi with Qwiic connector


<img src="imgs/IMG_0270.jpg" height="200" />
We need to use the screen to display the color detection, so we need to stop the running piscreen.service to make your screen available again

```bash
# stop the screen service
sudo systemctl stop piscreen.service
```

if you want to restart the screen service
```bash
# start the screen service
sudo systemctl start piscreen.service
```
 
2. **Server** (one person on laptop):
```bash
cd "Lab 6"  
source .venv/bin/activate
pip install -r requirements-server.txt
python app.py
```

2. **View in browser:**
   - Grid: `http://farlab.infosci.cornell.edu:5000`
   - Controller: `http://farlab.infosci.cornell.edu:5000/controller`

3. **Pi publisher** (everyone on their Pi):
```bash
# First time setup - create virtual environment
cd "Lab 6"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-pi.txt

# Run the publisher
python pixel_grid_publisher.py
```

Hold colored objects near sensor to change your pixel!

![Pixel grid with two devices](imgs/two-devices-grid.png)

**📸 Include: Screenshot of grid + photo of your Pi setup**
![ff68932d89c596e1c678c6ca4bc87891](https://github.com/user-attachments/assets/a0b7760e-27ab-44d1-8f45-ee9775209d0f)
![0016c6b910f2244e8fb10bb61bdac60c](https://github.com/user-attachments/assets/7e561420-6540-4ba2-98e9-c75dcbd8c9b8)
![97e2149784283ccac4e9a6429d5f5323](https://github.com/user-attachments/assets/7cb1e7ff-a5df-4abc-8ded-ce866404c936)
![99bf15160dfe2bafe7737e339902c57b](https://github.com/user-attachments/assets/50511415-ac93-468b-8a05-4c1b2bb54e48)
![8dbca9db22c33f8886969365e9635c7b](https://github.com/user-attachments/assets/9569f8bf-7857-4e0b-a51b-1cd6a932fd9a)
![743da4b8cd0d796474629e8be968484c](https://github.com/user-attachments/assets/426ce3bf-56a3-41cc-ac85-b9dfb6c63a8b)

---

## Part C: Make Your Own

**Requirements:**
- 3+ people, 3+ Pis
- Each Pi contributes sensor input via MQTT
- Meaningful or fun interaction

**Ideas:**

**Sensor Fortune Teller**
- Each Pi sends 0-255 from different sensor
- Server generates fortunes from combined values

**Frankenstories**
- Sensor events → story elements (not text!)
- Red = danger, gesture up = climbed, distance <10cm = suddenly

**Distributed Instrument**
- Each Pi = one musical parameter
- Only works together

**Others:** Games, presence display, mood ring

### Deliverables

Replace this README with your documentation:

**1. Project Description**
- What does it do? Why interesting? User experience?

**2. Architecture Diagram**
- Hardware, connections, data flow
- Label input/computation/output

**3. Build Documentation**
- Photos of each Pi + sensors
- MQTT topics used
- Code snippets with explanations

**4. User Testing**
- **Test with 2+ people NOT on your team**
- Photos/video of use
- What did they think before trying?
- What surprised them?
- What would they change?

**5. Reflection**
- What worked well?
- Challenges with distributed interaction?
- How did sensor events work?
- What would you improve?

---

## Code Files

**Server files:**
- `app.py` - Pixel grid server (Flask + WebSocket + MQTT)
- `mqtt_viewer.py` - MQTT message viewer for debugging
- `mqtt_bridge.py` - MQTT → WebSocket bridge
- `requirements-server.txt` - Server dependencies

**Pi files:**
- `pixel_grid_publisher.py` - Example (RGB sensor → MQTT)
- `requirements-pi.txt` - Pi dependencies

**Web interface:**
- `templates/grid.html` - Pixel grid display
- `templates/controller.html` - Color picker
- `templates/mqtt_viewer.html` - Message viewer

---

## Debugging Tools

**MQTT Message Viewer:** `http://farlab.infosci.cornell.edu:5001`
- See all MQTT messages in real-time
- View topics and payloads
- Helpful for debugging your own projects

**Command line:**
```bash
# See all IDD messages
mosquitto_sub -h farlab.infosci.cornell.edu -p 1883 -t "IDD/#" -u idd -P "device@theFarm"
```

---

## Troubleshooting

**MQTT:** Broker `farlab.infosci.cornell.edu:1883`, user `idd`, pass `device@theFarm`

**Sensor:** Check `i2cdetect -y 1`, APDS-9960 at `0x39`

**Grid:** Verify server running, check MQTT in console, test with web controller

**Pi venv:** Make sure to activate: `source .venv/bin/activate`


---

## Submission Checklist

Before submitting:
- [ ] Delete prep/instructions above
- [ ] Add YOUR project documentation
- [ ] Include photos/videos/diagrams  
- [ ] Document user testing with non-team members
- [ ] Add reflection on learnings
- [ ] List team names at top

**Your README = story of what YOU built!**

---

Resources: [MQTT Guide](https://www.hivemq.com/mqtt-essentials/) | [Paho Python](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php) | [Flask-SocketIO](https://flask-socketio.readthedocs.io/)

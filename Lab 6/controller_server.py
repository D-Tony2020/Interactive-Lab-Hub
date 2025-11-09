from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt
import threading, json, time

# ===== MQTT 配置 =====
BROKER = "farlab.infosci.cornell.edu"
PORT = 1883
USER, PW = "idd", "device@theFarm"
TOPIC_STATUS = "IDD/hall/smartlight/status/#"
TOPIC_EVENT = "IDD/hall/smartlight/event/#"
TOPIC_CMD = "IDD/hall/smartlight/cmd/"

# ===== 全局状态缓存 =====
devices = {}   # {device_id: {...}}

# ===== Flask 初始化 =====
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# ===== MQTT 客户端初始化 =====
client = mqtt.Client()
client.username_pw_set(USER, PW)

def on_message(client, userdata, msg):
    topic = msg.topic
    data = json.loads(msg.payload.decode())
    dev_id = data.get("device_id", "unknown")

    if "status" in topic:
        devices[dev_id] = data
        print(f"[STATUS] {dev_id}: mode={data['mode']} | light={'ON' if data['light_on'] else 'OFF'}")
        socketio.emit("update_status", {"device_id": dev_id, "data": data})
    elif "event" in topic:
        print(f"[EVENT] {dev_id}: {data}")
        socketio.emit("new_event", {"device_id": dev_id, "event": data})

# ✅ 连接并启用非阻塞循环
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC_STATUS)
client.subscribe(TOPIC_EVENT)
client.loop_start()   # ✅ 关键


threading.Thread(target=mqtt_loop, daemon=True).start()

# ===== MQTT 发送命令 =====
def send_command(dev_id, payload):
    topic = TOPIC_CMD + dev_id
    client.publish(topic, json.dumps(payload), qos=1)
    print(f"[CMD] {dev_id} -> {payload}")

# ===== Flask 路由 =====
@app.route("/")
def index():
    return render_template("dashboard.html", devices=devices)

@app.route("/set_param", methods=["POST"])
def set_param():
    data = request.json
    dev_id = data["device_id"]
    payload = data["payload"]
    send_command(dev_id, payload)
    return jsonify({"ok": True})

@app.route("/broadcast", methods=["POST"])
def broadcast():
    data = request.json
    for dev in devices.keys():
        send_command(dev, data)
    return jsonify({"ok": True, "msg": f"Broadcast to {len(devices)} devices"})

# ===== 启动服务 =====
if __name__ == "__main__":
    print("Controller Dashboard running on http://0.0.0.0:5000")
    socketio.run(app, host="0.0.0.0", port=5000)

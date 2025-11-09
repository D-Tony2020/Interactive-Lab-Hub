from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json, time

# ===== MQTT 配置 =====
BROKER = "farlab.infosci.cornell.edu"
PORT = 1883
USER, PW = "idd", "device@theFarm"
TOPIC_STATUS = "IDD/hall/smartlight/status/#"
TOPIC_EVENT  = "IDD/hall/smartlight/event/#"
TOPIC_CMD    = "IDD/hall/smartlight/cmd/"

# ===== 全局状态缓存 =====
devices = {}

# ===== Flask 初始化 =====
app = Flask(__name__)

# ✅ 启用稳定模式的 SocketIO（延长心跳、兼容局域网）
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading",
    ping_timeout=60,      # 等待客户端 pong 的最长时间
    ping_interval=25      # 心跳间隔，默认5，这里延长
)

# ===== MQTT 客户端初始化 =====
client = mqtt.Client()
client.username_pw_set(USER, PW)

# ===== MQTT 回调函数 =====
def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected to {BROKER} with result code {rc}")
    client.subscribe(TOPIC_STATUS)
    client.subscribe(TOPIC_EVENT)
    print(f"[MQTT] Subscribed to {TOPIC_STATUS} and {TOPIC_EVENT}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        dev_id = data.get("device_id", "unknown")

        # 处理状态上报
        if "status" in msg.topic:
            devices[dev_id] = data
            print(f"[STATUS] {dev_id}: mode={data['mode']} | "
                  f"light={'ON' if data['light_on'] else 'OFF'} | "
                  f"sound={data['sound_thresh']} | motion={data['motion_thresh']:.3f}")
            socketio.emit("update_status",
                          {"device_id": dev_id, "data": data},
                          broadcast=True)

        # 处理事件上报
        elif "event" in msg.topic:
            print(f"[EVENT] {dev_id}: {data}")
            socketio.emit("new_event",
                          {"device_id": dev_id, "event": data},
                          broadcast=True)

    except Exception as e:
        print("[ERROR] Failed to parse MQTT message:", e)
        print("  Raw payload:", msg.payload)

client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_start()   # ✅ 非阻塞 MQTT 循环（与 Flask 共存）

# ===== Flask 路由 =====
@app.route("/")
def index():
    return render_template("dashboard.html", devices=devices)

# 单设备参数设置
@app.route("/set_param", methods=["POST"])
def set_param():
    data = request.json
    dev_id = data["device_id"]
    payload = data["payload"]
    topic = TOPIC_CMD + dev_id
    client.publish(topic, json.dumps(payload), qos=1)
    print(f"[CMD] Sent to {dev_id}: {payload}")
    socketio.emit("new_event",
                  {"device_id": dev_id, "event": {"type": "cmd_sent", "payload": payload}},
                  broadcast=True)
    return jsonify({"ok": True})

# 群发命令
@app.route("/broadcast", methods=["POST"])
def broadcast():
    data = request.json
    for dev in list(devices.keys()):
        topic = TOPIC_CMD + dev
        client.publish(topic, json.dumps(data), qos=1)
        print(f"[BROADCAST] -> {dev}: {data}")
    socketio.emit("new_event",
                  {"device_id": "ALL", "event": {"type": "broadcast", "payload": data}},
                  broadcast=True)
    return jsonify({"ok": True, "msg": f"Broadcasted to {len(devices)} devices"})

# ===== 主程序入口 =====
if __name__ == "__main__":
    print("🚀 Controller Dashboard running on http://0.0.0.0:5000")
    socketio.run(app, host="0.0.0.0", port=5000)

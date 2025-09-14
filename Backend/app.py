import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import json
import math

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

DATABASE_NAME = 'transit.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- Fleet Analysis ---
def analyze_fleet_status(buses_list):
    """Detect bus bunching and add recommendations."""
    BUNCHING_THRESHOLD = 0.0015
    buses_by_route = {}

    for bus in buses_list:
        bus['status'] = "On Time"
        bus['recommendation'] = "None"
        buses_by_route.setdefault(bus['route_id'], []).append(bus)

    for route_id, buses_on_route in buses_by_route.items():
        if len(buses_on_route) > 1:
            buses_on_route.sort(
                key=lambda b: b['path_index'],
                reverse=(buses_on_route[0]['direction'] == -1)
            )

            for i in range(len(buses_on_route) - 1):
                front_bus = buses_on_route[i]
                back_bus = buses_on_route[i + 1]

                dist = math.dist(
                    (front_bus['lat'], front_bus['lng']),
                    (back_bus['lat'], back_bus['lng'])
                )

                if dist < BUNCHING_THRESHOLD:
                    front_bus['status'] = "Bunched"
                    back_bus['status'] = "Bunched"
                    back_bus['recommendation'] = "Hold at next stop for 60s"

    return buses_list

# --- Broadcast to frontend ---
def broadcast_latest_data():
    conn = get_db_connection()
    query = """
        SELECT b.*, r.name as route_name, r.path as route_path
        FROM buses b
        JOIN routes r ON b.route_id = r.id
    """
    buses_rows = conn.execute(query).fetchall()
    alerts_rows = conn.execute("SELECT * FROM alerts").fetchall()
    conn.close()

    buses_data = []
    for row in buses_rows:
        bus_dict = dict(row)
        route_path = json.loads(bus_dict["route_path"])

        next_stop_index = bus_dict["path_index"]
        if 0 <= next_stop_index < len(route_path):
            bus_dict["next_stop"] = route_path[next_stop_index]["stop"]
            next_stop_coord = route_path[next_stop_index]["coord"]

            dist = math.dist(
                (bus_dict["lat"], bus_dict["lng"]),
                (next_stop_coord[0], next_stop_coord[1])
            )
            bus_dict["eta"] = int(dist * 50000)  # heuristic ETA
        else:
            bus_dict["next_stop"] = "End of Line"
            bus_dict["eta"] = 0

        buses_data.append(bus_dict)

    buses_with_status = analyze_fleet_status(buses_data)

    alerts_data = [dict(row) for row in alerts_rows]

    # ✅ EMOJI feature added here
    for alert in alerts_data:
        if alert["type"] == "bunching":
            alert["emoji"] = "🚨"
        elif alert["type"] == "delay":
            alert["emoji"] = "⏳"
        elif alert["type"] == "maintenance":
            alert["emoji"] = "🛠️"
        elif alert["type"] == "reroute":
            alert["emoji"] = "🛣️"
        else:
            alert["emoji"] = "ℹ️"

    socketio.emit('update_data', {'buses': buses_with_status, 'alerts': alerts_data})
    print("📡 Broadcasted buses + alerts with emoji")

# --- API Endpoints ---
@app.route("/api/performance")
def get_performance():
    conn = get_db_connection()
    total_buses_count = conn.execute("SELECT COUNT(*) FROM buses").fetchone()[0]
    on_time_count = conn.execute("SELECT COUNT(*) FROM buses WHERE status = 'On Time'").fetchone()[0]
    on_time_rate = (on_time_count / total_buses_count) * 100 if total_buses_count > 0 else 0

    avg_occupancy = conn.execute("SELECT AVG(occupancy) FROM buses").fetchone()[0]
    avg_occupancy = avg_occupancy * 100 if avg_occupancy else 0

    active_alerts_count = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
    conn.close()

    return jsonify({
        "stats": {
            "totalBuses": total_buses_count,
            "onTimeRate": round(on_time_rate, 1),
            "passengerCapacity": round(avg_occupancy, 1),
            "activeAlerts": active_alerts_count,
        },
        "optimization": {"before": [12.5, 85, 78], "after": [8.2, 94, 91]},
        "forecast": [120, 135, 140, 160, 180, 175, 150, 130, 110],
        "demographics": {"labels": ["Students", "Professionals", "Seniors", "Tourists"], "data": [45, 30, 15, 10]},
    })

@app.route("/api/bus/update", methods=["POST"])
def receive_bus_update():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        "UPDATE buses SET lat=?, lng=?, occupancy=?, path_index=?, direction=? WHERE id=?",
        (data["lat"], data["lng"], data["occupancy"], data["path_index"], data["direction"], data["id"]),
    )
    conn.commit()
    conn.close()
    broadcast_latest_data()
    return jsonify({"success": True}), 200

@app.route("/api/alert/create", methods=["POST"])
def create_alert():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute("INSERT INTO alerts (type, route, message) VALUES (?,?,?)", (data["type"], data["route"], data["message"]))
    conn.commit()
    conn.close()
    broadcast_latest_data()
    return jsonify({"success": True}), 201

# --- WebSocket Events ---
@socketio.on("connect")
def handle_connect():
    print("🔌 Client connected")
    broadcast_latest_data()

# --- Main ---
if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)

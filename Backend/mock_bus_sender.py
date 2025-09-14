import requests
import random
import time
import sqlite3
import json
import math

# ---------------- CONFIG ---------------- #
SERVER_URL = "http://127.0.0.1:5000"
UPDATE_ENDPOINT = "/api/bus/update"
ALERT_ENDPOINT = "/api/alert/create"
DATABASE_NAME = 'transit.db'

BASE_BUS_SPEED = 0.0003      # Base step for bus movement
BUNCHING_THRESHOLD = 0.0015  # Approx distance in lat/lng degrees
UPDATE_INTERVAL = 3          # Seconds between updates

# ---------------- DB FETCH ---------------- #
def get_initial_data_from_db():
    """Fetch buses & routes from SQLite DB."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row

        buses_rows = conn.execute('SELECT * FROM buses').fetchall()
        routes_rows = conn.execute('SELECT * FROM routes').fetchall()

        conn.close()

        buses = {bus['id']: dict(bus) for bus in buses_rows}
        routes = {route['id']: {"name": route['name'], "path": json.loads(route['path'])} for route in routes_rows}

        return buses, routes
    except sqlite3.Error as e:
        print(f"❌ DB Error: {e}")
        return {}, {}

# ---------------- ALERTS ---------------- #
def send_alert(alert_type, route_id, message):
    """Send alert to backend."""
    alert_data = {"type": alert_type, "route": str(route_id), "message": message}
    try:
        requests.post(f"{SERVER_URL}{ALERT_ENDPOINT}", json=alert_data)
        print(f"⚠️ Sent alert: {message}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error when sending alert.")

def check_bunching(fleet_state):
    """Detect bus bunching on each route."""
    buses_by_route = {}
    for bus in fleet_state.values():
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

                distance = math.dist(
                    [front_bus['lat'], front_bus['lng']],
                    [back_bus['lat'], back_bus['lng']]
                )

                if distance < BUNCHING_THRESHOLD:
                    send_alert("bunching", route_id,
                               f"Bunching detected: Bus #{back_bus['id']} and Bus #{front_bus['id']} on Route {route_id}")

def maybe_send_random_alert(fleet_state):
    """Send random alert occasionally."""
    if random.random() < 0.01:  # 1% chance each cycle
        bus = random.choice(list(fleet_state.values()))
        alert_types = {
            "reroute": f"Bus #{bus['id']} on Route {bus['route_id']} rerouted due to road closure.",
            "delay": f"Bus #{bus['id']} on Route {bus['route_id']} is delayed.",
            "maintenance": f"Bus #{bus['id']} on Route {bus['route_id']} has a mechanical issue."
        }
        alert_type, message = random.choice(list(alert_types.items()))
        send_alert(alert_type, bus['route_id'], message)

# ---------------- SIMULATION ---------------- #
def simulate_fleet():
    """Main simulation loop."""
    fleet_state, routes = get_initial_data_from_db()
    if not fleet_state or not routes:
        print("❌ Could not load buses or routes. Exiting.")
        return

    print(f"✅ Starting simulation for {len(fleet_state)} buses. Press Ctrl+C to stop.")

    while True:
        check_bunching(fleet_state)
        maybe_send_random_alert(fleet_state)

        for bus_id, bus in fleet_state.items():
            route = routes[bus['route_id']]
            path = route['path']

            current_speed = BASE_BUS_SPEED * (1.5 if bus_id == 102 else 1.0)

            target_index = bus['path_index']
            target_stop = path[target_index]
            target_lat, target_lng = target_stop['coord']

            dy = target_lat - bus['lat']
            dx = target_lng - bus['lng']
            distance = math.sqrt(dx**2 + dy**2)

            if distance < current_speed:
                # Reached stop
                bus['lat'], bus['lng'] = target_lat, target_lng
                next_index = bus['path_index'] + bus['direction']
                if not (0 <= next_index < len(path)):
                    bus['direction'] *= -1
                    next_index = bus['path_index'] + bus['direction']
                bus['path_index'] = next_index
            else:
                # Move towards next stop
                bus['lat'] += (dy / distance) * current_speed
                bus['lng'] += (dx / distance) * current_speed

            # Simulate occupancy change
            bus['occupancy'] = max(0.1, min(0.98, bus['occupancy'] + random.uniform(-0.05, 0.05)))

            update_data = {
                "id": bus_id,
                "lat": round(bus['lat'], 6),
                "lng": round(bus['lng'], 6),
                "occupancy": round(bus['occupancy'], 2),
                "path_index": bus['path_index'],
                "direction": bus['direction']
            }

            try:
                requests.post(f"{SERVER_URL}{UPDATE_ENDPOINT}", json=update_data)
                print(f"🚌 Updated Bus #{bus_id} at ({update_data['lat']}, {update_data['lng']})")
            except requests.exceptions.ConnectionError:
                print(f"❌ Connection Error for Bus #{bus_id}, retrying later.")
                time.sleep(2)
                continue

        print("✅ Fleet update cycle complete.\n")
        time.sleep(UPDATE_INTERVAL)

# ---------------- RUN ---------------- #
if __name__ == '__main__':
    simulate_fleet()

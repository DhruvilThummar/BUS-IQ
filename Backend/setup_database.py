import sqlite3
import json

DATABASE_NAME = 'transit.db'

def setup_database():
    """
    Connects to the database, creates tables (including a new 'routes' table),
    clears existing data, and populates them with a new, larger fleet and defined routes.
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    print("Database connection established.")

    # --- Drop existing tables for a clean setup ---
    cursor.execute("DROP TABLE IF EXISTS buses")
    cursor.execute("DROP TABLE IF EXISTS routes")
    cursor.execute("DROP TABLE IF EXISTS alerts")
    print("Dropped existing tables for a clean reset.")

    # --- Create Routes Table ---
    # This table stores route information, including the path (as a JSON string of stops and coordinates).
    cursor.execute('''
    CREATE TABLE routes (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        path TEXT NOT NULL 
    )
    ''')
    print("Routes table created.")

    # --- Create Buses Table with New Columns for Tracking ---
    # path_index: The index of the next waypoint in the route's path the bus is heading towards.
    # direction: 1 for forward, -1 for backward along the path.
    cursor.execute('''
    CREATE TABLE buses (
        id INTEGER PRIMARY KEY,
        route_id INTEGER NOT NULL,
        lat REAL NOT NULL,
        lng REAL NOT NULL,
        occupancy REAL NOT NULL,
        path_index INTEGER NOT NULL,
        direction INTEGER NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (route_id) REFERENCES routes (id)
    )
    ''')
    print("Buses table with tracking columns created.")

    # --- Create Alerts Table ---
    cursor.execute('''
    CREATE TABLE alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        route TEXT NOT NULL,
        message TEXT NOT NULL
    )
    ''')
    print("Alerts table created.")

    # --- Insert Route Data with Stops ---
    # The path is a JSON string containing a list of objects, each with a stop name and coordinates.
    routes_to_add = [
        (5, 'Route 5 - Downtown Loop', json.dumps([
            {"stop": "Union Station", "coord": [34.0522, -118.2437]},
            {"stop": "Grand Park", "coord": [34.056, -118.2457]},
            {"stop": "Music Center", "coord": [34.058, -118.2497]},
            {"stop": "Financial District", "coord": [34.051, -118.2547]},
            {"stop": "Pershing Square", "coord": [34.048, -118.2517]},
        ])),
        (12, 'Route 12 - Civic Center Line', json.dumps([
            {"stop": "City Hall", "coord": [34.0600, -118.2450]},
            {"stop": "Cathedral Plaza", "coord": [34.0630, -118.2480]},
            {"stop": "Art Museum", "coord": [34.0650, -118.2520]},
        ]))
    ]
    cursor.executemany("INSERT INTO routes (id, name, path) VALUES (?, ?, ?)", routes_to_add)
    print(f"Successfully inserted {len(routes_to_add)} new routes.")

    # --- Insert Fleet Data with Initial Progress ---
    # Buses are assigned a route_id. Their starting lat/lng matches a waypoint on their route.
    # path_index is set to 1, meaning they are all heading towards the second stop on their route.
    buses_to_add = [
        # Route 5 buses
        (101, 5, 34.0522, -118.2437, 0.45, 1, 1, 'On Time'),
        (102, 5, 34.056, -118.2457, 0.60, 2, 1, 'On Time'),
        (103, 5, 34.051, -118.2547, 0.50, 4, 1, 'On Time'),
        # Route 12 buses
        (201, 12, 34.0600, -118.2450, 0.30, 1, 1, 'On Time'),
        (202, 12, 34.0630, -118.2480, 0.40, 2, 1, 'On Time')
    ]
    cursor.executemany("INSERT INTO buses (id, route_id, lat, lng, occupancy, path_index, direction, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", buses_to_add)
    print(f"Successfully inserted {len(buses_to_add)} new buses.")

    # Insert a sample initial alert
    cursor.execute("INSERT INTO alerts (type, route, message) VALUES ('delay', '5', 'Initial system alert: Minor traffic downtown.')")
    print("Inserted initial sample alert.")

    # Save (commit) the changes and close the connection
    connection.commit()
    connection.close()
    print("Database transit.db created and populated successfully.")

if __name__ == '__main__':
    setup_database()
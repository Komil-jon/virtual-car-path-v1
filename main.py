import os
import time
import datetime
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

USERNAME = "look"
PASSWORD = "eternal"

# Create Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

print("✅ Action: Flask App Created")

def convert_objectid(data):
    if isinstance(data, dict):
        return {key: convert_objectid(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)  # Convert ObjectId to string
    return data

def get_mongo_client():
    """Returns a MongoDB client connected to the virtual_path database."""
    connection_string = f"mongodb+srv://{USERNAME}:{PASSWORD}@core.pur20xh.mongodb.net/?appName=Core"
    client = MongoClient(connection_string)
    return client

def get_latest_update():
    """Get the latest update from the database."""
    client = get_mongo_client()
    db = client['virtual_path']
    collection = db['car_path']
    latest_record = collection.find_one(sort=[("update_id", -1)])  # Get the latest item
    return latest_record if latest_record else None

def get_update_by_id(update_id):
    """Fetch an update by its update_id."""
    client = get_mongo_client()
    db = client['virtual_path']
    collection = db['car_path']
    update_record = collection.find_one({"update_id": update_id})
    print(update_record)
    return update_record

def get_latest_updates(limit=20):
    """Fetch the latest 'limit' updates from the database."""
    client = get_mongo_client()
    db = client['virtual_path']
    collection = db['car_path']
    updates = list(collection.find().sort("update_id", -1).limit(limit))  # Get the latest 'limit' items
    return updates

def database_insert(record):
    """Insert a record into the MongoDB collection."""
    client = get_mongo_client()
    db = client['virtual_path']
    collection = db['car_path']
    collection.insert_one(record)

def generate_car_update(update_id, last_stop_position, update):
    """Generate a car update record."""
    return {
        "time": datetime.datetime.utcnow().isoformat() + "Z",
        "update_id": update_id,
        "car_id": "CAR_1",
        "position": update["current_position"],  # Example: (x, y, z)
        "average_speed": update["average_speed"],
        "battery_level": update["battery_level"],
        "car_status": update["car_status"],  # Example: "active", "idle", etc.
        "heading": update["heading"],
        "fuel_level": update["fuel_level"],
        "temperature": update["temperature"],
        "gps_accuracy": update["gps_accuracy"],
        "last_stop_location": last_stop_position
    }

@app.route("/")
def index():
    """Serve the core HTML file."""
    return send_file('templates/core.html')

@app.route("/update", methods=["POST"])
def update_database():
    """Handle incoming car location updates."""
    update = request.get_json()

    last_update = get_latest_update()
    record = generate_car_update(last_update["update_id"] + 1, last_update["position"], update)
    database_insert(record)
    return jsonify({"message": "Car locations on the database updated successfully"}), 200

@app.route("/api/get", methods=["GET"])
def get_car_update():
    """Fetch a car update based on the update_id."""
    update_id = request.args.get('update_id', type=int)

    if not update_id:
        return jsonify({"message": "Missing or invalid 'update_id' parameter"}), 400

    # Fetch the update from the database
    update_record = get_update_by_id(update_id + 1)
    update_record = convert_objectid(update_record)

    if update_record:
        return jsonify(update_record), 200
    else:
        return jsonify({"message": f"No update found with update_id {update_id}"}), 404

@app.route("/api/all")
def get_all_updates():
    connection_string = f"mongodb+srv://{USERNAME}:{PASSWORD}@core.pur20xh.mongodb.net/?appName=Core"
    client = MongoClient(connection_string)
    db = client['virtual_path']
    collection = db['car_path']
    
    # Fetch the latest 20 updates
    updates = list(collection.find().sort("update_id", -1).limit(20))
    
    # Convert ObjectId fields to strings
    updates = convert_objectid(updates)
    
    # Return the updates as a JSON response
    return jsonify(updates), 200

def main():
    """Start the Flask server."""
    print("🚀 Starting server...")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8000)), debug=True)

if __name__ == "__main__":
    main()

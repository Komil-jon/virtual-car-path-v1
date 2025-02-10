import random
import datetime
from pymongo import MongoClient

# MongoDB Connection Function
def database_insert(record):
    USERNAME = "look"
    PASSWORD = "eternal"
    
    connection_string = f"mongodb+srv://{USERNAME}:{PASSWORD}@core.pur20xh.mongodb.net/?appName=Core"
    client = MongoClient(connection_string)
    db = client['virtual_path']
    collection = db['car_path']
    collection.insert_one(record)

# Function to Generate a Simulated Car Update
def generate_car_update(update_id):
    return {
        "time": datetime.datetime.utcnow().isoformat() + "Z",
        "update_id": update_id,
        "car_id": "CAR_1",
        "position": {
            "x": round(random.uniform(-180, 180), 6),
            "y": round(random.uniform(-90, 90), 6),
            "z": round(random.uniform(0, 50), 2)
        },
        "average_speed": round(random.uniform(0, 120), 2),
        "battery_level": random.randint(0, 100),
        "car_status": random.choice(["active", "idle", "charging", "offline"]),
        "heading": round(random.uniform(0, 360), 2),
        "fuel_level": random.randint(0, 100),
        "temperature": {
            "engine": round(random.uniform(50, 100), 2),
            "cabin": round(random.uniform(15, 30), 2)
        },
        "gps_accuracy": round(random.uniform(0.1, 5), 2),
        "last_stop_location": {
            "x": round(random.uniform(-180, 180), 6),
            "y": round(random.uniform(-90, 90), 6),
            "z": round(random.uniform(0, 50), 2)
        }
    }

# Insert 100 Simulated Records into MongoDB
for i in range(1, 101):
    record = generate_car_update(i)
    database_insert(record)
    print(f"Inserted record {i}")

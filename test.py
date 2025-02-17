import time
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

# Function to Fetch Current Temperature in London
def fetch_outside_temperature():
    return 10.0  # Placeholder temperature in Celsius

def fetch_motor_temperature():
    return 15.0

def fetch_humidity():
    return 30.0

def fetch_pressure():
    return 10.13

def fetch_radiation():
    return 4.0

# Adjust heading to allow negative values instead of 357° using -3°
def adjust_heading(heading):
    return heading - 360 if heading > 180 else heading

# Function to Generate a Simulated Car Update
def generate_car_update(update_id, start_time, start_position, start_battery, start_heading):
    # Fetch current temperature in London
    current_temp = fetch_outside_temperature()
    
    # Calculate realistic movement for 5-second intervals
    speed = round(random.uniform(1.0, 2.0), 2)  # Speed in meters per second
    distance = speed * 5 * 3.6 # Distance covered in 5 seconds (max ~10 meters), 3.6 for m/s to km/h
    
    heading = adjust_heading((random.uniform(-3, 3)) % 360)  # Small change in heading for natural movement
    rad_heading = heading * (3.14159265 / 180)  # Convert to radians

    # Simulate realistic movement (convert meters to lat/lon changes)
    new_position = {
        "x": start_position["x"] + (distance * 0.000008 * random.uniform(0.9, 1.1)),  # Small lateral movement
        "y": start_position["y"] + (distance * 0.000008 * random.uniform(0.9, 1.1)),
        "z": start_position["z"]  # Assuming flat terrain
    }
    
    # Ensure positions are within valid ranges
    new_position["x"] = max(-180, min(180, new_position["x"]))
    new_position["y"] = max(-90, min(90, new_position["y"]))

    # Decrease battery level (slower than before to match a toy car's battery drain rate)
    battery_level = max(0, start_battery - random.uniform(0.05, 0.2))  # 0.05% - 0.2% decrease every 5 sec

    return {
        "time": (start_time + datetime.timedelta(seconds=update_id * 5)).isoformat() + "Z",
        "update_id": update_id,
        "car_id": "CAR_1",
        "position": new_position,
        "average_speed": speed,
        "battery_level": battery_level,
        "humidity": fetch_humidity(),
        "pressure": fetch_pressure(),
        "radiation": fetch_radiation(),
        "car_status": "active" if battery_level > 0 else "offline",
        "heading": heading,
        "fuel_level": 50,  # Constant fuel level (for simulation)
        "temperature": {
            "engine": fetch_motor_temperature(),  # Engine is slightly warmer
            "outside": fetch_outside_temperature()    # Cabin temperature close to ambient
        },
        "gps_accuracy": round(random.uniform(0.1, 1.0), 2),  # Improved GPS accuracy
        "last_stop_location": start_position if update_id == 1 else None  # First update has last stop as start
    }

# Initial conditions
start_time = datetime.datetime.utcnow()
start_position = {"x": -0.1276, "y": 51.5074, "z": 0}  # Approximate coordinates for London
start_battery = 100.0  # Start with full battery
start_heading = 0.0    # Start heading in degrees

# Insert Initial 100 Simulated Records
for i in range(1, 101):
    record = generate_car_update(i, start_time, start_position, start_battery, start_heading)
    database_insert(record)
    print(f"Inserted record {i}")

    # Update starting conditions for next iteration
    start_position = record["position"]
    start_battery = record["battery_level"]
    start_heading = record["heading"]

# Continuous Real-Time Updates Every 5 Seconds
i = 101
while True:
    time.sleep(5)
    record = generate_car_update(i, start_time, start_position, start_battery, start_heading)
    database_insert(record)
    print(f"Inserted record {i}")

    # Update starting conditions for next iteration
    start_position = record["position"]
    start_battery = record["battery_level"]
    start_heading = record["heading"]
    i += 1

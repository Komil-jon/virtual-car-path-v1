import requests
import time
import random
import json

# Define the correct API URL (Replace with your actual server URL)
url = "http://127.0.0.1:8000/update"

# Number of times to send the list of cars
num_requests = 50

# Interval between requests in seconds
interval = 1

# Number of cars to send each time
num_cars = 1

# Loop to send multiple POST requests
for i in range(num_requests):
    cars = []
    for j in range(num_cars):
        # Generate random latitude and longitude values
        latitude = round(random.uniform(40.0, 41.0), 6)  # Latitude range
        longitude = round(random.uniform(-75.0, -73.0), 6)  # Longitude range
        cars.append({
            "carId": f"car{j+1}",
            "latitude": latitude,
            "longitude": longitude
        })

    # Create the payload
    payload = {"cars": cars}

    # Convert to JSON string for debugging
    json_payload = json.dumps(payload, indent=4)
    print(f"\nRequest {i+1} payload:\n{json_payload}")

    # Send the POST request with proper headers
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})

        # Check the response status code and content
        print(f"Response {i+1} Status Code: {response.status_code}")
        print(f"Response {i+1} Content: {response.text}")

        if response.status_code != 200:
            print(f"⚠️ Warning: Request {i+1} failed!")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request {i+1} failed due to an error: {e}")

    # Wait for the specified interval
    time.sleep(interval)

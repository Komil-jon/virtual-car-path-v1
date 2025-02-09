import requests
import time
import random
import json

# Define the base URL for the POST requests
url = "https://8000-idx-virtual-car-path-1738924052649.cluster-6yqpn75caneccvva7hjo4uejgk.cloudworkstations.dev/update"

# Number of times to send the list of cars
num_requests = 5

# Interval between requests in seconds
interval = 1

# Number of cars to send each time
num_cars = 3

# Loop to send multiple POST requests
for i in range(num_requests):
    cars = []
    for j in range(num_cars):
        # Generate random latitude and longitude values
        latitude = random.uniform(40.0, 41.0)  # Latitude range
        longitude = random.uniform(-75.0, -73.0)  # Longitude range
        cars.append({
            "carId": f"car{j+1}",
            "latitude": latitude,
            "longitude": longitude
        })

    # Create the payload
    payload = {"cars": cars}
    
    #convert to json string for debug
    # json_payload = json.dumps(payload, indent=4)
    # print(f"Request {i+1} payload: {json_payload}")

    # Send the POST request
    try:
        response = requests.post(url, json=payload)

        # Check the response status code
        if response.status_code == 200:
            print(f"Request {i+1} successful: {response.text}")
        else:
            print(f"Request {i+1} failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request {i+1} failed due to an error: {e}")

    # Wait for the specified interval
    time.sleep(interval)
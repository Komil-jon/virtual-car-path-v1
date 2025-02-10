import aiohttp
import asyncio
import random
import json

# Define the correct API URL (Replace with your actual server URL)
url = "http://127.0.0.1:8000/update"

# Number of requests
num_requests = 500  

# Number of cars to send each time
num_cars = 1  

async def send_request(session, request_id):
    """Send a request asynchronously with a 1-second delay between each."""
    cars = [
        {
            "carId": f"car{j+1}",
            "latitude": round(random.uniform(40.0, 41.0), 6),
            "longitude": round(random.uniform(-75.0, -73.0), 6)
        }
        for j in range(num_cars)
    ]

    payload = {"cars": cars}
    json_payload = json.dumps(payload, indent=4)
    print(f"\n🚀 Request {request_id} payload:\n{json_payload}")

    try:
        async with session.post(url, json=payload) as response:
            response_text = await response.text()
            print(f"✅ Response {request_id} Status Code: {response.status}")
            print(f"📡 Response {request_id} Content: {response_text}")
    except Exception as e:
        print(f"❌ Request {request_id} failed due to: {e}")

async def main():
    """Send requests one by one with a 1-second delay."""
    async with aiohttp.ClientSession() as session:
        for i in range(num_requests):
            await send_request(session, i + 1)
            await asyncio.sleep(1)  # ⏳ Add a 1-second delay between requests

# Run the asyncio event loop
asyncio.run(main())

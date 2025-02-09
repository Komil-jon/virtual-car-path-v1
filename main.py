import os

from flask import Flask, send_file, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow WebSocket connections from any origin
print("Action: app created")

car_locations = []

@app.route("/")
def index():
    print("new client")
    return send_file('templates/core.html')

@app.route("/update", methods=["POST"])
def update_car_location():
    print(f"Received raw data: {request.get_data(as_text=True)}")  # Log raw input

    try:
        request_data = request.get_json()
        print(f"Parsed JSON: {request_data}")  # Log parsed JSON

        if not request_data or 'cars' not in request_data:
            print("Error: No 'cars' data provided")
            return jsonify({"message": "No 'cars' data provided"}), 400
        
        cars_data = request_data['cars']
        if not isinstance(cars_data, list):
            print("Error: 'cars' must be a list")
            return jsonify({"message": "'cars' must be a list"}), 400

        for car in cars_data:
            print(f"Processing car: {car}")  # Log each car
            car_locations.append(car)
            socketio.emit('car_location_updated', car)
        
        return jsonify({"message": "Car locations updated successfully"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")  # Log exception
        return jsonify({"message": "Error processing data", "error": str(e)}), 500
    
@socketio.on('connect')
def handle_connect():
    print('Action: Client connected')
    

def main():
    print("Action: Starting server")

    socketio.run(app, port=int(os.environ.get('PORT', 8000)), debug=True)

if __name__ == "__main__":
    main()
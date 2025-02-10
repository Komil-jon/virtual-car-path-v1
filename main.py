import os
import threading
import eventlet
import eventlet.wsgi

from flask import Flask, send_file, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Create Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Enable WebSockets (force async_mode="eventlet" for speed)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

print("✅ Action: Flask App Created")

# Store car locations
car_locations = []

@app.route("/")
def index():
    """Serve the core HTML file."""
    print("📢 New Client Connected")
    return send_file('templates/core.html')

@app.route("/update", methods=["POST"])
def update_car_location():
    """Handle incoming car location updates."""
    print(f"📡 Received Raw Data: {request.get_data(as_text=True)}")  # Log raw input

    try:
        request_data = request.get_json()
        print(f"✅ Parsed JSON: {request_data}")

        if not request_data or 'cars' not in request_data:
            print("⚠️ Error: No 'cars' data provided")
            return jsonify({"message": "No 'cars' data provided"}), 400
        
        cars_data = request_data['cars']
        if not isinstance(cars_data, list):
            print("⚠️ Error: 'cars' must be a list")
            return jsonify({"message": "'cars' must be a list"}), 400

        # Emit updates in a separate thread for **non-blocking** performance
        def emit_updates():
            for car in cars_data:
                socketio.emit('car_location_updated', car)
                print(f"🚗 Emitting update for car {car['carId']} → ({car['latitude']}, {car['longitude']})")

        threading.Thread(target=emit_updates).start()

        return jsonify({"message": "Car locations update triggered"}), 200

    except Exception as e:
        print(f"❌ Error: {str(e)}")  # Log exception
        return jsonify({"message": "Error processing data", "error": str(e)}), 500

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket client connections."""
    print('🔌 WebSocket Connected')

def main():
    """Start the Flask server using Eventlet for high-speed WebSockets."""
    print("🚀 Starting server with Eventlet for real-time WebSockets")

    # Run the server with Eventlet (better WebSocket handling)
    socketio.run(app, port=int(os.environ.get('PORT', 8000)), debug=True, allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    main()

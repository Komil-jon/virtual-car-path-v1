import os

from flask import Flask, send_file, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
print("Action: app created")

car_locations = []

@app.route("/")
def index():
    print("new client")
    return send_file('templates/core.html')

@app.route("/update", methods=["POST"])
def update_car_location():
    print('yedi')
    global car_locations
    try:
        request_data = request.get_json()
        if not request_data or 'cars' not in request_data:
            return jsonify({"message": "No 'cars' data provided"}), 400
        
        cars_data = request_data['cars']
        print(cars_data)
        if not isinstance(cars_data, list):
            return jsonify({"message": "'cars' must be a list"}), 400
        
        for car in cars_data:
            car_locations.append(car)
            socketio.emit('car_location_updated', car)
            
            return jsonify({"message": "Car location updated successfully"}), 200

    except Exception as e:
        return jsonify({"message": "Error processing data", "error": str(e)}), 500
    
@socketio.on('connect')
def handle_connect():
    print('Action: Client connected')
    

def main():
    print("Action: Starting server")

    socketio.run(app, port=int(os.environ.get('PORT', 80)), debug=True)

if __name__ == "__main__":
    main()
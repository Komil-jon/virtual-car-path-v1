let map;
let markers = {}; // Store car markers
let paths = {}; // Store polylines for each car

async function init() {
  console.log("🚀 Initializing Google Map...");

  await customElements.whenDefined("gmp-map");
  map = document.querySelector("gmp-map");

  map.innerMap.setOptions({
    mapTypeControl: false,
  });

  console.log("✅ Map initialized successfully.");

  // Connect to WebSocket server
  const socket = io.connect(window.location.origin);
  console.log("🔌 Connecting to WebSocket server...");

  socket.on("connect", () => {
    console.log("✅ WebSocket connected!");
  });

  socket.on("car_location_updated", (carData) => {
    console.log("📡 Received car location update:", carData);
    updateCarLocation(carData);
  });

  socket.on("disconnect", () => {
    console.log("❌ WebSocket disconnected!");
  });
}

// Update car position and draw path
function updateCarLocation(carData) {
  const { carId, latitude, longitude } = carData;
  console.log(`🚗 Updating position for ${carId} → (${latitude}, ${longitude})`);

  const position = new google.maps.LatLng(latitude, longitude);

  if (!markers[carId]) {
    console.log(`🆕 Creating new marker for ${carId}`);

    // Create a new marker for the car
    markers[carId] = new google.maps.Marker({
      position: position,
      map: map.innerMap,
      title: `Car ${carId}`,
      icon: {
        url: "https://maps.google.com/mapfiles/kml/shapes/cabs.png", // Car icon
        scaledSize: new google.maps.Size(40, 40),
      },
    });

    // Create a polyline for the car's path
    paths[carId] = new google.maps.Polyline({
      path: [position],
      geodesic: true,
      strokeColor: getRandomColor(),
      strokeOpacity: 1.0,
      strokeWeight: 3,
      map: map.innerMap,
    });

    console.log(`✅ Marker and path created for ${carId}`);
  } else {
    console.log(`✏️ Updating marker position for ${carId}`);

    // Move the marker to the new position
    markers[carId].setPosition(position);

    // Update the polyline path
    const path = paths[carId].getPath();
    path.push(position);

    console.log(`📈 Path updated for ${carId}`);
  }
}

// Generate a random color for different cars
function getRandomColor() {
  const color = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
  console.log(`🎨 Generated random color: ${color}`);
  return color;
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("📜 Document loaded, initializing map...");
  init();
});

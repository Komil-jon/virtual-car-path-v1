let map;
let markers = {};
let paths = {};
let lastCarId = null;
let latestUpdateId = 0;  // Initial value for the update ID

async function init() {
    console.log("🚀 Initializing Google Map...");
    await customElements.whenDefined("gmp-map");
    map = document.querySelector("gmp-map");
    map.innerMap.setOptions({ mapTypeControl: false });

    console.log("✅ Map initialized.");
    await fetchInitialUpdates();
    fetchNewUpdates();
}

// Fetch the latest 20 updates from your server's /api/all endpoint
async function fetchInitialUpdates() {
    try {
        const response = await fetch("/api/all");
        const data = await response.json();

        if (data.length > 0) {
            latestUpdateId = data[data.length - 1].update_id;  // Store the last update_id
            data.reverse().forEach(updateCarLocation);  // Reverse the array to show updates in chronological order
        }
    } catch (error) {
        console.error("❌ Error fetching initial updates:", error);
    }
}

// Continuously fetch new updates from your server's /api/get endpoint based on the latest update_id
async function fetchNewUpdates() {
    try {
        const response = await fetch(`/api/get?update_id=${latestUpdateId}`);
        const data = await response.json();

        if (data && data.update_id > latestUpdateId) {
            updateCarLocation(data);
            latestUpdateId = data.update_id;  // Update the latest update_id with the new one
        } else if (data.length > 0) {
            // If multiple updates are returned (batch updates), process them
            data.forEach(updateCarLocation);
            latestUpdateId = data[data.length - 1].update_id;  // Update with the last update_id
        }
    } catch (error) {
        console.error("❌ Error fetching new updates:", error);
    }

    setTimeout(fetchNewUpdates, 1000);  // Keep fetching every second
}

// Update car location and draw the path
function updateCarLocation(carData) {
    const { car_id, position, average_speed } = carData;
    const latitude = position.y;
    const longitude = position.x;
    console.log(`🚗 Updating ${car_id} → (${latitude}, ${longitude})`);

    const positionLatLng = new google.maps.LatLng(latitude, longitude);

    if (!markers[car_id]) {
        // If it's the first update for this car, create the marker and path
        markers[car_id] = new google.maps.Marker({
            position: positionLatLng,
            map: map.innerMap,
            title: `Car ${car_id}`,
            icon: {
                url: "https://maps.google.com/mapfiles/kml/shapes/cabs.png",
                scaledSize: new google.maps.Size(40, 40),
            },
        });

        paths[car_id] = new google.maps.Polyline({
            path: [positionLatLng],
            geodesic: true,
            strokeColor: getSpeedColor(average_speed),
            strokeOpacity: 1.0,
            strokeWeight: 3,
            map: map.innerMap,
        });

        console.log(`✅ Marker and path created for ${car_id}`);
    } else {
        // Update the marker and path for an existing car
        markers[car_id].setPosition(positionLatLng);
        const path = paths[car_id].getPath();
        path.push(positionLatLng);
        paths[car_id].setOptions({ strokeColor: getSpeedColor(average_speed) });
        console.log(`📈 Path updated for ${car_id}`);
    }

    animateCameraToPosition(positionLatLng, car_id);
}

// Smooth camera animation to new position
function animateCameraToPosition(position, carId) {
    if (lastCarId !== carId) {
        map.innerMap.setZoom(15);
        lastCarId = carId;
    }
    map.innerMap.panTo(position);
    console.log(`🔄 Camera moved to ${carId}`);
}

// Get a color based on the car's speed
function getSpeedColor(speed) {
    const minSpeed = 0;
    const maxSpeed = 120;
    const speedRatio = Math.min(Math.max(speed / maxSpeed, 0), 1);
    const red = Math.floor(255 * (1 - speedRatio));
    const green = Math.floor(255 * speedRatio);
    return `rgb(${red}, ${green}, 0)`;
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("📜 Document loaded, initializing map...");
    init();
});
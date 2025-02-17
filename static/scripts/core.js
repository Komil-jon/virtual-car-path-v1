let latestUpdateId = 0; // Track last update ID

// Create Canvas for Chart
const chartContainer = document.getElementById("chart-container");
const canvas = document.createElement("canvas");
canvas.id = "carChartCanvas";
chartContainer.appendChild(canvas);
const ctx = canvas.getContext("2d");

if (!ctx) {
    console.error("❌ Chart canvas not found!");
} else {
    console.log("✅ Chart canvas found, initializing...");
}

let map;
let markers = {};
let paths = {};
let lastCarId = null;

// Chart Data Structure
let chartData = {
    labels: [], // Time values
    datasets: [
        { label: "Speed (km/h)", data: [], borderColor: "red", backgroundColor: "rgba(255, 99, 132, 0.5)" },
        { label: "Battery (%)", data: [], borderColor: "blue", backgroundColor: "rgba(54, 162, 235, 0.5)" },
        { label: "Fuel Level (%)", data: [], borderColor: "green", backgroundColor: "rgba(75, 192, 192, 0.5)" },
        { label: "Engine Temp (°C)", data: [], borderColor: "orange", backgroundColor: "rgba(255, 159, 64, 0.5)" },
        { label: "Heading (°)", data: [], borderColor: "purple", backgroundColor: "rgba(153, 102, 255, 0.5)" },
        { label: "Humidity (%)", data: [], borderColor: "teal", backgroundColor: "rgba(0, 128, 128, 0.5)" },
        { label: "Pressure (10⁴Pa)", data: [], borderColor: "brown", backgroundColor: "rgba(165, 42, 42, 0.5)" },
        { label: "UV Radiation (mW/m²)", data: [], borderColor: "pink", backgroundColor: "rgba(255, 192, 203, 0.5)" },
    ]
};

// Chart Configuration
const chartConfig = {
    type: "line",
    data: chartData,
    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 2000,
            easing: "easeInOutQuart",
        },
        elements: {
            line: { tension: 0.3, borderWidth: 2 },
            point: { radius: 3 }
        },
        scales: {
            x: { title: { display: true, text: "Time" } },
            y: { title: { display: true, text: "Value" }, beginAtZero: false }
        },
        interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
        },
        plugins: {
            title: {
              display: true,
              text: "© Eternal 2025"
            }
        },
    }
};

const carChart = new Chart(ctx, chartConfig);

// Initialize Data Fetching
async function init() {
    console.log("🚀 Initializing chart and map...");
    await customElements.whenDefined("gmp-map");
    map = document.querySelector("gmp-map");
    map.innerMap.setOptions({ mapTypeControl: false });
    await fetchInitialUpdates();
    fetchChartData();
}

// Fetch Initial 20 Data Points
async function fetchInitialUpdates() {
    try {
        const response = await fetch("/api/all");
        const data = await response.json();

        if (data.length > 0) {
            latestUpdateId = data[0].update_id;
            data.reverse().forEach(updateCarLocation);
            data.forEach(updateChart);
        }
    } catch (error) {
        console.error("❌ Error fetching initial updates:", error);
    }
}

// Continuously Fetch New Data
async function fetchChartData() {
    try {
        const response = await fetch(`/api/get?update_id=${latestUpdateId}`);
        const data = await response.json();

        console.log(data);

        if (data && data.update_id > latestUpdateId) {
            console.log("1");
            updateCarLocation(data);
            updateChart(data);
            latestUpdateId = data.update_id;  // Update the latest update_id with the new one
        } else if (data.length > 0) {
            console.log("2");
            // If multiple updates are returned (batch updates), process them
            latestUpdateId = data[0].update_id;  // Update with the last update_id
            data.reverse().forEach(updateCarLocation);
            data.forEach(updateChart);
        }
        console.log("3");
    } catch (error) {
        console.error("❌ Error fetching chart data:", error);
    }
    setTimeout(fetchChartData, 1000);
}

// Update Chart with New Data
function updateChart(carData) {
    const time = new Date(carData.time).toLocaleTimeString();
    console.log(`📊 Adding time: ${time} | Speed: ${carData.average_speed}, Battery: ${carData.battery_level}`);

    if (chartData.labels.length >= 20) chartData.labels.shift();
    chartData.labels.push(time);

    chartData.datasets[0].data.push(carData.average_speed);
    chartData.datasets[1].data.push(carData.battery_level);
    chartData.datasets[2].data.push(carData.fuel_level);
    chartData.datasets[3].data.push(carData.temperature?.engine || 0);
    chartData.datasets[4].data.push(carData.heading);
    chartData.datasets[5].data.push(carData.humidity);
    chartData.datasets[6].data.push(carData.pressure);
    chartData.datasets[7].data.push(carData.radiation);

    chartData.datasets.forEach(dataset => {
        if (dataset.data.length > 20) dataset.data.shift();
    });

    setTimeout(() => carChart.update(), 100);
    console.log("📈 Chart updated:", chartData);
}

// Update Car Location
function updateCarLocation(carData) {
    const { car_id, position, average_speed } = carData;
    const latitude = position.y;
    const longitude = position.x;
    console.log(`🚗 Updating ${car_id} → (${latitude}, ${longitude})`);

    const positionLatLng = new google.maps.LatLng(latitude, longitude);
    
    if (!markers[car_id]) {
        markers[car_id] = new google.maps.Marker({
            position: positionLatLng,
            map: map.innerMap,
            title: `Car ${car_id}`,
            icon: { url: "https://maps.google.com/mapfiles/kml/shapes/cabs.png", scaledSize: new google.maps.Size(40, 40) }
        });
        paths[car_id] = new google.maps.Polyline({
            path: [positionLatLng],
            geodesic: true,
            strokeColor: getSpeedColor(average_speed),
            strokeWeight: 3,
            map: map.innerMap,
        });
    } else {
        markers[car_id].setPosition(positionLatLng);
        const path = paths[car_id].getPath();
        path.push(positionLatLng);
        
        // Create a new segment with a different color
        const newSegment = new google.maps.Polyline({
            path: [path.getAt(path.getLength() - 2), positionLatLng],
            geodesic: true,
            strokeColor: getSpeedColor(average_speed),
            strokeWeight: 7,
            map: map.innerMap,
        });
    }

    // Add circular markers at joints with a fixed blue color
    new google.maps.Marker({
        position: positionLatLng,
        map: map.innerMap,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 7, // Adjust size of the circle
            fillColor: "yellow",
            fillOpacity: 1,
            strokeWeight: 1,
            strokeColor: "orange"
        }
    });

    animateCameraToPosition(positionLatLng, car_id);
}


function animateCameraToPosition(position, carId) {
    if (lastCarId !== carId) {
        map.innerMap.setZoom(18);
        lastCarId = carId;
    }
    map.innerMap.panTo(position);
}

function getSpeedColor(speed) {
    const maxSpeed = 2;
    const speedRatio = Math.min(Math.max(speed / maxSpeed, 0), 1);
    const red = Math.floor(255 * speedRatio);
    const green = Math.floor(255 * (1 - speedRatio));
    return `rgb(${red}, ${green}, 255)`;
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("📜 Document loaded, initializing...");
    init();
});
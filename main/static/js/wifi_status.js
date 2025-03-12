// Function to fetch WiFi status
async function fetchWifiStatus() {
    // Show the loader
    document.getElementById('loader').style.display = 'block';

    try {
        // Fetch data from /wifi/status
        const response = await fetch('/wifi/status');
        const data = await response.json();

        // Hide the loader
        document.getElementById('loader').style.display = 'none';

        // Parse and display the content
        displayStatus(data);
    } catch (error) {
        // Hide the loader and show error
        document.getElementById('loader').style.display = 'none';
        document.getElementById('content').innerHTML = `<p>Error: ${error.message}</p>`;
    }
}
// Function to display WiFi status
function displayStatus(data) {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="status-card">
            <h2>WiFi Status</h2>
            <p><strong>Connected:</strong> <span class="${data.connected ? 'connected' : 'not-connected'}">${data.connected ? 'Yes' : 'No'}</span></p>
            <p><strong>Internet Access:</strong> <span class="${data.internet ? 'connected' : 'not-connected'}">${data.internet ? 'Yes' : 'No'}</span></p>
            <p><strong>Network Name:</strong> ${data['network name'] || 'Not Available'}</p>
        </div>
    `;
}

// Fetch WiFi status when the page loads
window.onload = fetchWifiStatus;
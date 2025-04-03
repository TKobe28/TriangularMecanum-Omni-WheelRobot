const socket = io();
const videoElement = document.getElementById('video');
let currentBlobUrl = null; // Track the current Blob URL

socket.on('video_frame', (base64Data) => {
    // Convert base64 to raw binary data
    const byteArray = Uint8Array.from(atob(base64Data), c => c.charCodeAt(0));
    const blob = new Blob([byteArray], { type: 'image/jpeg' });

    // Create new Blob URL
    const newBlobUrl = URL.createObjectURL(blob);

    // Update image source
    videoElement.onload = () => {
        // Revoke previous Blob URL after new image loads
        if (currentBlobUrl) {
            URL.revokeObjectURL(currentBlobUrl);
        }
        currentBlobUrl = newBlobUrl;
    };
    videoElement.src = newBlobUrl;
});

// quality slider
QUALITY_ENDPOINT = '/stream_settings'
let quality = 50

const qualitySlider = document.getElementById('qualitySlider');
const qualityLabel = document.getElementById('quality');

//
async function updateQuality() {
    if (isRequesting) return;

    isRequesting = true;
    try {
        await fetch(QUALITY_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'quality': quality,
            })
        });
    } catch (error) {
        console.error('Error:', error);
    }
    isRequesting = false;
}

// Update speed multiplier when slider changes
qualitySlider.addEventListener('input', () => {
    quality = parseFloat(qualitySlider.value);
    qualityLabel.textContent = `${quality.toFixed(0)} %`;
});
// post new value on mouse up
qualitySlider.addEventListener('mouseup', () => {
    updateQuality();
});

// Function to check if SSID is empty and disable/enable the confirm button
function checkSSID() {
  const ssid = document.getElementById('ssid').value;
  const confirmBtn = document.getElementById('confirm-btn');
  confirmBtn.disabled = ssid.trim() === ''; // Disable if SSID is empty
}

// Check SSID whenever the SSID input changes
document.getElementById('ssid').addEventListener('input', checkSSID);

document.getElementById('confirm-btn').addEventListener('click', function() {
  const ssid = document.getElementById('ssid').value;
  const password = document.getElementById('password').value;
  const hotspot = document.getElementById('toggle-switch').checked;
  fetch('/wifi/connect', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ ssid, password, hotspot }),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
});
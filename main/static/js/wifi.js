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

  // Disable all fields and the confirm button
  document.getElementById('ssid').disabled = true;
  document.getElementById('password').disabled = true;
  document.getElementById('toggle-switch').disabled = true;
  document.getElementById('confirm-btn').disabled = true;

  //enable the spinner
  document.getElementById('connecting-loader').style.display = 'block';
  // Clear any previous response message
  document.getElementById('response-message').textContent = '';

  fetch('/wifi/connect', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ ssid, password, hotspot }),
  })
  .then(response => {
    // Display the response status code
    document.getElementById('response-message').textContent = `Response Code: ${response.status}`;
  })
  .catch((error) => {
    // Display the error message
    document.getElementById('response-message').textContent = 'Error: ' + error.message;
  })
  .finally(() => {
    // Hide loading spinner
    document.getElementById('connecting-loader').style.display = 'none';

    document.getElementById('ssid').disabled = false;
    document.getElementById('password').disabled = false;
    document.getElementById('toggle-switch').disabled = false;
    document.getElementById('confirm-btn').disabled = false;
  });
});
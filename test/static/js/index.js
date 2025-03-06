// JavaScript for handling input
const CONTROL_ENDPOINT = '/control';
const BASE_SPEED = 1;
let isRequesting = false;
let speedMultiplier = 1;

// Initialize state
let currentState = {
    vx: 0,
    vy: 0,
    omega: 0
};

// Get speed slider and value display
const speedSlider = document.getElementById('speedSlider');
const speedValue = document.getElementById('speedValue');

// Update speed multiplier when slider changes
speedSlider.addEventListener('input', () => {
    speedMultiplier = parseFloat(speedSlider.value);
    speedValue.textContent = `${speedMultiplier.toFixed(0)}x`;
});

// Handle keyboard input
const keyMap = {
    'w': { vx: BASE_SPEED },
    's': { vx: -BASE_SPEED },
    'a': { vy: BASE_SPEED },
    'd': { vy: -BASE_SPEED },
    'ArrowLeft': { omega: -1 },
    'ArrowRight': { omega: 1 }
};

const activeKeys = new Set();

document.addEventListener('keydown', (e) => {
    if (keyMap[e.key] && !activeKeys.has(e.key)) {
        activeKeys.add(e.key);
        updateState();
        sendCommand();
    }
});

document.addEventListener('keyup', (e) => {
    if (keyMap[e.key]) {
        activeKeys.delete(e.key);
        updateState();
        sendCommand();
    }
});

// Handle button clicks
document.querySelectorAll('.control-btn').forEach(button => {
    button.addEventListener('mousedown', () => {
        const stateUpdate = {
            vx: parseFloat(button.dataset.vx) || 0,
            vy: parseFloat(button.dataset.vy) || 0,
            omega: parseFloat(button.dataset.omega) || 0
        };
        Object.assign(currentState, stateUpdate);
        sendCommand();
    });

    button.addEventListener('mouseup', () => {
        const stateUpdate = {
            vx: button.dataset.vx ? 0 : currentState.vx,
            vy: button.dataset.vy ? 0 : currentState.vy,
            omega: button.dataset.omega ? 0 : currentState.omega
        };
        Object.assign(currentState, stateUpdate);
        sendCommand();
    });
});

function updateState() {
    const newState = { vx: 0, vy: 0, omega: 0 };

    activeKeys.forEach(key => {
        if (keyMap[key]) {
            newState.vx += keyMap[key].vx || 0;
            newState.vy += keyMap[key].vy || 0;
            newState.omega += keyMap[key].omega || 0;
        }
    });

    currentState = newState;
}

async function sendCommand() {
    if (isRequesting) return;

    isRequesting = true;
    try {
        const command = {
            vx: currentState.vx * speedMultiplier,
            vy: currentState.vy * speedMultiplier,
            omega: currentState.omega * speedMultiplier
        };

        await fetch(CONTROL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(command)
        });
    } catch (error) {
        console.error('Error:', error);
    }
    isRequesting = false;
}

document.getElementById('logoutBtn').addEventListener('click', () => {
    fetch('/logout', {
        method: 'POST',
        credentials: 'include'
    }).then(() => {
        window.location.reload();
    });
});
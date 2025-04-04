import subprocess
import socket

def get_wifi_status():
    status = {
        "connected": False,
        "internet": False,
        "network name": "none"
    }

    # Check WiFi connection and SSID
    try:
        ssid = subprocess.check_output(
            ["iwgetid", "-r"], stderr=subprocess.DEVNULL
        ).decode().strip()
        if ssid:
            status["connected"] = True
            status["network name"] = ssid
    except subprocess.CalledProcessError:
        pass

    # Check internet connectivity (Google DNS ping)
    if status["connected"]:
        try:
            socket.setdefaulttimeout(2)
            socket.create_connection(("8.8.8.8", 53))
            status["internet"] = True
        except OSError:
            pass

    return status

if __name__ == "__main__":
    print(get_wifi_status())

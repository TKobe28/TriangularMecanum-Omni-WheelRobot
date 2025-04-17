import subprocess
import socket


def get_wifi_status() -> (dict, int):
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
    except FileNotFoundError:
        print("You probably don't have the libraries installed!")
        return {"error": "Libraries not installed"}, 500

    # Check internet connectivity (Google DNS ping)
    if status["connected"]:
        try:
            socket.setdefaulttimeout(2)
            socket.create_connection(("8.8.8.8", 53))
            status["internet"] = True
        except OSError:
            pass

    return status, 200


if __name__ == "__main__":
    print(get_wifi_status())

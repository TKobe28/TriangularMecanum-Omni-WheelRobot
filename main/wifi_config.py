import os.path
import subprocess
import time

if subprocess.getoutput("whoami") != 'root':
    print("Not ran as root - CANNOT MANIPULATE WIFI!! - Using test functions.")

    def connect_to_wifi(ssid: str, password: str) -> int:
        print("Imagine we now connected to " + ssid + " with " + password)
        return 200

    def start_hotspot(ssid: str = "FBI_van", password: str = "HailTrump!") -> int:
        print("Imagine we now have hotspot on " + ssid + " with " + password)
        return 200

else:
    # different wifi card devices names on my pc and on the pi - I have the file on my pc.
    # I know there are better ways for this, but I haven't got enough functioning braincells left to do something better.
    WIFI_INTERFACE_NAME = "wlan0" if not os.path.exists("not_pi") else "wlp15s0"

    def connect_to_wifi(ssid: str, password: str) -> int:
        """
        Connects to a WiFi network using the provided SSID and password.
        """
        try:
            # Disconnect from any existing connection
            subprocess.run(["nmcli", "device", "disconnect", WIFI_INTERFACE_NAME], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Couldn't disconnect from previous network (check above line)(still attempting connection): {e}")
            # no need to return

        time.sleep(5)  # give it some time to do some shit or sth
        try:
            # Connect to the new WiFi network
            subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "password", password], check=True)
            print(f"Successfully connected to {ssid}")
            return 200
        except subprocess.CalledProcessError as e:
            print(f"Failed to connect to {ssid}: {e}")
            return 500

    def start_hotspot(ssid: str = "FBI_van", password: str = "GodBlessMurica!") -> int:
        """
        Starts a WiFi hotspot with the provided SSID and password.
        """
        if len(password) < 8:
            return 400
        try:
            subprocess.run(["sudo", "nmcli", "device", "wifi", "hotspot", "ssid", ssid, "password", password, "ifname", WIFI_INTERFACE_NAME])

            print(f"Hotspot '{ssid}' started with password '{password}'")
            return 200
        except subprocess.CalledProcessError as e:
            print(f"Failed to start hotspot: {e}")
            return 500


# Example usage
if __name__ == "__main__":
    # Connect to a WiFi network
    connect_to_wifi("KobeZgoraj", "")

    time.sleep(5)

    start_hotspot()

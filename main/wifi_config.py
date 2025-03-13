import os.path
import subprocess
import time

if subprocess.getoutput("whoami") != 'root':
    print("Not ran as root - CANNOT MANIPULATE WIFI!! - Using test functions.")

    def connect_to_wifi(ssid: str, password: str):
        print("Imagine we now connected to " + ssid + " with " + password)
        return 0

    def start_hotspot(ssid: str = "FBI_van", password: str = "HailTrump!"):
        print("Imagine we now have hotspot on " + ssid + " with " + password)
        return 0

else:
    # different wifi card devices names on my pc and on the pi - I have the file on my pc.
    # I know there are better ways for this, but I haven't got enough functioning braincells left to do something better.
    WIFI_INTERFACE_NAME = "wlan0" if not os.path.exists("not_pi") else "wlp15s0"

    def connect_to_wifi(ssid, password):
        """
        Connects to a WiFi network using the provided SSID and password.
        """
        try:
            # Disconnect from any existing connection
            subprocess.run(["nmcli", "device", "disconnect", WIFI_INTERFACE_NAME], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Couldn't disconnect from previous network (check above line)(still attempting connection): {e}")

        time.sleep(5)  # give it some time to do some shit or sth
        try:
            # Connect to the new WiFi network
            subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "password", password], check=True)
            print(f"Successfully connected to {ssid}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to connect to {ssid}: {e}")


    def start_hotspot(ssid: str = "FBI_van", password: str = "GodBlessMurica!"):
        """
        Starts a WiFi hotspot with the provided SSID and password.
        """
        try:
            subprocess.run(["sudo", "nmcli", "device", "wifi", "hotspot", "ssid", ssid, "password", password, "ifname", WIFI_INTERFACE_NAME])

            print(f"Hotspot '{ssid}' started with password '{password}'")
        except subprocess.CalledProcessError as e:
            print(f"Failed to start hotspot: {e}")


# Example usage
if __name__ == "__main__":
    # Connect to a WiFi network
    connect_to_wifi("KobeZgoraj", "")

    time.sleep(5)

    start_hotspot()

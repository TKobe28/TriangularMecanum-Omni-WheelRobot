import os.path
import subprocess
import time

if subprocess.getoutput("whoami") != 'root':
    print("Not ran as root - CANNOT MANIPULATE WIFI!! - Using test functions.")

    def connect_to_wifi(ssid: str, password: str):
        print("Imagine we now connected to " + ssid + " with " + password)
        return 0

    def start_hotspot(ssid: str, password: str):
        print("Imagine we now have hotspot on " + ssid + " with " + password)
        return 0

else:
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
        try:
            # Connect to the new WiFi network
            subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "password", password], check=True)
            print(f"Successfully connected to {ssid}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to connect to {ssid}: {e}")


    def start_hotspot(ssid="RPiHotspot", password="raspberry"):
        """
        Starts a WiFi hotspot with the provided SSID and password.
        """
        try:
            # Stop any existing hotspot services
            subprocess.run(["sudo", "systemctl", "stop", "hostapd"], check=True)
            subprocess.run(["sudo", "systemctl", "stop", "dnsmasq"], check=True)

            # Configure hostapd (hotspot)
            with open("/etc/hostapd/hostapd.conf", "w") as f:
                f.write(f"""
interface={WIFI_INTERFACE_NAME}
driver=nl80211
ssid={ssid}
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
""")

            # Configure dnsmasq (DHCP and DNS forwarding)
            with open("/etc/dnsmasq.conf", "w") as f:
                f.write(f"""
no-resolv
server=127.0.0.53
interface={WIFI_INTERFACE_NAME}
bind-interfaces
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
""")

            # Start hotspot services
            subprocess.run(["sudo", "systemctl", "start", "hostapd"], check=True)
            subprocess.run(["sudo", "systemctl", "start", "dnsmasq"], check=True)

            print(f"Hotspot '{ssid}' started with password '{password}'")
        except subprocess.CalledProcessError as e:
            print(f"Failed to start hotspot: {e}")


# Example usage
if __name__ == "__main__":
    # Connect to a WiFi network
    connect_to_wifi("KobeZgoraj", "")

    time.sleep(5)

    print("Test1234")
    start_hotspot(ssid="RPiHotspot", password="raspberry")

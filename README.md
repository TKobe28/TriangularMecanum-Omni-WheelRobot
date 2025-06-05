# Triangular Mecanum-Omni-Wheel Robot

## Overview

This project is a school robotics project.

We designed and made a triangular robot with 3 mecanum omni wheels and a camera for streaming, all controlled by a raspberry pi 3 b.

The pi hosts a website, which has camera feed, controls, basic authentication system and simple network managing system.

The project is written in Python, using Flask (a big part of the code is Javascript, but that's because there is socket.io.js in the static files, so that the project works used even if there is no internet connection).

## Features

- Triangular chassis with three mecanum omni wheels
- Real-time video feed using Pi Camera
- Web-based interface for control and camera stream

## Hardware Components we used

- Raspberry Pi 3B (or compatible model)
- 3x Omni wheels with DC motors
- Motor driver
- Pi Camera module
- 3d printed chasis
- 8 or 6 1.5 Volt AA batteries
- a step-down buck converter (to 5.1 volts)
- 3 LEDs
- a button used for enabling the hotspot (for setting up wifi or normal usage)


## printing and building
coming soon (relatively to the age of ur mom hehee get burned lol ts never coming bru)

## Installation

1. Flash Raspberry Pi OS onto SD card.
2. Clone the project repository (we did this on /home/{user})
3. cd into the new folder
4. If you know what you are doing and if you want to have other stuff on the same pi you can try making a virtual environment, but I didn't do that
5. Install dependencies: `pip install -r requirements.txt` (you might need to do this as root - usually by adding "sudo" to the start)
6. Enable camera module via `raspi-config` if using Pi Camera. I also recommend connecting to a wifi network while you are there.
7. run `chmod +x run.sh`
8. *OPTIONAL:* If you want the server to start automatically with each boot you can also enable systemd service included:
    1. run `chmod +x ./serverServiceSetup.sh`
    2. run `./serverServiceSetup.sh`
    3. run `sudo systectl enable server.service`
    4. run `sudo systemctl start server.service` 
    5. you can read this for more info: https://wiki.archlinux.org/title/Systemd

---
NOTE: IF YOU WANT TO MODIFY WIFI SETTINGS YOU SHOULD RUN THE SERVER AS ROOT - this usually means adding "sudo" before your commands (you should do that when installing dependencies too)

### User Management

#### Adding a New User

To add a new user for authentication:

1. Run the following command:
   ```bash
   python3 main/add_user.py
   ```
2. Follow the prompts:
   - Enter a unique username.
   - Enter a password (input is hidden).
   - Enter the access level as an integer (lower numbers mean more access).

The user information (username, hashed password, and access level) will be saved to `main/secret`.

#### Removing a User

To remove a user:

1. Open the `main/secret` file in a text editor.
2. Each user entry consists of three lines:
    1. Username
    2. Password hash
    3. Access level
3. Find the three lines corresponding to the user you want to remove and delete them.
4. Save and close the file.


## Usage

- run by running `./run.sh` or just by booting up the pi, if you set up systemd service in the installation 
- Access the web interface via `<raspberry_pi_ip>:5000` from any device on the same network.
- to enable hotspot on the raspberry pi, hold the button for ten seconds.

## How it works
On hopes and dreams.

## Notes

- it probably won't work first try lol. 

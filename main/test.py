from picamera2 import Picamera2

# Initialize Picamera2
picam2 = Picamera2()

# Configure the camera
config = picam2.create_still_configuration()
picam2.configure(config)

# Start the camera
picam2.start()

# Capture a single frame and save it
frame = picam2.capture_file("captured_frame.jpg")

# Stop the camera
picam2.stop()

print("Frame saved as 'captured_frame.jpg'")

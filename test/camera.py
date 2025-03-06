import cv2
import time
try:
    from picamera2 import Picamera2
    test = False
except ModuleNotFoundError:
    print("Picamera not installed, running in test mode")
    test = True

if test:
    camera = cv2.VideoCapture(0)
    camera.read()  # to init faster
else:
    camera = Picamera2()
    camera_config = camera.create_video_configuration()
    camera.configure(camera_config)
    camera.start()

FPS_LIMIT = 24
_frame_time = 1 / FPS_LIMIT


if not test:
    def generate_frames():
        """Yields frames from the camera as JPEG-encoded images."""
        while True:
            frame = camera.capture_array()
            return frame
else:
    def generate_frame():
        while True:
            ret, frame = camera.read()
            if not ret:
                return None
            return frame

with open("goofy_ahh.jpg", "rb") as f:
    goofy_image = f.read()


def video_stream_generator():
    while True:
        frame = generate_frame()
        if frame is not None:
            ret, frame = cv2.imencode(".jpg", frame)
            if not ret:
                frame = None
            frame = frame.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        if not frame:
            print("could not capture frame.")
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + goofy_image + b'\r\n')

import time
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident
try:
    from picamera2 import Picamera2
    from picamera2.encoders import H264Encoder
    test = False
except ModuleNotFoundError:
    print("Picamera not installed, running in test mode")
    test = True
from flask import render_template_string
from flask_socketio import SocketIO
import cv2
import base64
import threading
from control import app

socketio = SocketIO(app, cors_allowed_origins="*")

QUALITY = 50
FRAMETIME = 1 / 24

if test:
    camera = cv2.VideoCapture(0)

    # todo: cv2.imencode('.jpg', img, params=[cv2.IMWRITE_JPEG_QUALITY, 50])
    def emit_frames():
        while True:
            success, frame = camera.read()
            if success:
                _, buffer = cv2.imencode('.jpg', frame, params=[cv2.IMWRITE_JPEG_QUALITY, QUALITY])
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                socketio.emit('video_frame', jpg_as_text)
            time.sleep(FRAMETIME)

else:
    camera = Picamera2()
    config = camera.create_video_configuration(
        main={"size": (640, 480)},
        raw={"size": (640, 480)},  # Match sensor readout to output
        encode="main",
        queue=False  # Critical for low latency
    )
    camera.configure(config)
    camera.start()

    def emit_frames():
        try:
            while True:
                buffer = camera.capture_array()

                # Fastest possible JPEG conversion
                _, jpeg = cv2.imencode(
                    ".jpg",
                    buffer,
                    params=[cv2.IMWRITE_JPEG_QUALITY, QUALITY]
                )
                if not _:
                    continue
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                socketio.emit('video_frame', jpg_as_text)  # todo: tobytes()?
                time.sleep(FRAMETIME)
        finally:
            camera.stop()


@app.route('/test')
def test():
    return render_template_string('''<html><body>
        <img id="video" width="640" height="480">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        <script>
            const socket = io();
            socket.on('video_frame', (data) => {
                document.getElementById('video').src = 'data:image/jpeg;base64,' + data;
            });
        </script></body></html>''')


threading.Thread(target=emit_frames, daemon=True).start()  # todo

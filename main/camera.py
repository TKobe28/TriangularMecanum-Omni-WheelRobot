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
print("Importing socket.io, might take some time ...")
from flask_socketio import SocketIO
import cv2
import base64
import threading
from control import app
from traceback import format_exception

socketio = SocketIO(app, cors_allowed_origins="*")
print("socketio ok")

QUALITY = 50
FRAMETIME = 1 / 24

if test:
    camera = cv2.VideoCapture(0)

    def emit_frames():
        while True:
            start_capture_time = time.time()
            success, frame = camera.read()
            if success:
                _, buffer = cv2.imencode('.jpg', frame, params=[cv2.IMWRITE_JPEG_QUALITY, QUALITY])
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                socketio.emit('video_frame', jpg_as_text)

            capture_time = time.time() - start_capture_time
            if capture_time < FRAMETIME:
                time.sleep(FRAMETIME - capture_time)

else:
    print("not test!")
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
                start_capture_time = time.time()
                buffer = camera.capture_array()

                # Fastest possible JPEG conversion
                _, jpeg = cv2.imencode(
                    ".jpg",
                    buffer,
                    params=[cv2.IMWRITE_JPEG_QUALITY, QUALITY]
                )

                if not _:
                    continue
                jpg_as_text = base64.b64encode(jpeg).decode('utf-8')
                socketio.emit('video_frame', jpg_as_text)  # is tobytes() better?
                time.sleep(FRAMETIME)
                capture_time = time.time() - start_capture_time
                if capture_time < FRAMETIME:
                    time.sleep(FRAMETIME - capture_time)
        except Exception as e:
            print("ERROR IN EMITING FRAMES:", "\n".join(format_exception(e)))
        finally:
            camera.stop()


threading.Thread(target=emit_frames, daemon=True).start()

# a lot was copied from https://github.com/miguelgrinberg/flask-video-streaming/
import cv2
import time
import threading
import io
import os
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


class CameraEvent:
    """An Event-like class that signals all active clients when a new frame is
    available.
    """
    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera:
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    event = CameraEvent()

    def __init__(self):
        """Start the background camera thread if it isn't running yet."""
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()

            # start background frame thread
            BaseCamera.thread = threading.Thread(target=self._thread, daemon=True)
            BaseCamera.thread.start()

            # wait until first frame is available
            BaseCamera.event.wait()

    def get_frame(self):
        """Return the current camera frame."""
        BaseCamera.last_access = time.time()

        # wait for a signal from the camera thread
        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        """"Generator that returns frames from the camera."""
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        BaseCamera.thread = None


if test:
    # cv2
    class Camera(BaseCamera):
        video_source = 0

        def __init__(self):
            if os.environ.get('OPENCV_CAMERA_SOURCE'):
                Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
            super(Camera, self).__init__()

        @staticmethod
        def set_video_source(source):
            Camera.video_source = source

        @staticmethod
        def frames():
            camera = cv2.VideoCapture(Camera.video_source)
            if not camera.isOpened():
                raise RuntimeError('Could not start camera.')

            while True:
                # read current frame
                _, img = camera.read()

                # encode as a jpeg image and return it
                yield cv2.imencode('.jpg', img, params=[cv2.IMWRITE_JPEG_QUALITY, 50])[1].tobytes()
else:
    # Picamera2
    class Camera(BaseCamera):
        @staticmethod
        def frames():
            with Picamera2() as camera:
                config = camera.create_video_configuration(
                    main={"size": (640, 480)},
                    raw={"size": (640, 480)},  # Match sensor readout to output
                    encode="main",
                    queue=False  # Critical for low latency
                )
                camera.configure(config)

                # from libcamera import controls
                # # Disable auto-exposure and other latency-inducing features
                # controls = {
                #     "AfMode": controls.AfModeEnum.Manual,
                #     "ExposureTime": 10000,  # Lock exposure if possible
                #     "AwbMode": controls.AwbModeEnum.Indoor  # Lock white balance
                # }
                # picam2.set_controls(controls)

                camera.start()

                ## let camera warm up
                #time.sleep(2)

                #stream = io.BytesIO()
                try:
                    while True:
                        buffer = camera.capture_array()

                        # Fastest possible JPEG conversion
                        _, jpeg = cv2.imencode(
                            ".jpg",
                            buffer,
                            params=[cv2.IMWRITE_JPEG_QUALITY, 50]
                        )
                        if not _:
                            continue
                        yield jpeg.tobytes()
                        # camera.capture_file(stream, format='jpeg')
                        # stream.seek(0)
                        # yield stream.read()

                        # # reset stream for next frame
                        # stream.seek(0)
                        # stream.truncate()
                finally:
                    camera.stop()


def video_stream_generator():
    camera = Camera()
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'

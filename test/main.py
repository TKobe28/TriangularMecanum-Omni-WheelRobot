from flask import Flask, Response
from picamera2 import Picamera2
import cv2

# Initialize Flask app and Picamera2
app = Flask(__name__)
camera = Picamera2()
camera_config = camera.create_video_configuration()
camera.configure(camera_config)
camera.start()

def generate_frames():
    """Yields frames from the camera as JPEG-encoded images."""
    while True:
        frame = camera.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Endpoint that serves the video feed."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Simple HTML page to display the video feed."""
    return '''
        <html>
        <head>
            <title>Live Feed</title>
        </head>
        <body>
            <h1>Raspberry Pi Camera Live Feed</h1>
            <img src="/video_feed" style="width:100%; max-width:640px;">
        </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
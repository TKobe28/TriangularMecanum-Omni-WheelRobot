from flask import Flask, Response, request, jsonify
import cv2
import typing
test = True
if not test:
    from picamera2 import Picamera2

    camera = Picamera2()
    camera_config = camera.create_video_configuration()
    camera.configure(camera_config)
    camera.start()

# Initialize Flask app and Picamera2
app = Flask(__name__)

if not test:
    def generate_frames():
        """Yields frames from the camera as JPEG-encoded images."""
        while True:
            frame = camera.capture_array()
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
else:
    with open("goofy_ahh.jpg", "rb") as f:
        image = f.read()

    def generate_frames():
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Endpoint that serves the video feed."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


control_function: typing.Callable = lambda vx, vy, omega: (0, "")


@app.route("/control", methods=['POST'])
def control():
    data = request.json
    if not data or not all(k in data for k in ('vx', 'vy', 'omega')):
        print("Nono request")
        return jsonify({"error": "Missing parameters"}), 400

    vx = data['vx']
    vy = data['vy']
    omega = data['omega']
    print("now control ihihiiha")
    result = control_function(vx, vy, omega)
    return jsonify(result)


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
    app.run(host='0.0.0.0', port=5000, debug=True)

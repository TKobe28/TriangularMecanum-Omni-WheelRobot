from flask import Flask, Response, request, jsonify, render_template, send_from_directory
import os
import cv2
import typing
from functools import wraps, cache
import hashlib

try:
    from picamera2 import Picamera2
    test = False

except ModuleNotFoundError:
    print("Picamera not installed, running in test mode")
    test = True

if not test:
    camera = Picamera2()
    camera_config = camera.create_video_configuration()
    camera.configure(camera_config)
    camera.start()

hashing_function = cache(hashlib.sha256)  # possible memory overflow uwu
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

users: list[tuple[str, str, int]] or [] = []  # [(username1, pass1, access_level1), (username2, pass2, access_level1), ...]
with open("./secret", "r") as f:
    it = iter(f)

    for user, password, access_level in zip(it, it, it):
        users.append((user.strip(), password.strip(), int(access_level)))

    if len(user) < 2:
        print("There are no registered users! Adding test user ('user', 'testpass')")
        users.append(('user', '13d249f2cb4127b40cfa757866850278793f814ded3c587fe5889e889a7a9f6c', 1))


def check_auth(username: str, password: str, access_level: int = 0):
    """Check if a username/password combination is valid."""
    password = hashing_function(password.encode(), usedforsecurity=True).hexdigest()
    for _username, _password, _access_level in users:
        if _username == username and _password == password and _access_level <= access_level:
            return True
    return False


def authenticate():
    """Send a 401 response to enable basic auth."""
    return Response(
        'Please login to access this page.',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(access_level=0):
    """Decorator to enforce basic authentication."""
    def decorator(f: typing.Callable):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password, access_level):
                if auth:
                    print(auth.username, auth.password)
                return authenticate()
            return f(*args, **kwargs)
        return decorated
    return decorator


@app.route('/logout', methods=['POST'])
def logout():
    return Response(
        'Logged out successfully.',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


@app.route('/video_feed')
@requires_auth(access_level=1)
def video_feed():
    """Endpoint that serves the video feed."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


control_function: typing.Callable = lambda vx, vy, omega: (0, "")


@app.route("/control", methods=['POST'])
@requires_auth(access_level=0)
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
@requires_auth(access_level=1)
def index():
    """Simple HTML page to display the video feed."""
    return render_template("index.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

import multiprocessing
import time
from flask import Flask, Response, request, jsonify, render_template, send_from_directory, render_template_string
import os
import typing
from functools import wraps, cache
import hashlib
import wifi_config

hashing_function = cache(hashlib.sha256)  # possible memory overflow uwu
app = Flask(__name__)
import camera
print("Imported camera!")

# users
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


@app.route('/stream_settings', methods=['POST'])
@requires_auth(access_level=0)
def stream_settings_handler():
    quality = request.json['quality']
    if not (type(quality) is int and 1 <= quality <= 100):
        return Response(status=400)
    camera.QUALITY = quality
    return Response(status=200)


wifi_semaphore = multiprocessing.Semaphore()  # todo: test!


@app.route('/wifi')
@requires_auth(access_level=0)
def wifi_page():
    try:
        wifi_semaphore.acquire()
        return render_template("wifi.html")
    finally:
        wifi_semaphore.release()


@app.route("/wifi/status")
@requires_auth(0)
def wifi_status():
    time.sleep(1)
    return jsonify({
        'connected': False,
        'internet': False,
        'network name': None
    })


@app.route('/wifi/connect', methods=['POST'])
@requires_auth(0)
def connect_wifi():  # todo: security, check if ok, return actual status (though unnecessary as the sender disconnects anyway)
    if request.json['hotspot'] == True:
        statuscode = wifi_config.start_hotspot(request.json['ssid'], request.json['password'])
    else:
        statuscode = wifi_config.connect_to_wifi(request.json['ssid'], request.json['password'])
    return Response(status=statuscode)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

import movement
import control
from sys import platform
if platform.uname().system.lower()=='linux':
    print("Detected Linux, Preparing gunicorn")        
    import gunicorn.app.base

    class StandaloneApplication(gunicorn.app.base.BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application


if __name__ == "__main__":
    movement_ = movement.Movement()
    control.control_function = movement_.move_robot

    if platform.uname().system.lower()=='linux':
        options = {
            'bind': '%s:%s' % ('0.0.0.0', '5000'),
            'workers': 2,
            'timeout': 120,
        }
        StandaloneApplication(control.app, options).run()
    else:
        print("Starting flask test mode as it's not linux this yes")
        control.app.run(host='0.0.0.0', port=5000, debug=False)

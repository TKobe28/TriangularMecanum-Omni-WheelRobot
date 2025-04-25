import leds
leds.turn_led("red", True)
import movement
import control
import wifi_config
import atexit
try:
    import button
    button.activation_function = wifi_config.start_hotspot
except ModuleNotFoundError:
    pass

movement_ = movement.Movement()
control.control_function = movement_.move_robot

leds.turn_led("green", True)
if __name__ == "__main__":
    control.app.run(host='0.0.0.0', port=5000, debug=False)

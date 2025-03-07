import movement
import control

if __name__ == "__main__":
    movement_ = movement.Movement()
    control.control_function = movement_.move_robot

    control.app.run(host='0.0.0.0', port=5000, debug=False)

import sys
import atexit
import numpy as np
import math
import traceback
import time
import leds

try:
    import RPi.GPIO as GPIO
    test = False
    GPIO.setmode(GPIO.BCM)

    @atexit.register
    def clear_GPIO():
        GPIO.cleanup()

except ModuleNotFoundError:
    print("Could not import movement libraries, running in test mode.")
    test = True
    import matplotlib.pyplot as plt
    from matplotlib._pylab_helpers import Gcf as __Gcf  # so we can handle window updates ourselves


MIN_DUTY = 25


class Movement:
    class Motor:
        pwm_freq = 1000

        def __init__(self, pins: [int], angle: float, id=69, small_wheels_angle: float = math.radians(45), reversed: bool=False):
            self.id = id
            self.pins = pins
            self.pwms = []
            self.angle = angle  # the angle from forward vector
            self.speed = 0
            self.small_wheels_angle = small_wheels_angle
            self.phi = self.angle + self.small_wheels_angle
            self.reversed = reversed
            if not test:
                for pin in self.pins:
                    GPIO.setup(pin, GPIO.OUT)
                    self.pwms.append(pwm := GPIO.PWM(pin, self.pwm_freq))
                    pwm.start(0)

        def set_speed(self, speed: float):
            if self.reversed:
                speed = -speed
            self.speed = speed
            if abs(speed) < 1e-2:
                speed = 0

            if speed > 0:
                duty = max(abs(speed), MIN_DUTY)
                self.pwms[0].ChangeDutyCycle(duty)
                self.pwms[1].ChangeDutyCycle(0)
            elif speed < 0:
                duty = max(abs(speed), MIN_DUTY)
                self.pwms[0].ChangeDutyCycle(0)
                self.pwms[1].ChangeDutyCycle(duty)
            else:
                self.pwms[0].ChangeDutyCycle(0)
                self.pwms[1].ChangeDutyCycle(0)

    def __init__(self):
        self.motors = [
            self.Motor([7, 1],   math.radians(60),  id=1, small_wheels_angle=math.radians(-45), reversed=True),  # this one is right edition wheel and reversed because it's wired wrong uwu
            self.Motor([25, 8],  math.radians(180), id=2),
            self.Motor([20, 21], math.radians(300), id=3),
        ]
        self.orientation = 0

    def move_robot(self, vx, vy, omega):
        """
        Move the robot with the given velocity vector and angular velocity.
        Maintains the correct speed ratio while ensuring all speeds stay in [-100, 100].
        """
        print(f"Moving with vx={vx}, vy={vy}, omega={omega}")
        leds.turn_led("blue", not (vx == vy == omega == 0))
        try:
            self.orientation += omega
            speeds = []

            # Compute raw speeds
            for motor in self.motors:
                speed = -1 * (vx * math.cos(motor.phi) + vy * math.cos(motor.phi)) + omega  # idk why * -1
                speeds.append(speed)

            # Find the maximum absolute speed
            max_speed = max(abs(s) for s in speeds)

            # Scale speeds if the max is over 100
            if max_speed > 100:
                scaling_factor = 100 / max_speed
                speeds = [s * scaling_factor for s in speeds]

            # Set the adjusted speeds
            for motor, speed in zip(self.motors, speeds):
                motor.set_speed(speed)

            return 0, ""
        
        except Exception as e:
            return -1, traceback.format_exc()

    def test_movement(self):
        self.move_robot(6, 6, 50)
        time.sleep(10)


if test:  # so that we can test stuff on pc, not just on the py
    __TK = None

    def updater():
        while True:
            global __TK
            if __Gcf.figs == {}:
                __TK = None
            else:
                if __TK == None:
                    __TK = __Gcf.get_active().window
                __TK.update()

    class Movement(Movement):  # sowy
        class Motor(Movement.Motor):
            def set_speed(self, speed):
                self.speed = speed

        def __init__(self):
            self.dx = 0
            self.dy = 0
            super().__init__()

        def move_robot(self, vx, vy, omega):
            self.dx = vx
            self.dy = vy
            return super().move_robot(vx, vy, omega)

        def test_movement(self):
            """Test the robot's movement with predefined commands."""
            # Move forward
            self.move_robot(1.0, 0.0, 0.0)
            self.visualise(name="forward")

            # Move sideways
            self.move_robot(0.0, 1.0, 0.0)
            self.visualise(name="sideways")

            # Rotate in place
            self.move_robot(0.0, 0.0, np.pi / 4)
            self.visualise(name="rotate")

            # Move diagonally
            self.move_robot(1.0, 1.0, 0.0)
            self.visualise(name="diagonally")

            # Rotate while moving
            self.move_robot(-5.8, -3.4, np.pi / 4)
            self.visualise(name="idk")

            try:
                updater()
            finally:
                return

        def visualise(self, name: str = "test"):
            """Update the plot with the current robot position and orientation."""
            fig, ax = plt.subplots()
            plt.title(name)
            ax.set_aspect('equal')
            robot_arrow = None
            wheel_arrows = [None, None, None]
            wheel_labels = [None, None, None]

            # Draw the robot as an arrow
            robot_arrow = ax.arrow(
                0, 0, self.dx, self.dy,
                head_width=0.5, head_length=0.7, fc='blue', ec='blue'
            )
            body_points_x = []
            body_points_y = []
            for i, motor in enumerate(self.motors):
                # Calculate wheel position relative to the robot's center
                wheel_x = 5 * np.cos(motor.angle)  # + self.orientation)
                wheel_y = 5 * np.sin(motor.angle)  # + self.orientation)
                body_points_x.append(wheel_x)
                body_points_y.append(wheel_y)

                # Calculate wheel direction (perpendicular to the wheel angle)
                wheel_dx = -np.sin(motor.angle) * motor.speed  # + self.orientation
                wheel_dy = np.cos(motor.angle) * motor.speed  # + self.orientation

                wheel_arrows[i] = ax.arrow(
                    wheel_x, wheel_y, wheel_dx, wheel_dy,
                    head_width=0.2, head_length=0.3, fc='red', ec='red'
                )
                wheel_labels[i] = ax.text(wheel_x + 0.5, wheel_y, str(motor.id))

            plt.plot(body_points_x + [body_points_x[0]], body_points_y + [body_points_y[0]])

            plt.show(block=False)
            print("Updated plot")

    if __name__ == "__main__":
        test = Movement()
        test.test_movement()
        sys.exit()

# Run the test
if __name__ == "__main__":
    movement = Movement()
    movement.test_movement()

import sys
import atexit
import numpy as np
import math
import traceback

test = True
if not test:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)


    @atexit.register
    def clear_GPIO():
        GPIO.cleanup()

else:
    import matplotlib.pyplot as plt


class Movement:
    class Motor:
        pwm_freq = 1000

        def __init__(self, pins: [int], angle: float):
            self.pins = pins
            self.pwms = []
            self.angle = angle
            self.speed = 0
            if not test:
                for pin in self.pins:
                    GPIO.setup(pin, GPIO.OUT)
                    self.pwms.append(pwm := GPIO.PWM(pin, self.pwm_freq))  # 1 kHz PWM frequency
                    pwm.start(0)

        def set_speed(self, speed: float):
            self.speed = speed
            if speed > 0:
                self.pwms[0].ChangeDutyCycle(speed)
                self.pwms[1].ChangeDutyCycle(0)
            elif speed < 0:
                self.pwms[0].ChangeDutyCycle(0)
                self.pwms[1].ChangeDutyCycle(speed)
            else:
                self.pwms[0].ChangeDutyCycle(speed)
                self.pwms[1].ChangeDutyCycle(speed)

    def __init__(self):

        self.motors = [
            self.Motor([38, 40], math.radians(45)),
            self.Motor([28, 26], math.radians(165)),
            self.Motor([24, 22], math.radians(285))
        ]
        self.orientation = 0

    def move_robot(self, vx, vy, omega):
        """
        Move the robot with the given velocity vector and angular velocity.
        """
        print(vx, vy, omega)
        try:
            self.orientation += omega
            for motor in self.motors:
                speed = vx * math.cos(motor.angle) + vy * math.sin(motor.angle) + omega
                motor.set_speed(speed)
            return 0, ""
        except Exception as e:
            return -1, traceback.format_exc()


if test:
    class Movement(Movement):  # sowy
        class Motor(Movement.Motor):
            def set_speed(self, speed):
                self.speed = speed

        def __init__(self):
            self.fig, self.ax = plt.subplots()
            self.ax.set_xlim(-10, 10)
            self.ax.set_ylim(-10, 10)
            self.ax.set_aspect('equal')
            self.robot_arrow = None
            self.wheel_arrows = [None, None, None]
            super().__init__()

        def test_movement(self):
            """Test the robot's movement with predefined commands."""
            # Move forward
            self.move_robot(1.0, 0.0, 0.0)
            self.update_plot()
            plt.show(block=False)

            # Move sideways
            self.move_robot(0.0, 1.0, 0.0)
            plt.show(block=False)

            # Rotate in place
            self.move_robot(0.0, 0.0, np.pi / 4)
            plt.show(block=False)

            # Move diagonally
            self.move_robot(1.0, 1.0, 0.0)
            plt.show(block=False)

            # Rotate while moving
            self.move_robot(1.0, 0.0, np.pi / 4)
            plt.show(block=False)

        def update_plot(self):
            """Update the plot with the current robot position and orientation."""
            if self.robot_arrow is not None:
                self.robot_arrow.remove()
            for arrow in self.wheel_arrows:
                if arrow is not None:
                    arrow.remove()

            # Draw the robot as an arrow
            dx = np.cos(self.orientation)
            dy = np.sin(self.orientation)
            self.robot_arrow = self.ax.arrow(
                0, 0, dx, dy,
                head_width=0.5, head_length=0.7, fc='blue', ec='blue'
            )

            for i, motor in enumerate(self.motors):
                # Calculate wheel position relative to the robot's center
                wheel_x = 5 * np.cos(motor.angle + self.orientation)
                wheel_y = 5 * np.sin(motor.angle + self.orientation)

                # Calculate wheel direction (perpendicular to the wheel angle)
                wheel_dx = -np.sin(motor.angle + self.orientation) * motor.speed
                wheel_dy = np.cos(motor.angle + self.orientation) * motor.speed

                self.wheel_arrows[i] = self.ax.arrow(
                    wheel_x, wheel_y, wheel_dx, wheel_dy,
                    head_width=0.2, head_length=0.3, fc='red', ec='red'
                )
            print("Updated plot")

    if __name__ == "__main__":
        test = Movement()
        test.test_movement()
        plt.show()
        sys.exit()

# Run the test
if __name__ == "__main__":
    movement = Movement()


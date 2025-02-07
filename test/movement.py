import sys
import atexit
import numpy as np
import math
import traceback
import time

test = False
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
        pwm_freq = 5000

        def __init__(self, pins: [int], angle: float, id=69):
            self.id = id
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
            print(self.id, speed)
            if speed > 0:
                self.pwms[0].ChangeDutyCycle(abs(speed))
                self.pwms[1].ChangeDutyCycle(0)
            elif speed < 0:
                self.pwms[0].ChangeDutyCycle(0)
                self.pwms[1].ChangeDutyCycle(abs(speed))
            else:
                self.pwms[0].ChangeDutyCycle(abs(speed))
                self.pwms[1].ChangeDutyCycle(abs(speed))

    def __init__(self):

        self.motors = [
            self.Motor([20, 21], math.radians(45), 1),
            self.Motor([25, 8], math.radians(165), 2),
            self.Motor([7, 1], math.radians(285), 3)
        ]
        self.orientation = 0

    def move_robot(self, vx, vy, omega):
        """
        Move the robot with the given velocity vector and angular velocity.
        Maintains the correct speed ratio while ensuring all speeds stay in [-100, 100].
        """
        print(f"Moving with vx={vx}, vy={vy}, omega={omega}")
        
        try:
            self.orientation += omega
            speeds = []

            # Compute raw speeds
            for motor in self.motors:
                speed = vx * math.cos(motor.angle) + vy * math.sin(motor.angle) + omega
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
    movement.test_movement()

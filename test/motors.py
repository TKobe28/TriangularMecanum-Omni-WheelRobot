import RPi.GPIO as GPIO
import time

# Define GPIO pins
motor1_pins = [38, 40]  
motor2_pins = [28, 26]  
motor3_pins = [24, 22] 

# Setup GPIO
GPIO.setmode(GPIO.BCM)
motors = [motor1_pins] # , motor2_pins, motor3_pins]
for pins in motors:
    GPIO.setup(pins[0], GPIO.OUT)
    GPIO.setup(pins[1], GPIO.OUT)

def motor_control(pins, direction):
    if direction == "forward":
        GPIO.output(pins[0], GPIO.HIGH)
        GPIO.output(pins[1], GPIO.LOW)
    elif direction == "backward":
        GPIO.output(pins[0], GPIO.LOW)
        GPIO.output(pins[1], GPIO.HIGH)
    else:
        GPIO.output(pins[0], GPIO.LOW)
        GPIO.output(pins[1], GPIO.LOW)

try:
    # Example: Move Motor 1 forward, Motor 2 backward, Motor 3 stop
    motor_control(motor1_pins, "forward")
    motor_control(motor2_pins, "backward")
    motor_control(motor3_pins, "stop")
    time.sleep(5)

finally:
    # Cleanup
    GPIO.cleanup()

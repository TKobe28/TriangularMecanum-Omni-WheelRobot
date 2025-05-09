import RPi.GPIO as GPIO
import time

# Define GPIO pins
motor1_pins = [20, 21]
motor2_pins = [25, 8]
motor3_pins = [7, 1]

# PWM frequency in Hz
PWM_FREQ = 5000

# Setup GPIO
GPIO.setmode(GPIO.BCM)
motors = [motor1_pins, motor2_pins, motor3_pins]

# Initialize motor pins as outputs and PWM
pwm_objects = []

for pins in motors:
    GPIO.setup(pins[0], GPIO.OUT)
    GPIO.setup(pins[1], GPIO.OUT)
    
    pwm1 = GPIO.PWM(pins[0], PWM_FREQ)
    pwm2 = GPIO.PWM(pins[1], PWM_FREQ)
    
    pwm1.start(0)  # Start with 0% duty cycle
    pwm2.start(0)
    
    pwm_objects.append((pwm1, pwm2))

def pwm_test(pwm1, pwm2):
    """ Ramps up and down PWM duty cycle """
    try:
        for duty_cycle in range(0, 101, 10):  # Increase duty cycle
            pwm1.ChangeDutyCycle(duty_cycle)
            pwm2.ChangeDutyCycle(100 - duty_cycle)
            time.sleep(0.1)

        for duty_cycle in range(100, -1, -10):  # Decrease duty cycle
            pwm1.ChangeDutyCycle(duty_cycle)
            pwm2.ChangeDutyCycle(100 - duty_cycle)
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        pass

try:
    for i, (pwm1, pwm2) in enumerate(pwm_objects):
        print(i)
        pwm_test(pwm1, pwm2)
    print("Test done")
finally:
    # Cleanup
    for pwm1, pwm2 in pwm_objects:
        pwm1.stop()
        pwm2.stop()
    GPIO.cleanup()

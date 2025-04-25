import RPi.GPIO as GPIO
import time

# red, green, blue
led_pins = [27, 17, 22]  # Adjust as needed

GPIO.setmode(GPIO.BCM)

# Setup pins as output
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

def turn_led(which: str | int, on: bool):
    if type(which) is str:
        if which == "red":
            which = 0
        elif which == "green":
            which = 1
        else:  # default
            which = 2
    
    GPIO.output(pin, GPIO.HIGH if on else GPIO.LOW)


if __name__ == "__main__":
    try:
        while True:
            for pin in led_pins:
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(pin, GPIO.LOW)
                time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

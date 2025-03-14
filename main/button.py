import RPi.GPIO as GPIO
import atexit  
import time
import typing

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
BUTTON_PIN = 19  # Pin number for the button
ACTIVATION_TIME = 10  # seconds

activation_function: typing.Callable = lambda : (print("OK"))
# Set up button pin as input with pull-up resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

global last_pressed
last_pressed = None


def button_pressed(channel):
    global last_pressed
    last_pressed = time.time()
    print("Button pressed (down)")
    GPIO.remove_event_detect(BUTTON_PIN)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_released, bouncetime=200)


def button_released(channel):
    global last_pressed
    if last_pressed is not None and time.time() - last_pressed >= ACTIVATION_TIME:
        print("Buttonr released - pressed long enough!")
        activation_function()
    else:
        print("Button released (up) - not long enough")
    GPIO.remove_event_detect(BUTTON_PIN)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=button_pressed, bouncetime=200)
    

GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=button_pressed, bouncetime=200)

atexit.register(GPIO.cleanup)

if __name__ == "__main__":
    input()

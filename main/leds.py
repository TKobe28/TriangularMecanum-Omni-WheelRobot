import time
try:
    import RPi.GPIO as GPIO

    leds = {  # (state, pin_number)
        "red": (False, 27),
        "green": (False, 17),
        "blue": (False, 22),
    }

    GPIO.setmode(GPIO.BCM)

    # Setup pins as output
    for state, pin in leds:
        GPIO.setup(pin, GPIO.OUT)

    def turn_led(which: str, on: bool | None = None):
        state, pin = leds[which]

        if on is None:
            on = not state

        GPIO.output(pin, GPIO.HIGH if on else GPIO.LOW)

        print(f"Turned the {which} LED {'on' if on else 'off'}." if not on == state
              else f"The {which} LED is already {'on' if on else 'off'}.")

        leds[which] = (on, pin)


    if __name__ == "__main__":
        try:
            while True:
                for led_name in leds.keys():
                    turn_led(led_name)
                    time.sleep(0.2)

        except KeyboardInterrupt:
            pass
        finally:
            GPIO.cleanup()
except ImportError:
    print("Not found libraries - using test virtual leds")

    leds = {
        "red": False,
        "green": False,
        "blue": False
    }

    def turn_led(which: str, on: bool | None = None):
        state = leds[which]

        if on is None:
            on = not state

        print(f"Turned the {which} LED {'on' if on else 'off'}." if not on == state
              else f"The {which} LED is already {'on' if on else 'off'}.")

        leds[which] = on

    if __name__ == "__main__":
        try:
            while True:
                for led_name in leds.keys():
                    turn_led(led_name)
                    time.sleep(0.2)

        except KeyboardInterrupt:
            pass

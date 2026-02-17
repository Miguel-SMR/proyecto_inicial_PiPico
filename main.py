from machine import Pin
import time

led_onboard = Pin(25, Pin.OUT)

while True:
    led_onboard.value(1)
    time.sleep(1)
    led_onboard.value(0)
    time.sleep(1)
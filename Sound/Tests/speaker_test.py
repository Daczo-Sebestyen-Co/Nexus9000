from machine import Pin
import time

speaker = Pin(2, Pin.OUT)

while True:
    speaker.value(1)
    time.sleep_us(1233)
    speaker.value(0)
    time.sleep_us(1233)
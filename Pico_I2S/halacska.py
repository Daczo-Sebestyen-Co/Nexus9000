import machine
import time
import math

op = machine.Pin(0, machine.Pin.OUT)

pitch = 440

while True:
    op.toggle()
    time.sleep_us(int((1/pitch)/2*1000000))


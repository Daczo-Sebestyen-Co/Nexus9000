import machine
import utime

Button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)

while True :
    print(Button.value())
    utime.sleep(1)

import pcf8574
from machine import I2C, Pin
import utime

asd = I2C(1, scl=Pin(3), sda=Pin(2))

pcf = pcf8574.PCF8574(asd, 0x20)

# set pin 3 HIGH
pcf.pin(0, 0)
pcf.pin(1, 1)

a = pcf.pin(3)

while True:
    print(pcf.pin(0))
    utime.sleep(0.1)
    



from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)

line_I = bytearray([0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10])
line_II = bytearray([0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18])
line_III = bytearray([0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C])
line_IIII = bytearray([0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E])
line_IIIII = bytearray([0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F])
lcd.custom_char(0, line_I)
lcd.custom_char(1, line_II)
lcd.custom_char(2, line_III)
lcd.custom_char(3, line_IIII)
lcd.custom_char(4, line_IIIII)
barN = 10
value = 0

while True:
    #if value >= barN*5+1:
    #    break
    lcd.clear()
    for i in range(80):
        if (value) > ((i+1)*5):
            lcd.putstr(chr(4))
        elif (value) == ((i+1)*5):
            lcd.putstr(chr(4))
            break
        else :
            if 0 == value-i*5-1:
                lcd.putstr(chr(0))
            elif 1 == value-i*5-1:
                lcd.putstr(chr(1))
            elif 2 == value-i*5-1:
                lcd.putstr(chr(2))
            elif 3 == value-i*5-1:
                lcd.putstr(chr(3))
    value = value + 1
    sleep(0.1)
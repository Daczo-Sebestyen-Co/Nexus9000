from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)

rocket = bytearray([0x04, 0x0A, 0x1F,  0x04,  0x0E,  0x1B,  0x15,  0x00])
lcd.custom_char(0, rocket)

while True:
    print(I2C_ADDR)
    lcd.blink_cursor_on()
    lcd.putstr("I2C Address:"+str(I2C_ADDR)+"\n")
    lcd.putstr("Hi! I'm working!")
    lcd.putstr(chr(0))
    sleep(2)
    
    lcd.clear()
    lcd.putstr("I2C Address:"+str(hex(I2C_ADDR))+"\n")
    lcd.putstr("I'm still standing!")
    sleep(2)
    
    lcd.blink_cursor_off()
    lcd.clear()
    lcd.putstr("Backlight Test")
    
    for i in range(10):
        lcd.backlight_on()
        sleep(0.2)
        lcd.backlight_off()
        sleep(0.2)
        
    lcd.backlight_on()
    lcd.hide_cursor()
    
    for i in range(20):
        lcd.putstr(str(i))
        sleep(0.4)
        lcd.clear()
import gpio
from lcd_i2c import LCD_I2C

class LCD:
    def __init__(self, address, col=22, row=4):
        self.lcd = LCD_I2C(address, col, row)
        

    def write(self, template):
        self.lcd.write_text(template)

lcd =LCD(0x27)
lcd.write('01234678901234678922\n01234678901234678922\n01234678901234678922\n01234678901234678922')
lcd.lcd.clear()
lcd.lcd.write(5)


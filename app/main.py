import I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()

mylcd.lcd_display_string("SRE QUEST 2!", 1, 2)
mylcd.lcd_display_string("################", 2)

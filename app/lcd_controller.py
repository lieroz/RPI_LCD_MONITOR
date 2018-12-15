from multiprocessing import Process
from I2C_LCD_driver import LCD
from time import sleep


class LCD_controller(Process):
    LCD_DISPLAY_WIDTH = 16
    DELAY = 0.5

    def __init__(self, chan_out):
        super().__init__()
        self.chan_out = chan_out
        self.lcd = LCD()

    def run(self):
        while True:
            data = self.chan_out.get()
            self.write_string(data)

    def write_string(self, text):
        length = len(text)
        begin, straight = 0, True
        
        if length > LCD_controller.LCD_DISPLAY_WIDTH:
            while True:
                if not self.chan_out.empty():
                    break

                end = begin + self.LCD_DISPLAY_WIDTH

                if end == length:
                    straight = False
                elif begin == 0:
                    straight = True

                self.lcd.lcd_display_string(text[begin:end], 1)
                sleep(LCD_controller.DELAY)

                if straight:
                    begin += 1
                else:
                    begin -= 1
        else:
            self.lcd.lcd_display_string(text, 1)


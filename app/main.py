from multiprocessing import Queue
from gpio_listener import GPIO_listener
from os_poller import OS_poller
from lcd_controller import LCD_controller


if __name__ == '__main__':
    q1 = Queue()
    q2 = Queue()

    g = GPIO_listener(q1)
    osp = OS_poller(q1, q2)
    lcd = LCD_controller(q2)

    lcd.start()
    osp.start()
    
    lcd.join()
    osp.join()


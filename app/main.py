from multiprocessing import Queue
from gpio_listener import GPIO_listener
from os_poller import OS_poller
from lcd_controller import LCD_controller
from daemon import Daemon
import RPi.GPIO as GPIO
import argparse
import signal
import sys


def generic_signal_handler(_signo, _stack_frame):
    GPIO.cleanup()
    sys.exit(0)


def main():
    q1, q2 = Queue(), Queue()

    gpio_listener = GPIO_listener(q1)
    os_poller = OS_poller(q1, q2)
    lcd_controller = LCD_controller(q2)

    os_poller.start()
    lcd_controller.start()
    
    os_poller.join()
    lcd_controller.join()


class AppDaemon(Daemon):
    def __init__(self, pidfile):
        super().__init__(pidfile) 

    def run(self):
        main()
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--daemonize", action="store_true",
                    help="daemonize app")
    args = parser.parse_args()
    signal.signal(signal.SIGTERM, generic_signal_handler)

    if args.daemonize:
        d = AppDaemon("lcd_pidfile")
        d.start()
    else:
        main()

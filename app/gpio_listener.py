import RPi.GPIO as GPIO


class GPIO_listener():
    BUTTON_PREV_GPIO = 11
    BUTTON_STATE_GPIO = 12
    BUTTON_NEXT_GPIO = 13

    def __init__(self, chan_in):
        self.chan_in = chan_in

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(GPIO_listener.BUTTON_PREV_GPIO, GPIO.IN, 
                pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO_listener.BUTTON_STATE_GPIO, GPIO.IN, 
                pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO_listener.BUTTON_NEXT_GPIO, GPIO.IN, 
                pull_up_down=GPIO.PUD_DOWN)
        
        GPIO.add_event_detect(GPIO_listener.BUTTON_PREV_GPIO, GPIO.RISING, 
                callback=lambda pin: self.button_prev_callback(pin))
        GPIO.add_event_detect(GPIO_listener.BUTTON_STATE_GPIO, GPIO.RISING, 
                callback=lambda pin: self.button_state_callback(pin))
        GPIO.add_event_detect(GPIO_listener.BUTTON_NEXT_GPIO, GPIO.RISING, 
                callback=lambda pin: self.button_next_callback(pin))

    def button_prev_callback(self, pin):
        self.chan_in.put(pin)
    
    def button_state_callback(self, pin):
        self.chan_in.put(pin)

    def button_next_callback(self, pin):
        self.chan_in.put(pin)

    def __del__(self):
        GPIO.cleanup()


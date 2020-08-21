# import RPi.GPIO as GPIO

# #####################The basic code of LED control##########################

# GPIO.setmode(GPIO.BCM)      #select bread board type(BCM, BOARD)
# GPIO.setwarnings(False)   #simplified warning = False
# GPIO.setup(8, GPIO.OUT)   #LED -> output, 8th pin used

# GPIO.output(8, 0)           # 1: turn on  , 0: turn off


# #initialization
# GPIO.cleanup


############ LED control 10 repeat ##########################
import RPi.GPIO as GPIO
import time

led_pin1 = 8
led_pin2 = 16
led_pin3 = 26
GPIO.setmode(GPIO.BCM)      #select bread board type(BCM, BOARD)
GPIO.setwarnings(False)   #simplified warning = False
GPIO.setup(led_pin1, GPIO.OUT)   #LED -> output, 8th pin used
GPIO.setup(led_pin2, GPIO.OUT)
GPIO.setup(led_pin3, GPIO.OUT)


for i in range(10):
    GPIO.output(led_pin1, 1)
    GPIO.output(led_pin2, 1)
    GPIO.output(led_pin3, 1)
    time.sleep(1)
    GPIO.output(led_pin1, 0)
    GPIO.output(led_pin2, 0)
    GPIO.output(led_pin3, 0)
    time.sleep(1)

GPIO.cleanup


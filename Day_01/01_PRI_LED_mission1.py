import RPi.GPIO as GPIO
import time


sensor = 4
led_pin1 = 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN)
GPIO.setup(led_pin1, GPIO.OUT)

print("Delect READY___!@!!!!!")
time.sleep(3)   #3sec waiting


while True:
    try:
        if GPIO.input(sensor) == 1:
            print("DETECTED!")
            GPIO.output(led_pin1, 1)
            time.sleep(1)
            GPIO.output(led_pin1, 0)
            time.sleep(0)
        if GPIO.input(sensor) == 0:
            print("Where are U?")
            time.sleep(0.2)
        

    except KeyboardInterrupt:
        GPIO.cleanup
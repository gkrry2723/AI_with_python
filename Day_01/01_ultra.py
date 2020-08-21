import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

TRGI = 23
ECHO = 24
print("Distance measurement with Ultrasonic")

GPIO.setup(TRGI, GPIO.OUT)  #발사
GPIO.setup(ECHO, GPIO.IN)   #받기

GPIO.output(TRGI, False)    # 대기해라
print("Waiting for sensor to settle")
time.sleep(2)   #대기

try:
    while True:
        GPIO.output(TRGI, True)
        time.sleep(0.00001)
        GPIO.output(TRGI, False)
        while GPIO.input(ECHO) == 0:    # 출발할때 time 체크
            start = time.time()
        while GPIO.input(ECHO) == 1:    # 신호 들어오면 time 체크
            stop = time.time()
        check_time = stop - start
        distance = check_time*34300/2
        print("Distance : %.3f cm" %distance)
        time.sleep(0.4)

except KeyboardInterrupt:
    print("Measuremenet stopped by User")
    GPIO.cleanup()
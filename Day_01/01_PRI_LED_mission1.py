import RPi.GPIO as GPIO
import time

# 20184754 김현주, 20184487 유채림 ---- day 1. mission1 -----
# mission: 센서등 시스템 설계
# 내용:  1. 시스템이 작동가능한 상태가 되면 Detect Ready 문구를 출력한다.
#       2. 센서에 움직임이 detect되면 Detect 문구가 출력되고 문이 LED에 불이 들어온다.
#       3. 센서에 움직임이 detect되지 않으면 Where are U 문구가 출력되고 LED에 불이 들어오지 않는다.
#       4. KeyboardInterrupt가 발생하면 작동을 멈춘다.

sensor = 4
led_pin1 = 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN)
GPIO.setup(led_pin1, GPIO.OUT)

print("Detect READY___!@!!!!!")
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

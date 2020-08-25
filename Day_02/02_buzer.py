import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)


p = GPIO.PWM(18, 100) #pulse 로 100
#Frq = [263, 294, 330, 349, 392, 440, 494] # 도레미파솔라시 주파수를 입력
Frq = [263, 263, 294, 263, 349, 330, 263, 263, 294, 263, 392, 349, 262, 262, 523, 440, 330, 294, 349, 349, 330, 262, 294, 262] # 생일축하합니다.
speed = 0.5

p.start(10) # 대기상태에 대한 기본적인 PWM

try:
    while 1:
        for fr in Frq:
            p.ChangeFrequency(fr)
            time.sleep(speed) # 음이 바뀌는 interval

except KeyboardInterrupt:
    pass
    p.stop()
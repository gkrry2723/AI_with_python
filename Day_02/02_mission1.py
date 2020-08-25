import RPi.GPIO as GPIO
import time
from lcd import lcddriver

# 20184754 김현주, 20184487 유채림 ---- day 2. mission1 -----
# mission: 손님 맞이 로봇 만들기
# 내용:  1. 동작이 detect되면 화면에 "guest get in" 문구를 출력하고 환영 노래를 출력하고 LCD에 환영 문구를 출력하고 손님 수를 센다.
#       2. 동작이 detect 되지 않으면 lcd를 clear 한다.
#       3. 1과 2를 반복한다.
#       4. KeyboardInterrupt가 발생하면 작동을 멈추고 총 손님 수를 화면에 출력한다.


sensor = 4
buzzer = 18
display = lcddriver.lcd()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(sensor, GPIO.IN)

p = GPIO.PWM(buzzer, 100) #buzzer pulse 로 100
Frq = [263, 294, 330]   #환영 노래 음 설정->도레미
speed = 0.2
num = 0                 #손님 수를 count 하는 num 변수

try:
    while True:
        if GPIO.input(sensor) == 1:     #손님이 detect 되면
            p.start(10)
            print("guest get in")       #환영 문구 화면에 출력
            num= num+1                  #손님 수 추가 
            for fr in Frq:              #노래 출력
                p.ChangeFrequency(fr)
                time.sleep(speed) # 음이 바뀌는 interval
            p.stop()
            display.lcd_display_string("Welcome!",1)        #lcd에 환영 문구 출력
            display.lcd_display_string("Have a good time",2)
            time.sleep(2)
            
        if GPIO.input(sensor) == 0:
            time.sleep(0.2)
            display.lcd_clear()
            p.stop()
        

except KeyboardInterrupt:
    print("\n 최종 손님의 수는: ",num) # 손님 수 출력
    p.stop()
    GPIO.cleanup
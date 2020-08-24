import RPi.GPIO as GPIO
import time

# 20184754 김현주, 20184487 유채림 ---- day 1. mission2 -----
# mission: 자동문 시스템 설계
# 내용:  1. 문 가까이(30 cm 이내로) 가면 환영 문구가 출력되고 문이 5초 열림( 서보모터 180도 돌아가기)
#       2. 문에서 멀어지면(30 cm 이상으로) 문이 열린 뒤 5초 후에 닫히고 
#           아직 멀이지지 않은 상태라면( 30cm 이내) 멀어질 때 까지(30cm 이상) 문이 열려있는다.
#       3. 문이 닫힐 때, 문이 닫힌다는 문구가 나온다( 서보모터 0도-제자리- 로 돌아가기)


SERVO_PIN = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_PIN, 50)     #purse 폭을 바꿔서 전류의 양을 제어함. -> pwm 방식
servo.start(0)      # 처음 시작할때 0에서 부터 시작

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
        if distance <= 30.0:
            print("Distance : %.3f cm" %distance)
            print("Welcome. The door is opened. Have a nice time~!!")
            servo.ChangeDutyCycle(12.5)
            time.sleep(5)
            servo.ChangeDutyCycle(2.5)

            GPIO.output(TRGI, True)
            time.sleep(0.00001)
            GPIO.output(TRGI, False)
            while GPIO.input(ECHO) == 0:    # 출발할때 time 체크
                start = time.time()
            while GPIO.input(ECHO) == 1:    # 신호 들어오면 time 체크
                stop = time.time()
            check_time = stop - start
            distance = check_time*34300/2

            if distance > 30.0:              # 만약 사람이 아직 안지나가면 문을 계속 열고 있음. 사람과의 거리가 30 이상이면 그때 닫음
                print("The door is closed.")
                time.sleep(1)

        

except KeyboardInterrupt:
    print("Measuremenet stopped by User")
    GPIO.cleanup()

from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO
from lcd import lcddriver
import time

app = Flask(__name__) #app server file을 main host만 use하고자 할때 사용. name이 main으로 바뀌며 가동됨.

SERVO_PIN = 21
TRGI = 23
ECHO = 24
BUZER = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT, initial=GPIO.HIGH) #처음에 불이 꺼진 상태로 시작한다
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(TRGI, GPIO.OUT)  
GPIO.setup(ECHO, GPIO.IN)   
GPIO.setup(BUZER, GPIO.OUT)

GPIO.output(TRGI, False)    # 대기해라
servo = GPIO.PWM(SERVO_PIN, 50)
display = lcddriver.lcd()
p = GPIO.PWM(BUZER, 100)
Frq = [263, 263, 294, 263, 349, 330, 263, 263, 294, 263, 392, 349, 262, 262, 523, 440, 330, 294, 349, 349, 330, 262, 294, 262] # 생일축하합니다.
speed = 0.3

##############################     1. 루트에 넣기   ########################################
@app.route("/") #route는 web 상에서 하는 root를 말함.
def hello():
    return render_template("index.html")    #html 가져오기
    return "SMART HOME"


##############################     2. 서브 루트에 넣기   ########################################

## 1. 불키기
@app.route("/led/on") #subroute
def led_on():
    try:
        GPIO.output(14,GPIO.HIGH)
        display.lcd_display_string("LED on",1)
        time.sleep(5)       
        display.lcd_clear()
        return "ok"
    except expression as identifier:
        return "fail"

## 2. 불끄기    
@app.route("/led/off") #subroute
def led_off():
    try:
        GPIO.output(14,GPIO.LOW)
        display.lcd_display_string("LED off",1)
        time.sleep(5)       
        display.lcd_clear()
        return "ok"
    except expression as identifier:
        return "fail"

## 3. cleanup
@app.route("/gpio/cleanup") #subroute
def gpio_cleanup():
    GPIO.cleanup()
    return "GPIO CLEAN UP"

## 4. 에어컨 키기 -> 창문 닫고(서보) LCD에 내용 출력
@app.route("/temperature/high")
def temperature_high():
    try:
        servo.start(0)
        servo.ChangeDutyCycle(6.0)
        display.lcd_display_string("Temp is high",1)
        display.lcd_display_string("Aircondi on",2)
        time.sleep(5)       
        display.lcd_clear()
        return "ok"
    except expression as identifier:
        return "fail"

## 5. 에어컨 끄기 -> 창문 열고(서보) LCD에 내용 출력
@app.route("/temperature/low")
def temperature_low():
    try:
        servo.start(0)
        servo.ChangeDutyCycle(2.5)
        display.lcd_display_string("Temp is low",1)
        display.lcd_display_string("Aircondi off",2)
        time.sleep(5)       
        display.lcd_clear()
        return "ok"
    except expression as identifier:
        return "fail"

# 6. 침대 가까이 누우면 초음파 센서가 detect하여 불을 끄고, LCD에 출력하고 자장가를 불러줌(buzer)
#    멀어지면 불이 켜진다.
@app.route("/sleep_care/on")
def sleep_care_on():
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

            if distance <= 8.0:
                GPIO.output(14,GPIO.LOW)
                display.lcd_display_string("Light off",1)
                display.lcd_display_string("Sleep tight!",2)
                time.sleep(5)       
                display.lcd_clear()
                p.start(10)
                for fr in Frq:
                    p.ChangeFrequency(fr)
                    time.sleep(speed)
                p.stop()
                
                GPIO.output(TRGI, True)
                time.sleep(0.00001)
                GPIO.output(TRGI, False)
                while GPIO.input(ECHO) == 0:    # 출발할때 time 체크
                    start = time.time()
                while GPIO.input(ECHO) == 1:    # 신호 들어오면 time 체크
                    stop = time.time()
                check_time = stop - start
                distance = check_time*34300/2

                if distance > 13.0: 
                    GPIO.output(14,GPIO.HIGH)
                    display.lcd_display_string("Light on",1)
                    display.lcd_display_string("Good morning!",2)
                    time.sleep(5)       
                    display.lcd_clear()
                    time.sleep(1)
        return "ok"
    except expression as identifier:
        return "fail"

if __name__ == "__main__":   #host에서 실행되면
    app.run(host="0.0.0.0") #실행되면 local host에서 실행시켜라(0.0.0.0: local host. 인터넷이 연결되지 않아도 실행되는 로컬 웹)
                            #실행시켜서 나오는 5000은 외부 포트
                            # 실행시키고 나서 누가 들어오면 콘솔에 누가 들어왔는지 뜸

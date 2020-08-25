from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__) #app server file을 main host만 use하고자 할때 사용. name이 main으로 바뀌며 가동됨.

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW) #처음에 불이 꺼진 상태로 시작한다


##############################     1. 루트에 넣기   ########################################
@app.route("/") #route는 web 상에서 하는 root를 말함.
def hello():
    return "SMART HOME"


##############################     2. 서브 루트에 넣기   ########################################
@app.route("/led/on") #subroute
def LED_on():
    GPIO.output(14,GPIO.HIGH)
    return "LED on"
    
@app.route("/led/off") #subroute
def LED_off():
    GPIO.output(14, GPIO.LOW)
    return "LED_off"

@app.route("/gpio/cleanup") #subroute
def gpio_cleanup():
    GPIO.cleanup()
    return "GPIO CLEAN UP"


if __name__ == "__main__":   #host에서 실행되면
    app.run(host="0.0.0.0") #실행되면 local host에서 실행시켜라(0.0.0.0: local host. 인터넷이 연결되지 않아도 실행되는 로컬 웹)
                            #실행시켜서 나오는 5000은 외부 포트
                            # 실행시키고 나서 누가 들어오면 콘솔에 누가 들어왔는지 뜸
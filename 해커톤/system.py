########################################################################################
# 1. 팀: 유채림팀
# 2. 팀원: 20184754 김현주, 20194487 유채림
# 3. 내용: open cv를 통해 얼굴인식을 하여 마스크를 끼고있는지 여부를 확인하여
#           착용중이면 LCD에 착용중이라는 문구를 출력하고
#           착용하지 않았다면 착용하지  않았다는 문구를 출력하고 서보모터로 마스크를 가져다 준다. 
##########################################################################################
import RPi.GPIO as GPIO
import time
import picamera
import cv2
import cv2 as cv
import numpy as np
import lcddriver

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 입술색이라고 판단할 색의 범위를 설정
Color_Lower = (46,130,36)
Color_Upper = (200, 200, 255)

SERVO_PIN = 21
TRGI = 5
ECHO = 6
BUZER = 18

print("Distance measurement with Ultrasonic")

GPIO.setup(TRGI, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUZER, GPIO.OUT)

display = lcddriver.lcd()
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(2.5) 
p = GPIO.PWM(BUZER, 100)
Frq=[349, 349, 349]
speed = 0.3

GPIO.output(TRGI, False)
print("Waiting for sensor to settle")
time.sleep(1)

try:
    while True:
        # 1. 초음파로 사람이 문 앞으로 왔는지(외출할 것인지) 확인 
        GPIO.output(TRGI, True)
        time.sleep(0.00001)
        GPIO.output(TRGI, False)
        while GPIO.input(ECHO) == 0:
            start = time.time()
        while GPIO.input(ECHO) == 1:
            stop = time.time()
        check_time = stop - start
        distance = check_time*34300/2
        print("Distance : %.1f cm" %distance)

        #만약 문앞으로 왔다면
        if distance<10:
            display.lcd_display_string("Welcome!",1)
            display.lcd_display_string("come here!",2)
            time.sleep(2)       
            display.lcd_clear()
            #2. 카메라로 문 앞에 온 사람의 사진을 찍음
            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)
                camera.start_preview()
                display.lcd_display_string("Please look here",1)
                display.lcd_display_string("for 5 second",2)
                time.sleep(2)       
                display.lcd_clear()
                time.sleep(1)
                camera.start_recording('test1.h264')
                camera.wait_recording(3)
                camera.stop_recording()
                camera.capture('test.jpg')
                camera.stop_preview()
            
            #3. 찍은 사진으로 얼굴 인식하기 
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

            img = cv2.imread('test.jpg')

            gray = cv2.cvtColor(img, cv.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            #4-1. 마스크를 끼고 있는 경우, 얼굴로 인식이 되지 않는 경우가 다반사이다.
            #     초음파 센서 10CM 가까이 온 경우는 거의 대부분 외출을 위해 온 경우라고 판단하여 이런 경우 마스크를 끼고 있다고 판단한다.
            if len(faces) == 0:
                print('mask on.(1)')
                display.lcd_display_string("Mask detected!",1)
                display.lcd_display_string(" ",2)
                time.sleep(5)       
                display.lcd_clear()
                GPIO.cleanup()    
                cv.waitKey(0)
                cv.destroyAllWindows()
                raise SystemExit
                break
            
            #4-2. 얼굴 인식이 된 경우 위에서 정한 색의 범위로 입술부분을 찾는다.
            for (x,y,w,h) in faces:

                cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]

                nh=int(h/3)
                nw=int(w/3)

                dot = img[y+nh+nh:y+h,x+nw:x+nw+nw]
                dot = cv2.GaussianBlur(dot, (11, 11),1)
                hsv = cv2.cvtColor(dot, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, Color_Lower, Color_Upper)
                
                print(mask)
                #cv2.imshow('mask', mask)

                a=1
                b=0

                for item in mask:
                    for no in item:
                        if no !=0:
                            a+=1
                        else:
                            b+=1

                # a: 붉은색이 있는 곳, b가 붉은색이 detect되지 않은곳
                #5-1. 붉은색이 거의 없다고 판단될때(사진상 입술이 없다.)
                #     마스크를 쓰고있기에 입술이 안보인다고 판단한다.
                if b/a > 70:
                    print('undetected',b/a)
                    display.lcd_display_string("Mask detected!",1)
                    display.lcd_display_string(" ",2)
                    time.sleep(5)       
                    display.lcd_clear()
                    exit()
                    GPIO.cleanup()    
                    cv.waitKey(0)
                    cv.destroyAllWindows()
                    quit()
                    break
                
                #5-2. 입술이 있다고 판단되는 경우
                #     마스크를 쓰지 않고있다고 판단하고
                #     -1) 부저를 울리고
                #     -2) LCD창에 이 상황을 알리고
                #     -3) 서보 모터로 마스크를 가져다 준다.
                else :
                    print('detected',b/a)
                    p.start(10)
                    for fr in Frq:
                        p.ChangeFrequency(fr)
                        time.sleep(speed)
                    p.stop()
                    display.lcd_display_string("YOu forgot ",1)
                    display.lcd_display_string("wearing mask!",2)
                    
                    servo.ChangeDutyCycle(12.5)
                    time.sleep(5)       
                    display.lcd_clear()
                    
                    display.lcd_display_string("Here you are ",1)
                    display.lcd_display_string("take your mask!",2)
                    time.sleep(10)
                    servo.ChangeDutyCycle(2.5)
                    display.lcd_clear()
                    exit()
                    GPIO.cleanup()    
                    cv.waitKey(0)
                    cv.destroyAllWindows()
                    quit()
                    break
                    
                    

    GPIO.cleanup()    
    cv.waitKey(0)
    cv.destroyAllWindows()

except KeyboardInterrupt:
    print("Measuremenet stopped by User")
    GPIO.cleanup()


import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

global lxy_BZ
lxy_BZ=0

def L_BUTTON(event,x,y,flags,param): 
    # 判断事件是否为 Left Button Double Clicck 
    if event == cv2.EVENT_LBUTTONDOWN:
        if x>280 and x<360 and y>88 and y<140:
            canvas=cv2.imread("JS.jpg")
            cv2.putText(canvas, text=temp, org=(130, 160), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
            cv2.putText(canvas, text=humi, org=(130, 260), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
            cv2.imshow("lxy",canvas)
            cv2.waitKey(10)
            GPIO.output(23, GPIO.HIGH)
        elif x>280 and x<360 and y>152 and y<196:
            canvas=cv2.imread("TS.jpg")
            cv2.putText(canvas, text=temp, org=(130, 160), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
            cv2.putText(canvas, text=humi, org=(130, 260), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
            cv2.imshow("lxy",canvas)
            cv2.waitKey(10)
            GPIO.output(23, GPIO.LOW)
        elif x>280 and x<360 and y>212 and y<256:
            canvas=cv2.imread("JF.jpg")
            cv2.putText(canvas, text=temp, org=(130, 160), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
            cv2.putText(canvas, text=humi, org=(130, 260), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
            cv2.imshow("lxy",canvas)
            cv2.waitKey(10)
            GPIO.output(24, GPIO.HIGH)
        elif x>280 and x<360 and y>272 and y<316:
            canvas=cv2.imread("TF.jpg")
            cv2.putText(canvas, text=temp, org=(130, 160), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
            cv2.putText(canvas, text=humi, org=(130, 260), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
            cv2.imshow("lxy",canvas)
            cv2.waitKey(10)
            GPIO.output(24, GPIO.LOW)
        elif x>32 and x<144 and y>336 and y<384:
            canvas=cv2.imread("ZD.jpg")
            GPIO.output(26, GPIO.HIGH)
            cv2.putText(canvas, text=temp, org=(130, 160), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
            cv2.putText(canvas, text=humi, org=(130, 260), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
            cv2.imshow("lxy",canvas)
            cv2.waitKey(10)
            global lxy_BZ
            lxy_BZ=1
        elif x>216 and x<336 and y>336 and y<384:
            canvas=cv2.imread("SD.jpg")
            GPIO.output(26, GPIO.LOW)
            cv2.putText(canvas, text=temp, org=(130, 160), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
            cv2.putText(canvas, text=humi, org=(130, 260), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
            cv2.imshow("lxy",canvas)
            cv2.waitKey(10)
            global lxy_BZ
            lxy_BZ=0
        #cv2.circle(img,(x,y),20,(255,0,0),-1) 
cv2.namedWindow('lxy')

cv2.setMouseCallback('lxy',L_BUTTON)
while True:
    channel =18
    data = []
    j = 0

    GPIO.setmode(GPIO.BCM)

    time.sleep(1)

    GPIO.setup(channel, GPIO.OUT)
    GPIO.setup(26, GPIO.OUT)

    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    #GPIO.output(23, GPIO.LOW)
    GPIO.output(channel, GPIO.LOW)
    time.sleep(0.02)
    GPIO.output(channel, GPIO.HIGH)
    GPIO.setup(channel, GPIO.IN)


    while GPIO.input(channel) == GPIO.LOW:
      continue
    while GPIO.input(channel) == GPIO.HIGH:
      continue

    while j < 40:
      k = 0
      while GPIO.input(channel) == GPIO.LOW:
        continue
      while GPIO.input(channel) == GPIO.HIGH:
        k += 1
        if k > 100:
          break
      if k < 8:
        data.append(0)
      else:
        data.append(1)

      j += 1

    #print ("sensor is working.")
    #print (data)
    humidity_bit = data[0:8]
    humidity_point_bit = data[8:16]
    temperature_bit = data[16:24]
    temperature_point_bit = data[24:32]
    check_bit = data[32:40]

    humidity = 0
    humidity_point = 0
    temperature = 0
    temperature_point = 0
    check = 0

    for i in range(8):
      humidity += humidity_bit[i] * 2 ** (7-i)
      humidity_point += humidity_point_bit[i] * 2 ** (7-i)
      temperature += temperature_bit[i] * 2 ** (7-i)
      temperature_point += temperature_point_bit[i] * 2 ** (7-i)
      check += check_bit[i] * 2 ** (7-i)

    tmp = humidity + humidity_point + temperature + temperature_point

    if check == tmp:
        print ("temperature :", temperature, "*C, humidity :", humidity, "%")

#    else:
#      print ("wrong")
#      print ("temperature :", temperature, "*C, humidity :", humidity, "% check :", check, ", tmp :", tmp)
    if check == tmp:
        canvas=cv2.imread("lxy.jpg")
        font = cv2.FONT_HERSHEY_SIMPLEX
        humi=str(humidity)
        temp=str(temperature)
        global lxy_BZ
        if  lxy_BZ==1:
            if humidity<20:
                GPIO.output(23, GPIO.HIGH)
            elif humidity>20:
                GPIO.output(23, GPIO.LOW)
            if temperature<30:
                GPIO.output(24, GPIO.LOW)
            elif temperature>30:
                GPIO.output(24, GPIO.HIGH)
        cv2.putText(canvas, text=temp, org=(130, 160), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
        cv2.putText(canvas, text=humi, org=(130, 260), fontFace=font, fontScale=1, thickness=2, lineType=cv2.LINE_AA, color=(0, 0, 250))
        cv2.imshow("lxy",canvas)
        cv2.waitKey(10)
GPIO.cleanup()  

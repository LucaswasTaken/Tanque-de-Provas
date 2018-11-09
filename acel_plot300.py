from mpu6050 import mpu6050
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpat
import cv2
import imutils
cap = cv2.VideoCapture(0)
sensor = mpu6050(0x68)

xmin = 0;
xmax = 10;
ymax = -8;
ymin = -12;
plt.axis([xmin, xmax, ymin, ymax])
plt.ion()
i = 0;
legendaconf = mpat.Patch(color='blue',label='Aceleracao')
legendaconf2 = mpat.Patch(color='red',label='Deslocamento')
first_legend = plt.legend(handles=[legendaconf],loc=1)
ax = plt.gca().add_artist(first_legend)
plt.legend(handles=[legendaconf2],loc=4)
while(True):
        time.sleep(0.1)
        accelerometer_data = sensor.get_accel_data();
        _, frame = cap.read()

        frame = imutils.resize(frame, 300)
    
        lower_red = np.array([0,0,100])
        upper_red = np.array([50,50,255])
    
        mask = cv2.inRange(frame, lower_red, upper_red)
        res = cv2.bitwise_and(frame,frame, mask= mask)
        #cv2.imshow('frame',frame)
        #cv2.imshow('mask',mask)
        cv2.imshow('res',res)
        mome = cv2.moments(mask,True)
        height, width = res.shape[:2]

    
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
                break
        
        
        y = accelerometer_data["x"]
        if (mome["m00"]!=0):
                yred = -(height-mome["m01"]/mome["m00"])/15
                plt.plot(i,yred,'.r-')

        plt.scatter(i, y)
        plt.pause(0.06)
        i=i+1;
        if (i==xmax-1):
                xmin = xmin+1;
                xmax = xmax+1;
                plt.axis([xmin, xmax, ymin, ymax])
cv2.destroyAllWindows()
cap.release()

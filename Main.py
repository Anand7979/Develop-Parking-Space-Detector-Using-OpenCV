import cv2
import numpy as np
import cvzone
import pickle

#Video Feed
cap=cv2.VideoCapture('carPark.mp4')

width, height=107,48

with open('CarParkPos','rb') as f:
    posList=pickle.load(f)

def checkParkingSpace(imgPro):
    spacecounter=0
    for pos in posList:
        x,y=pos
        imgcrop=imgPro[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),imgcrop)
        #cv2.rectangle(img,pos , (pos[0]+width, pos[1]+height), (255, 0, 255), 2)
        count=cv2.countNonZero(imgcrop)
        # cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1,thickness=2,offset=0,colorR=(0,0,255))

        if count<900:
            color=(0,255,0)
            thickness=5
            spacecounter +=1
        else:
            color=(0,0,255)
            thickness=3
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),color,thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img,f'Free: {spacecounter}/{len(posList)}', (100,50), scale=3, thickness=5, offset=20, colorR=(0, 200,0))

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES)== cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()
    imggray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgblur=cv2.GaussianBlur(imggray,(3,3),1)
    imgthres=cv2.adaptiveThreshold(imgblur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgmedian=cv2.medianBlur(imgthres,5)
    kernel=np.ones((3,3),np.uint8)
    imgdilate=cv2.dilate(imgmedian,kernel,iterations=1)
    checkParkingSpace(imgdilate)
    # for pos in posList:
    #     cv2.rectangle(img,pos , (pos[0]+width, pos[1]+height), (255, 0, 255), 2)
    cv2.imshow("Video",img)
    # cv2.imshow("Gray",imggray)
    # cv2.imshow("Blur",imgblur)
    # cv2.imshow("Thres",imgthres)
    # cv2.imshow("Median",imgmedian)
    # cv2.imshow("Dilate",imgdilate)
    cv2.waitKey(10)

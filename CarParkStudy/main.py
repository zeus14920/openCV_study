import cv2
import pickle
import cvzone
import numpy as np

#Video feed
cap = cv2.VideoCapture('carPark.mp4')

#사진에 라벨링 된 바이너리 파일 읽기
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48

def checkParkingSpace(imgPro):

    spaceCounter = 0

    for pos in posList:
        x,y = pos
        #rectangle을 먼저 적용시 테두리를 먼저 표시한 뒤 각 화면을 띄움, 이에 테두리도 함께 표시
        #cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
        imgCrop = imgPro[y:y+height,x:x+width]
        #cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        #cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1, thickness=2, offset= 0, colorR=(0,0,255))

        if count < 900:
            color = (0,255,0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20, colorR=(0,200,0))
while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,25,16)
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.ones((3,3),np.uint8)
    imgDialate = cv2.dilate(imgMedian, kernel, iterations=1)
    imgErode = cv2.erode(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDialate)
    #for pos in posList:
        #cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
    cv2.imshow("Image", img)
    #cv2.imshow("ImageBlur", imgBlur)
    #cv2.imshow("ImageThres", imgThreshold)
    #cv2.imshow("ImageMedian", imgMedian)
    #cv2.imshow("ImageDialate", imgDialate)
    #cv2.imshow("ImageErode", imgErode)
    cv2.waitKey(10)
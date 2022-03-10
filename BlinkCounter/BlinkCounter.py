import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture('Video.mp4')
# cvzone 활용, 얼굴의 윤곽선을 따라서 점을 찍어줌
detector = FaceMeshDetector(maxFaces=1)
# 그래프 창을 띄움, 최소 20에서 최대 50
# 0~100까지의 범위를 가질 수 있음
plotY = LivePlot(640, 360, [20, 50], invert=True)

# 윤곽선의 점들 중 특정 부분 지정
idList = [22, 23, 24, 26, 110, 110, 157, 158, 159, 160, 161, 130, 243]
# idList = [50,60,70]
ratioList = []
blinkCount = 0
counter = 0
color = (255, 0, 255)

while True:

    # 동영상의 현재 프레임 수(cv2.CAP_PROP_POS_FRAMES), 동영상의 총 프레임 수(cv2.CAP_PROP_FRAME_COUNT)
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # set() 함수 - 속성 수정
        # 현재 프레임 수와 총 프레임 수 같을 시 현재 프레임 수를 0으로 세팅
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    # 윤곽선의 점들을 그리지 않음
    img, faces = detector.findFaceMesh(img, draw=False)

    # 조건에 만족하는 경우만 윤곽선의 점에 색을 입혀 표시
    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 5, color, cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor, _ = detector.findDistance(leftLeft, leftRight)

        # 눈동자 위 아래 표시
        cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
        # 눈동자 좌 우 표시
        cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)
        ratio = int((lenghtVer / lenghtHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        #눈을 깜박일 때 초록색으로 아닐 때는 빨간색으로 표시
        #ratioAvg가 35이하 일 때 눈을 깜박임으로 인식
        if ratioAvg < 35 and counter == 0:
            blinkCount += 1
            color = (0, 200, 0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (255, 0,255)
        cvzone.putTextRect(img, f'Blink Count: {blinkCount}', (50, 100), colorR=color)

        # imgPlot = plotY.update(ratio)
        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        # cv2.imshow("ImagePlot", imgPlot)
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
    else:
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, img], 2, 1)

    # 이미지크기 확인
    # (720, 1280, 3) -> 세로(높이)x가로(넓이)x색(3)
    # print(img.shape)
    # 이미지 크기를 640x360으로 변환
    # img = cv2.resize(img,(640,360))
    cv2.imshow("Image", imgStack)
    cv2.waitKey(25)

#사진에 마우스 클릭을 통해서 라벨링 작업 및 바이너리 파일로 저장
import cv2
import pickle

width, height = 107, 48

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

# 마우스를 클릭 했을 때 이벤트
def  mouseClick(events, x, y, flags, params):
    #마우스 왼쪽을 눌렀을 때 posList에 x,y 좌표를 저장
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))

    #마우스 오른쪽을 눌렀을 때 x1,y1 값 저장
    #posList의 x,y 각각의 값이 x1~x1+width 그리고 y1~y1+height 값 사이에 있으면 x,y의 값 삭제
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1 = pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)

    #CarParkPos에 바이너리로 저장
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread('carParkImg.png')
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 2)
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)
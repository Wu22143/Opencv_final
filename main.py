
import cv2
import pickle
import cvzone
import numpy as np
 
#讀取影像檔
cap = cv2.VideoCapture('C:/Users/Yu_Cheng/Desktop/opencv_final/4A8G0023_final/carPark.mp4')
 
with open('park_list', 'rb') as f:
    posList = pickle.load(f)
 
width, height = 107, 48
 
 
def checkParkingSpace(imgPro):
    #計算停車場位置
    spaceCounter = 0
 
    for pos in posList:
        x, y = pos
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
        imgCrop = imgPro[y:y + height, x:x + width]
        #count:框選範圍內的像素點數量
        count = cv2.countNonZero(imgCrop)
        print(count)
 
        #如果小於900就判別為此車格沒有停車
        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
 
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
 
    cvzone.putTextRect(img, f'Park Space: {spaceCounter}/{len(posList)}', (300, 35), scale=3,
                           thickness=3, offset=10, colorR=(0,200,0))
while True:
 
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    #轉灰階
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #經過高思慮波-減少圖像的雜訊與細節
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    #自適應二值化
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    #中值濾波 減少噪點
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    #膨脹
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    cv2.waitKey(10)
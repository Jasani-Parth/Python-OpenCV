import cv2
import numpy as np

FrameWidth = 640
FrameHeight = 480

myColor = [[96, 83, 147, 119, 255, 255]]
color = [[255, 0, 0]]

mypoints = []


def findColor(Image):
    imgHSV = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)
    count = 0
    newpoints = []

    for color in myColor:
        lower = np.array(color[:3])
        upper = np.array(color[3:])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = ScanContours(mask)
        cv2.circle(imgResult, (x, y), 10, color[count], cv2.FILLED)

        if x != 0 and y != 0:
            newpoints.append([x, y, count])

        count += 1

    return newpoints


def ScanContours(Image):
    contours, hierarchy = cv2.findContours(Image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 0:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)

    return x + w // 2, y


def drawOnCanvas():
    for point in mypoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, color[point[2]], cv2.FILLED)


# code for webcam
video_capture = cv2.VideoCapture(0)
video_capture.set(3, FrameWidth)
video_capture.set(4, FrameHeight)

while True:
    message, img = video_capture.read()
    imgResult = img.copy()
    newPoints = findColor(Image=img)

    if len(newPoints) != 0:
        for p in newPoints:
            mypoints.append(p)

    if len(mypoints) != 0:
        drawOnCanvas()
         
    cv2.imshow("Live", img)
    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

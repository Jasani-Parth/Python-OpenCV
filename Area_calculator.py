import cv2
import random


def ScanContours(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        Area = cv2.contourArea(cnt)

        if Area > 500:
            cv2.drawContours(imgcontour, cnt, -1, (210, 20, 125), 3)
            perimeter = cv2.arcLength(cnt, True)
            corner = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            # print(len(corner))  this is number of corners so we can approximate shape by corner
            objCor = len(corner)
            x, y, w, h = cv2.boundingRect(corner)

            if objCor == 3:
                Type = "Triangle"
            elif objCor == 4:
                if w == h:
                    Type = "Square"
                else:
                    Type = "Rectangle"
            else:
                Type = "Circle"

            # cv2.rectangle(imgcontour, (x, y), (x + w, y + h), (0, 255, 0), 1) generating rectangle around shape
            cv2.putText(imgcontour, Type + f" {Area} ", (x + w // 2, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                        (0, 0, 0), 2)


if __name__ == "__main__":
    
    if random.randint(0, 5) < 2:
        img = cv2.imread("Photos/shapes2.png")
    else:
        img = cv2.imread("Photos/shapes.png")

    imgcontour = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, 50, 50)  # Detecting Edges Through Canny Image
    ScanContours(imgCanny)

    cv2.imshow("Finding Border", imgCanny)
    cv2.imshow("Image", imgcontour)
    cv2.waitKey(0)

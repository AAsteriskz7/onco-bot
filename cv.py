import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

folder_path = 'train\\benign'

def label(filename): 
    img = cv2.imread(filename)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    equalized_image = cv2.equalizeHist(gray)

    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(equalized_image, kernel, 2)
    eroded = cv2.erode(dilated, kernel, 2)

    blur = cv2.GaussianBlur(eroded, [11, 11], 15)    

    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)

    canny = cv2.Canny(thresh, 125, 175)

    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    center = (img.shape[1]//2, img.shape[0]//2)
    cv2.ellipse(mask, center, (int(img.shape[1]*0.3), int(img.shape[0]*0.5)), 0, 0, 360, 255, -1)

    result = cv2.bitwise_and(canny, canny, mask=mask)

    contours, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    c = 0
    for contour in contours:
        c = c+1
        if c == 15:
            return True
    
    for contour in contours:
        if (cv2.contourArea(contour) > 0):
            hull = cv2.convexHull(contour)
            if (cv2.contourArea(hull)*0.8 < cv2.contourArea(contour)):
                return True
    return False
            
correct = 0    
count = 0

if __name__ == "__main__":
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)


        if (os.path.isfile(file_path)):
            if (main(file_path)):
                correct = correct + 1
        count = count + 1

    print(str(correct) + "/" + str(count))
    print(correct/count*100)
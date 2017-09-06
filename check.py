import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
from imutils.perspective import four_point_transform
from imutils import contours
import argparse
import imutils
import cv2

def display(image):
    cv2.namedWindow("Image") 
    cv2.imshow("Image", image)  
    cv2.waitKey (0)  
    print("Output the image ...  \'ans.png\'")
    cv2.imwrite("./ans.png", paper, [int(cv2.IMWRITE_PNG_COMPRESSION), 9]) 
    cv2.destroyAllWindows()  


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged


def getMoment(cnts,bound=(200,50,4480,3980)):
    Answer = [(0,0)]
    for c in cnts :
        (x,y,w,h) = cv2.boundingRect(c)
        if x>bound[0] and x<bound[2] and y>bound[1] and y<bound[3]:
            M = cv2.moments(c)
            try :
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            except : 
                cX = 0 
                cY = 0
            Answer.append((cX,cY))

    return Answer

def getBlack(image,width=4500,height=4000,imgmode='RGB'):
    ### Picture Preprocess
    if imgmode == 'GRAY':
        gray = image
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    edged = auto_canny(blurred)
    cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    docCnt = None
    # ensure that at least one contour was found
    if len(cnts) > 0 :
        # sorted them in descending order
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        # approximate the contour
        for c in cnts :
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02*peri, True)
            # if find four point, we can assume we have found the paper, Complete.
            if len(approx) == 4 :
                docCnt = approx
                break

    ### 
    warped = four_point_transform(gray, docCnt.reshape(4,2))

    ### Recognized Multiple Choose
    thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY| cv2.THRESH_OTSU)[1]
    warped = cv2.resize(warped, (width,height), cv2.INTER_LANCZOS4)
    thresh = cv2.resize(thresh, (width,height), cv2.INTER_LANCZOS4)

    ChQImg = cv2.blur(thresh, (13,13))
    ChQImg = cv2.threshold(ChQImg, 10,255, cv2.THRESH_BINARY)[1]
    cnts = cv2.findContours(ChQImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    return cnts



# # Usage:
# image = cv2.imread('./test/test600-p3.png')
# cnt = getBlack(image)
# print(getMoment(cnt))

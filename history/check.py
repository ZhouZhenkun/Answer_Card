# python 3.5, numpy+mlk,scipy for openCV
# use imutils for four_point_transform
# matplotlib for drawing
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
from imutils.perspective import four_point_transform
from imutils import contours
import argparse
import imutils
import cv2


# Debug
path = '../test/4.png'
print("Drawing checked result in result.png")



# Re
width1 = 4500
height1 = 4000
border_width = 6
# width1 = 800
# height1 = 2000


def display(image):
    cv2.namedWindow("Image") 
    cv2.imshow("Image", image)  
    cv2.waitKey (0)  
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


### Picture Preprocess
# Read Picture 
image = cv2.imread(path)
# image = cv2.imread('./test/yooo.png')
# display(image)
# Convert into gray Picture 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Guass Filter
blurred = cv2.GaussianBlur(gray, (5,5), 0)
# display(blurred)

# Edge Detection
edged = auto_canny(blurred)
# display(edged)

# find corner
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



# *************************  check  ****************************
# Draw red point on the corner 
# newimage = image.copy()
# # newimage = cv2.resize(newimage, (800,2000), cv2.INTER_LANCZOS4)
# for i in docCnt :
#     cv2.circle(newimage, (i[0][0],i[0][1]), 1, (0,0,255), -1)
# # display(newimage)
# print(docCnt)

# cv2.imwrite("./four_point.png", newimage, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])  
# Reshape, four_point_transform
paper = four_point_transform(image, docCnt.reshape(4,2))
warped = four_point_transform(gray, docCnt.reshape(4,2))
# display(paper)





# # ********************************************************
# # If wanna Deborder
# def deborder(x):
#     x[0][0][0] += border_width
#     x[0][0][1] += border_width
#     x[1][0][0] += border_width
#     x[1][0][1] -= border_width
#     x[2][0][0] -= border_width
#     x[2][0][1] -= border_width
#     x[3][0][0] -= border_width
#     x[3][0][1] += border_width
#     return x

# newimage = image.copy()
# docCnt = deborder(docCnt)
# for i in docCnt :
#     cv2.circle(newimage, (i[0][0],i[0][1]), 1, (0,0,255), -1)
# # display(newimage)
# paper = four_point_transform(image, docCnt.reshape(4,2))
# warped = four_point_transform(gray, docCnt.reshape(4,2))
# # display(paper)
# ********************************************************






### Recognized Multiple Choose
# Resize into standard width & height
# gray to BMP
# thresh = cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,53,2)
# # display(thresh)
thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY| cv2.THRESH_OTSU)[1]
# display(thresh)
# Resize picture which is possible to be used
paper = cv2.resize(paper, (width1,height1), cv2.INTER_LANCZOS4)
warped = cv2.resize(warped, (width1,height1), cv2.INTER_LANCZOS4)
thresh = cv2.resize(thresh, (width1,height1), cv2.INTER_LANCZOS4)


# Mean Filter

ChQImg = cv2.blur(thresh, (13,13))
# display(ChQImg)
ChQImg = cv2.threshold(ChQImg, 10,255, cv2.THRESH_BINARY)[1]
cnts = cv2.findContours(ChQImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cnts = cnts[0] if imutils.is_cv2() else cnts[1]
questionCnts = []

Answer = [(0,0)]
for c in cnts :
    (x,y,w,h) = cv2.boundingRect(c)
    questionCnts.append(c)
    if x>10 and x<4400 and y>15:
        M = cv2.moments(c)
        # print(M)
        try :
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        except : 
            cX = 0 
            cY = 0
        cv2.drawContours(paper, c, -1, (0,0,255), 1, lineType=0)
        cv2.circle(paper, (cX,cY), 5, (255,255,255), -1)
        Answer.append((cX,cY))

# print(questionCnts)
# ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}
# correct = 0
# each question has 5 possible answers, to loop over the
# question in batches of 5
# k = 5
# for (q, i) in enumerate(np.arange(0, len(questionCnts), k)):
#     # sort the contours for the current question from
#     # left to right, then initialize the index of the
#     # bubbled answer
cnts = contours.sort_contours(questionCnts)[0]
#     bubbled = None

#     # loop over the sorted contours
# for (j, c) in enumerate(cnts):
#     mask = np.zeros(thresh.shape, dtype="uint8")
#     cv2.drawContours(mask, [c], -1, 255, -1)
#     # display(mask)

#     mask = cv2.bitwise_and(thresh, thresh, mask=mask)
#     total = cv2.countNonZero(mask)
#     # display(mask)
result = {}
for i in range(1,35+1):
    result[i] = ''


def getQuest(moment):
    a,b = moment
    choose = int((a-154)/102)
    quest = int((b-5)/101)
    # print(a,b,quest,choose)
    try :
        # print(result[quest].find(str(choose)))
        if result[quest].find(str(choose)) == -1 :
            result[quest] += str(choose)
    except :
        pass

for (a,b) in Answer :
    getQuest((a,b))
    cv2.circle(paper, (a,b), 5, (0,0,255), -1)


print(result)


# for quest in  range(1,35+1):
#     # ont_size + width 
#     up_y = 100 + 6 + 101*(quest-1)
#     down_y = up_y + 101
#     for choose in range(1,10+1):
#         # x = font_size * 2.5 + width + font_size *1  + font_pad*1
#         left_x = 250 + 6  + 102 * (choose-1) 
#         right_x = left_x + 102
#         cv2.rectangle(paper, (left_x,up_y),(right_x,down_y),(0,0,255),1)





# display(paper)
cv2.imwrite("./result.png", paper, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])  
print("Completed")
# paper.


# Judge the Answer
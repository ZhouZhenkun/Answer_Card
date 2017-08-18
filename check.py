# python 3.5, numpy+mlk,scipy for openCV
# use imutils for four_point_transform
# matplotlib for drawing
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
from imutils.perspective import four_point_transform

width1 = 400
height1 = 600


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
image = cv2.imread('draw.jpg')
# display(image)


# Convert into gray Picture 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Guass Filter
blurred = cv2.GaussianBlur(gray, (3,3), 0)
# Adapt Binary => Bitmap
blurred = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,2)
# Add padding
blurred = cv2.copyMakeBorder(blurred,5,5,5,5,cv2.BORDER_CONSTANT,value=(255,255,255))
# display(blurred)



### Edge Detection
# Print edged
edged = auto_canny(blurred)
cv2.imshow("Edges", edged)
cv2.waitKey(0)
# display(edged)




cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
docCnt = None
# Ensure atleast one outline 
if len(cnts) > 0 :
    # sorted them 
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    # find approximate outline
    for c in cnts :
        # epsilon = 0.1*cv2.arcLength(cnt,True)
        # approx = cv2.approxPolyDP(cnt,epsilon,True)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01*peri, True)
        # if find four, Complete
        if len(approx) == 4 :
            docCnt = approx
            break

# Draw red point on the corner
newimage = image.copy()
for i in docCnt :
    cv2.circle(newimage, (i[0][0],i[0][1]), 5, (0,0,255), -1)

# display(newimage)




# Reshape, four_point_transform
sample = four_point_transform(image, docCnt.reshape(4,2))
paper = four_point_transform(image, docCnt.reshape(4,2))
warped = four_point_transform(gray, docCnt.reshape(4,2))
# warped = four_point_transform(gray, np.array([[0,0],[0,1200],[400,0],[400,1200]]))
print(docCnt.reshape(4,2))
# display(paper)
# display(warped)


### Recognized Multiple Choose
# Resize into standard width & height
# gray to BMP
thresh = cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,53,2)
# thresh = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,53,2)
# Resize picture which is possible to be used
thresh = cv2.resize(thresh, (width1,height1), cv2.INTER_LANCZOS4)
paper = cv2.resize(paper, (width1,height1), cv2.INTER_LANCZOS4)
warped = cv2.resize(warped, (width1,height1), cv2.INTER_LANCZOS4)
# Mean Filter
ChQImg = cv2.blur(thresh, (23,23))
ChQImg = cv2.threshold(ChQImg, 130,225, cv2.THRESH_BINARY)[1]
display(ChQImg)

cnts = cv2.findContours(ChQImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
Answer = [(0,0)]
for c in cnts :
    (x,y,w,h) = cv2.boundingRect(c)
    print(x,y,w,h)
    if (w>=5 and h>=5) and y>15 and y<500:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.drawContours(paper, c, -1, (0,0,255), 5, lineType=0)
        cv2.circle(paper, (cX,cY), 7, (255,255,255), -1)
        Answer.append((cX,cY))

display(sample)
for (a,b) in Answer :
    print(a,b)
    cv2.circle(sample, (a,b), 5, (0,0,255), -1)
display(sample)
# display(cnts)

# Judge the Answer
import cv2
import numpy as np
from file import *
from image_edit import *
from Image_Processing import *
from image_process import *

def corner_harris(window):
    img=get_img()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.01*dst.max()]=[0,0,255]

    cv2.imshow('harris',img)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

def SubPixel(window):

    img=get_img()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # find Harris corners
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.dilate(dst,None)
    ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
    dst = np.uint8(dst)

    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

    # Now draw them
    res = np.hstack((centroids,corners))
    res = np.int0(res)
    img[res[:,1],res[:,0]]=[0,0,255]
    img[res[:,3],res[:,2]] = [0,255,0]
    cv2.imwrite('subpixel.png',img)
    cv2.imshow('SubPixel.png',img)
def findcontour(window):
    img=get_img()
    img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #set a thresh
    thresh = 100
    #get threshold image
    ret,thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
    #find contours
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #create an empty image for contours
    img_contours = np.zeros(img.shape)
    # draw the contours on the empty image
    cv2.drawContours(img_contours, contours, -1, (0,255,0), 3)
    #save image
    cv2.imshow('findcontour',img_contours)
def bounding(window):
    image = get_img()
    original = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    ROI_number = 0
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 2)

    cv2.imshow('image', image)
def trash(window):
    img = get_img()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, 2, 1)
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        length = len(hull)
        if length > 5:
            for i in range(length):
                cv2.line(img, tuple(hull[i][0]), tuple(hull[(i+1)%length][0]), (0,0,255), 2)

    cv2.imshow('Convex Hull', img)
def simple(window):
    src = get_img()
    gray=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    cv2.imshow('Source',src)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow('Threshold',thresh)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_all=cv2.drawContours(image=src,contours=contours,contourIdx=-1,color=(0,255,0),thickness=3)
    cv2.imshow('simple', contour_all)

from tkinter import messagebox
from file import *
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
from cv2 import selectROI,destroyWindow,calcHist

def showsize(window):
    img=get_img()
    print(img.shape)

def gaussian(window):
    img=get_img()
    gaussian = cv2.GaussianBlur(img, (11, 11), 0)
    cv2.imshow('GaussianBlur',gaussian)
def blur(window):
    
    img = img=get_img()
    blur = cv2.blur(img, (5, 5))  # 均值滤波
    cv2.imshow('blur',blur)
    
def twoblur(window):
    img = img=get_img()
    blur = cv2.bilateralFilter(img, 9, 75, 75)  # 双边滤波
    cv2.imshow('twoblur',blur)

def strokeEdge(window,  blurKsize = 7, edgeKsize = 5):
    src=get_img()
    '''

    :param src:          原圖像  BGR彩色空間
    :param blurKsize:    模糊濾波器kernel size    k<3  不進行模糊操作
    :param edgeKsize:    邊緣檢測kernel size
    :return:             dst


    '''
    if blurKsize >= 3:
        ##中值模糊
        blurredSrc = cv2.medianBlur(src, blurKsize)
        #灰階化
        gray = cv2.cvtColor(blurredSrc, cv2.COLOR_BGR2GRAY)
    else:
        #灰階化
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    cv2.imshow('gray',gray)
   ###邊緣檢測
    laplacian = cv2.Laplacian(gray, cv2.CV_8U, gray, ksize= edgeKsize)
    cv2.imshow('laplacian',laplacian)
   ##歸一化   轉換背景
    normalizeInverse = (1.0/255)*(255- gray)
    cv2.imshow('normalizeInverse', normalizeInverse)
   ##分離通道
    channels = cv2.split(src)

    ##計算後的結果與每個通道相乘
    for channel in channels:
        ##這裏是點乘  即對應原素相乘
        channel[:] = channel * normalizeInverse

    cv2.imshow('merge',channels[0])
    
    #return  cv2.merge(channels)

def move(window):
    img = get_img()
    rows,cols,ch = img.shape
    M = np.float32([[1,0,100],[0,1,50]])
    dst = cv2.warpAffine(img,M,(cols,rows))
    show_img(window,dst)

def turn(window):
    img = get_img()
    rows,cols,ch = img.shape

    M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    show_img(window,dst)

def affine_transform(window):
    img = get_img()
    rows,cols,ch = img.shape

    pts1 = np.float32([[50,50],[200,50],[50,200]])
    pts2 = np.float32([[10,100],[200,50],[100,250]])

    M = cv2.getAffineTransform(pts1,pts2)

    dst = cv2.warpAffine(img,M,(cols,rows))

    plt.subplot(121),plt.imshow(img),plt.title('Input')
    plt.subplot(122),plt.imshow(dst),plt.title('Output')
    plt.show()

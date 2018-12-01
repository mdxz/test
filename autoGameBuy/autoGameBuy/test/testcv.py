import cv2

import os
import numpy as np
import copy
import time
from pytesseract import *
import re

def fun():
    originalImagPath = "C:/projects/autoGameBuy/autoGameBuy//pictures/capture_0.png"
    # mm = cv2.imread("C:/projects/autoGameBuy/autoGameBuy//pictures/capture_0.png")
    image = cv2.imread(originalImagPath)
    # 灰度化
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # 二值化
    result = cv2.adaptiveThreshold(grayImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
    # # 去噪声
    # # img = del_noise(result, 6)
    # # img = del_noise(img, 4)
    # # img = del_noise(img, 3)
    # # 加滤波去噪
    # im_temp = cv2.bilateralFilter(src=img, d=15, sigmaColor=130, sigmaSpace=150)
    # im_temp = im_temp[1:-1, 1:-1]
    # im_temp = cv2.copyMakeBorder(im_temp, 83, 83, 13, 13, cv2.BORDER_CONSTANT, value=[255])
    #
    # # cv2.imwrite(gbnImagePath, im_temp)

if __name__ == '__main__':
    fun()
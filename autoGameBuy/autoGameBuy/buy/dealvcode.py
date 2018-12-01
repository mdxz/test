#!/usr/bin/env python
#-*- coding:utf-8 -*-

# -*- coding:utf-8 -*-
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import cv2
import os
import numpy as np
import copy
import time
from pytesseract import *
import re

basePath  = os.path.dirname(os.path.dirname(__file__)) + "//pictures/"

def get_screenshot(driver):
    print("in get_screenshot......................................")
    # 获得截屏
    screenshot = driver.get_screenshot_as_png()
    # 将截屏转换为数字信息
    screenshot = Image.open(BytesIO(screenshot))
    # 返回截屏
    return screenshot

def get_postion(wait):
    """
    获取位置信息：
    :return:
    """
    print("in get_postion......................................")
    # 第一步：找到已经加载的验证码图片
    img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#UpdatePanel1>.login_cap>div>div>img")))
    time.sleep(2)
    # 第二步：返回图片的位置对象
    location = img.location
    print("location = {}".format(location))
    # 第三步：返回图片位置大小对象
    size = img.size
    print("size = {}".format(size))
    # 第四部：获得图片坐标信息，位置信息
    # top, bottom, left, right = int(location['y']), int(location['y'] + size['height']), int(location['x']), int(
    #     location['x'] + size['width'])
    left = location['x']
    top = location['y']
    width = left + size['width']
    hight = top + size['height']
    # 第五步：返回图片的位置信息
    return (left, top, width, hight)

# def get_gesst_img(name):
#     """
#     :param name:
#     :return:
#     """
#     print("开始运行driver......")
#     driver = webdriver.Chrome()
#     url = "https://member.mycard520.com.tw/Login/MyCardMemberLogin.aspx?ReturnUrl=%2fMemberLoginService%2fdefault.aspx%3fAuthCode%3d811B50D65B75491AA442CE42D8DB9FB3&AuthCode=811B50D65B75491AA442CE42D8DB9FB3"
#     wait = WebDriverWait(driver, 20)
#     driver.get(url)
#     driver.maximize_window()
#     print("driver 运行完毕。。。。。")
#
#     # 获取验证码图片第一步是截屏整个屏幕
#     screenshot = get_screenshot(driver)
#     # 获取验证码图片第二不是获取图片的位置信息
#     left, top, width, hight = get_postion(wait)
#     print("left, top, width, hight = {}".format((left, top, width, hight)))
#     # 按照位置信息和整个图片获得想要的图片
#     captcha = screenshot.crop((left, top, width, hight))
#     # 保存图片以便查看图片的正确性
#     captcha.save(name)
#     # 返回图片对象

def get_gesst_img(name,driver,wait):
    """
    :param name:
    :return:
    """
    print("in get_gesst_img......................................")
    # 获取验证码图片第一步是截屏整个屏幕
    screenshot = get_screenshot(driver)
    # 获取验证码图片第二不是获取图片的位置信息
    left, top, width, hight = get_postion(wait)
    print("left, top, width, hight = {}".format((left, top, width, hight)))
    # 按照位置信息和整个图片获得想要的图片
    captcha = screenshot.crop((left, top, width, hight))
    # 保存图片以便查看图片的正确性
    captcha.save(name)
    # 返回图片对象

def getOriginalPic(originalImagPath,driver,wait):
    print("in getOriginalPic......................................")
    #imgpath
    print("fileName = {}".format(originalImagPath))
    get_gesst_img(originalImagPath,driver,wait)

def del_noise(img,number):
    print("in del_noise......................................")
    height = img.shape[0]
    width = img.shape[1]

    img_new = copy.deepcopy(img)
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            point = [[], [], []]
            count = 0
            point[0].append(img[i - 1][j - 1])
            point[0].append(img[i - 1][j])
            point[0].append(img[i - 1][j + 1])
            point[1].append(img[i][j - 1])
            point[1].append(img[i][j])
            point[1].append(img[i][j + 1])
            point[2].append(img[i + 1][j - 1])
            point[2].append(img[i + 1][j])
            point[2].append(img[i + 1][j + 1])
            for k in range(3):
                for z in range(3):
                    if point[k][z] == 0:
                        count += 1
            if count <= number:
                img_new[i, j] = 255
    return img_new

def gray_binary_noise_img(originalImagPath, gbnImagePath):
    """
    该函数实现对于原始图片的灰度，二值化，噪声等处理
    :param originalImagPath: 初始验证码图片路径
    :param gbnImagePath: 经过处理过后图片路径
    :return:
    """
    print("in gray_binary_noise_img......................................")
    print("originalImagPath = {}".format(originalImagPath))
    image = cv2.imread(originalImagPath)
    # 灰度化
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 二值化
    result = cv2.adaptiveThreshold(grayImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
    # 去噪声
    img = del_noise(result, 6)
    img = del_noise(img, 4)
    img = del_noise(img, 3)
    # 加滤波去噪
    im_temp = cv2.bilateralFilter(src=img, d=15, sigmaColor=130, sigmaSpace=150)
    im_temp = im_temp[1:-1, 1:-1]
    im_temp = cv2.copyMakeBorder(im_temp, 83, 83, 13, 13, cv2.BORDER_CONSTANT, value=[255])

    cv2.imwrite(gbnImagePath, im_temp)

def erode_dilate_img(infilePath, erodeImagePath, dilateImagePath):
    """
    该函数实现对于经过灰度二值化已经噪声处理过的图片进行腐蚀和膨胀等处理
    :param infilePath: 输入的图片
    :param erodeImagePath: 腐蚀处理过后的图片
    :param dilateImagePath: 膨胀处理过后的图片
    :return:
    """
    print("in erode_dilate_img......................................")
    img = cv2.imread(infilePath, cv2.IMREAD_UNCHANGED)
    #对于识别的正确率:参数取值比较重要，这里取3合适，对于其他的可以调节
    k = np.ones((3, 3), np.uint8)
    result1 = cv2.erode(img, k, 3)
    result2 = cv2.dilate(img, k, 3)
    cv2.imwrite(erodeImagePath, result1)
    cv2.imwrite(dilateImagePath, result2)

def img_to_str(inflie):
    """
    该函数实现的是将图片中的内容转化成文字状态
    :param inflie:
    :return:
    """
    print("in img_to_str......................................")
    # filePath = basePath + "result1-2.jpg"
    text = image_to_string(inflie)
    print(text)
    return  text

def dealText(text):
    """
    该函数实现对于验证码处理成正确的格式：主要是去掉里面的非数字成分：包括空格，小数点,问号等等
    :param text:待处理的字符
    :return:处理过后的字符串
    """
    print("in dealText......................................")
    text = re.findall(r'(\w*[0-9]+)\w*',text)
    numbers = ""
    if len(text) > 0:
        for number in text:
            numbers = numbers + number
    print(numbers)
    return numbers
def dealVCode(count, driver,wait):
    #这里在获取验证码图片之前，为了满足在解析验证码的时候可能的不正确的情况，需要多次解析验证码，所以，这里在获取验证码之前先刷新验证码
    #刷新验证码:首先找到刷新按钮
    print("in dealVCode......................................")
    driver.maximize_window()
    try:
        pass
        #点击刷新按钮，刷新验证码
        try:
            pass
        except:
            print("点击刷新验证码按钮失败!")
    except:
        print("找寻 刷新验证码 按钮失败")
    print("成功的刷新验证码图片!")
    # 驱动浏览器获得验证码图片，并保存到指定的目录下面
    originalImagPath = basePath + "capture_{}.png".format(count)
    getOriginalPic(originalImagPath,driver,wait)
    #对原始图片进行灰度噪声处理
    gbnImagePath = basePath + "gbn_{}.jpg".format(count)
    gray_binary_noise_img(originalImagPath, gbnImagePath)
    #对图片进行腐蚀膨胀等处理
    erodeImagePath = basePath + "erode_{}.jpg".format(count)
    dilateImagePath = basePath+ "dilate_{}.jpg".format(count)
    erode_dilate_img(gbnImagePath,erodeImagePath, dilateImagePath)
    #将处理过的图片调用image_to_string转换成文本字符
    text = img_to_str(erodeImagePath)
    # img_to_str(dilateImagePath)
    # 处理text：去掉多余的空格，符号，小数点等等，只是保留数字
    numbersText = dealText(text)
    return (numbersText, driver, wait)

if __name__=='__main__':
    #因为识别率不是100%，所以这里需要一个循环处理方式，当经过各种方式处理以后，如果返回的文本不是6位的数字的话，点击更换验证码再处理
    #处理的次数暂时定位5次
    print("开始运行driver......")
    driver = webdriver.Chrome()
    url = "https://member.mycard520.com.tw/Login/MyCardMemberLogin.aspx?ReturnUrl=%2fMemberLoginService%2fdefault.aspx%3fAuthCode%3d811B50D65B75491AA442CE42D8DB9FB3&AuthCode=811B50D65B75491AA442CE42D8DB9FB3"
    wait = WebDriverWait(driver, 20)
    driver.get(url)
    print("driver 运行完毕。。。。。")
    # driver.find_elements_by_link_text()

    (text, driver, wait) = dealVCode(0, driver,wait)
    print("##########################################")
    print(text)


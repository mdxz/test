#!/usr/bin/env python
#-*- coding:utf-8 -*-

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

def inputSafePassword(safecode, driver,wait):
    """
    该函数实现的是：输入安全密码，完成后面的购买操作
    :param safecode: 需要输入的 安全代码
    :param driver: 当前的driver
    :param wait: 当前的wait
    :return: 返回最后是否成功的购买（订单号和统计信息组成的字符串）或是购买失败(inputsafepasswordfail)或是网络问题(inputsafepasswordwrongnet)的状态和当前driver,wait组成的元组
    """
    #设置一个变量来标志输入完全代码的成功状态：初始值设置为网络错误
    inputsafepasswordstatus = "inputsafepasswordwrongnet"
    #这里需要判断输入的验证码是否正确，如果验证码正确的话，会跳转到对应的填支付面的页面，如果不正确的话会任然在验证码的页面，重新获得验证码然后输入
    #这里判断的标准二个取其中的一个 1. 看是否还有验证码对应的标签  2. 看是否有跳转后的 请输入安全代码的标签，这里暂时采用第二种情况
    try:
        #找寻正确跳转页面的 请输入安全代码的标签
        safecodeButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_Label4"
        )))
        # 在能够正确的找到 请输入安全代码的标签后，找到对应的输入框，然后输入第二个密码
        try:
            inputSafecodeButton = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_txtSecCode"
            )))
            # 点击输入框弹出输入键盘
            try:
                ActionChains(driver).move_to_element(inputSafecodeButton).perform()
                ActionChains(driver).click(inputSafecodeButton).perform()
                #操作键盘输入安全代码
                try:
                    for key in safecode:
                        #找到key值对应的键的按钮
                        try:
                            keyButton = wait.until(EC.presence_of_element_located((
                                By.LINK_TEXT, "{}".format(key)
                            )))
                            #找到对应的按键以后，移动鼠标单击
                            try:
                                ActionChains(driver).move_to_element(keyButton).perform()
                                ActionChains(driver).click(keyButton).perform()
                            except:
                                print("移动 鼠标 点击 按键 {} 失败!".format(key))
                                return (inputsafepasswordstatus, driver, wait)
                        except:
                            print("找寻 {} 对应的按键失败".format(key))
                            return (inputsafepasswordstatus, driver, wait)
                    #当完成输入安全代码以后，寻找登录按钮
                    try:
                        safecodeLoginButton = wait.until(EC.presence_of_element_located((
                            By.CSS_SELECTOR, ".normal_btn>#ctl00_ContentPlaceHolder1_btnLogin"
                        )))
                        #点击登录按钮
                        try:
                            ActionChains(driver).move_to_element(safecodeLoginButton).perform()
                            ActionChains(driver).click(safecodeLoginButton).perform()
                            #在操作点击登录按钮没有问题以后会跳转页面
                            #通过 请输入安全代码的标签 来判断是否有 网络问题
                            try:
                                safecodeButton = wait.until(EC.presence_of_element_located((
                                    By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_Label4"
                                )))
                                #如果没有异常的话，则是网络有问题
                                print(" 在safecode 点击登录后，由于网路问题 跳转不成功!")
                                return (inputsafepasswordstatus, driver, wait)
                            except:
                                #如果找不到 请输入安全代码的标签的话，则是说明政工跳转
                                #完成购买: ordernumber={} 统计statistics={}
                                #在成功跳转的页面中查询 订单号标签
                                try:
                                    pass
                                    #找到订单号标签后提取订单号信息
                                    ordernumber = "12345"
                                    #查询统计标签
                                    try:
                                        pass
                                        #找到标签提取统计信息
                                        statistics = "678910"
                                        inputsafepasswordstatus = "完成购买：ordernumber={},统计statistics={}".format(ordernumber,statistics)
                                    except:
                                        print("在最后 跳转的页面中没有找到 统计标签!")
                                        #这种情况出现在购买成功，但是由于网络卡顿等问题，只显示了购买的订单信息的情况，所以这种情况算是成功 ?
                                        inputsafepasswordstatus = "完成购买：ordernumber={},统计statistics=网络卡顿没有取到! ".format(ordernumber)
                                        return (inputsafepasswordstatus, driver, wait)

                                except:
                                    #没有找到订单号标签，说明余额不足,失败
                                    print("在最后 跳转的页面中没有找到 订单号标签!")
                                    inputsafepasswordstatus = "inputsafepasswordfail"
                                    return (inputsafepasswordstatus, driver, wait)
                        except:
                            print("在输入安全代码以后 点击登录按钮 失败!")
                            return (inputsafepasswordstatus, driver, wait)
                    except:
                        print("在输入安全代码以后 寻找登录按钮 失败!")
                        return (inputsafepasswordstatus, driver, wait)
                except:
                    print("操作键盘输入安全代码失败!")
                    return (inputsafepasswordstatus, driver, wait)
            except:
                print("点击 输入 安全代码 框 失败 !")
                return (inputsafepasswordstatus, driver, wait)
        except:
            print("找寻 请输入安全代码的输入框 失败!")
            return (inputsafepasswordstatus, driver, wait)
    except:
        print("找到 请输入安全代码的标签 标签失败")
        return (inputsafepasswordstatus, driver, wait)



def baidu():
    driver = webdriver.Chrome()
    url = "https://www.baidu.com/"
    wait = WebDriverWait(driver, 20)
    driver.get(url)

    #找到新闻标签
    try:
      # buttons = driver.find_elements_by_css_selector("#u1>a:nth-child(1)")[0]
      buttons = driver.find_elements_by_css_selector("#u1")
      # print(buttons.text)
      # print(buttons.text)
      for button in buttons:
          print(button.text)

    except:
        print("找到新闻标签失败!")


if __name__ == '__main__':
    # driver = webdriver.Chrome()
    # url = "https://member.mycard520.com.tw/MemberLoginService/default.aspx?AuthCode=6B3678EBC6FF4DA6B729EFB71F472663"
    # wait = WebDriverWait(driver, 20)
    # driver.get(url)
    # inputSafePassword("sima1988",driver,wait)
    baidu()
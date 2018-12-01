#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
from tools.controltime import (timestampToTime)



# 订单号          产品信息          订单归属者   下订单时间   订单完成时间    订单购买状态         备注信息
# ordernumber     productinfor        buyer       starttime    finishtime     orderstatus          backupinfo
#ordernumber,product,username,orderstatus, backupinfo
def saveBuyProcessStartStatus(ordernumber,productinfor,buyer,orderstatus, backupinfo):
    """
    该函数的作用的是保存订单的初始状态
    :param ordernumber:
    :param productinfor:
    :param buyer:
    :param orderstatus:
    :param backupinfo:
    :return:
    """

    starttime = timestampToTime(time.time())
    finishtime = starttime

    print("初始信息: ordernumber = {}, productinfor = {}, buyer = {}, starttime = {}, finishtime = {},orderstatus={}, backupinfo = {}".format(ordernumber,productinfor,buyer,starttime,finishtime,orderstatus, backupinfo))



def getPamentAccountInfor():
    """
    该函数实现的是从支付账户表中返回所有的支付账户信息，密码信息等
    :return: 返回所有的支付账户信息组成的元组
    """
    accountinfo = (("daniulkb100@163.com","2long1988","sima1988"),)
    return accountinfo

#   订单号          产品信息          订单归属者   下订单时间   订单完成时间    订单购买状态         备注信息
#   ordernumber     productinfor        buyer       starttime    finishtime     orderstatus          backupinfo
def updateOrderDBInfor(ordernumber,orderstatus,backupinfo):
    """
    该函数实现的是更新订单信息
    :return:
    """
    #这里将每次更新的时间由更新函数内部得到
    finishtime = timestampToTime(time.time())
    productinfor = "Battlefield™ 1 革命"
    buyer = "460288492@qq.com"
    starttime = timestampToTime(time.time())
    print(
        "变化后的信息: ordernumber = {}, productinfor = {}, buyer = {}, starttime = {}, finishtime = {}, orderstatus={}, backupinfo = {}".format(
            ordernumber, productinfor, buyer, starttime, finishtime, orderstatus, backupinfo))





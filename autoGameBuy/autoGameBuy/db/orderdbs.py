#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pymysql
import time
from tools.controltime import (timestampToTime)
from conf.config import (MYSQL_LOCAL_HOST,MYSQL_LOCAL_PORT,MYSQL_LOCAL_USER,MYSQL_LOCAL_PASSWD,MYSQL_LOCAL_DB,MYSQL_LOCAL_CHARSET)

class AutoGameBuyDB():
    def __init__(self):
        """
        初始化数据库操作：建立数据库链接，获得数据库游标
        """
        self.conn = pymysql.connect(host=MYSQL_LOCAL_HOST, port=MYSQL_LOCAL_PORT, user=MYSQL_LOCAL_USER,
                                    password=MYSQL_LOCAL_PASSWD, db=MYSQL_LOCAL_DB, charset=MYSQL_LOCAL_CHARSET)
        self.cursor = self.conn.cursor()

    #为了避免重复购买，在某个单号进行购买前，首先查看该单号在 orderinfors 表中的状态
    def orderInfor_checkOrderInfor(self, ordernumber):
        """
        该函数实现的是在orderinfors表中查询某个单号的信息:操作的表是：orderinfors
        :param ordernumber: 需要查询的单号
        :return: 返回的查询信息：若单号已经处在成功购买(成功)或是正在购买中则不再需要购买，若不存在单号或是之前的购买失败，则可以再次购买
        """
        pass


    #保存购买的开始信息
    def orderInfor_saveBuyProcessStartStatus(self,ordernumber, productinfor, buyer, orderstatus, backupinfo):
        """
        该函数的作用的是保存订单的初始状态：操作的表是：orderinfors
        :param ordernumber: 订单号
        :param productinfor: 产品信息
        :param buyer: 订单归属者
        :param orderstatus: 订单购买状态： 失败，完成，进行中!
        :param backupinfo: 订单备注信息： 失败时：指向失败的环节及原因 成功时：保存订单信息和统计信息
        :return:
        """

        starttime = timestampToTime(time.time())
        finishtime = starttime

        flag = 0
        #数据库操作语句
        sql = ""

        print(
            "初始信息: ordernumber = {}, productinfor = {}, buyer = {}, starttime = {}, finishtime = {},orderstatus={}, backupinfo = {}".format(
                ordernumber, productinfor, buyer, starttime, finishtime, orderstatus, backupinfo))


    #更新购买状态操作函数
    def orderInfor_updateOrderDBInfor(self,ordernumber, orderstatus, backupinfo):
        """
        该函数实现在购买过程中不断的更新某个订单的购买状态： 操作的表是：orderinfors
        :param ordernumber: 需要更新状态的订单号
        :param orderstatus: 更新的状态
        :param backupinfo: 更新的备注信息
        :return:
        """
        # 这里将每次更新的时间由更新函数内部得到
        finishtime = timestampToTime(time.time())
        productinfor = "Battlefield™ 1 革命"
        buyer = "460288492@qq.com"
        starttime = timestampToTime(time.time())
        print(
            "变化后的信息: ordernumber = {}, productinfor = {}, buyer = {}, starttime = {}, finishtime = {}, orderstatus={}, backupinfo = {}".format(
                ordernumber, productinfor, buyer, starttime, finishtime, orderstatus, backupinfo))

    #查看所有的订单信息
    def orderInfor_checkAllOrderInfor(self):
        """
        该函数实现的是查看所有的订单信息
        :return: 返回所有的信息
        """
        pass


    def payAccountInfo_insertPaymentAccountInfor(self, account, passowrd, safecode):
        """
        该函数实现的是向支付账户表中插入账户信息
        :param account: 账号
        :param passowrd: 密码
        :param safecode: 安全代码
        :return: 返回的是操作是否成功
        """
        pass

    def payAccountInfo_getPaymentAccountInfor(self):
        """
        该函数实现的是返回所有的可用支付账号信息
        :return: 返回的是支付账号相关信息
        """
        pass

    def payAccountInfo_checkPaymentAccountInfor(self):
        """
        该函数实现查看所有的账户信息
        :return:
        """
        pass

    def payAccountInfo_deletAccount(self,account):
        """
        该函数实现删除某个特定账户信息
        :param account: 账号
        :return: 返回操作结果成功或是失败
        """
        pass


    def pemissonAccountInfo_insertUser(self,username,password):
        """
        添加后台操作账户
        :param username:账号
        :param password: 密码
        :return: 返回操作的状态
        """

    def pemissonAccountInfo_deleteUser(self,username):
        """
        删除特定用户
        :param username: 待删除用户的username
        :return:
        """

    def pemissonAccountInfo_checkUserInfo(self):
        """
        该函数实现的是查看所有的管理账户信息
        :return: 返回所有的管理账户信息
        """

    def isExistImage(self, uid):
        """
        判断某个uid对应的image图片是否存在于数据库中
        :param uid:
        :return:
        """
        outcome = None
        sql = "select imagepath from bilibiliuser where uid = \"%s\";" % (uid)
        bilibiliLogger.info("BilibiDB:isExistImage:sql={sql}".format(sql=sql))
        try:
            self.cursor.execute(sql)
            outcome = self.cursor.fetchall()
            bilibiliLogger.info("BilibiDB:isExistImage:outcome={outcome}".format(outcome=outcome))
        except:
            bilibiliLogger.error("BilibiDB:isExistImage:失败！")
        #注意对于返回结果的处理方式
        if len(outcome) == 0 or outcome[0][0] == None:
            return 0
        else:
            return 1
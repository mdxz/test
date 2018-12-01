#!/usr/bin/env python
#-*- coding:utf-8 -*-


def getOrderStatus(ordernumber):
    """
    该函数实现的是根据订单编号来查询该订单在天猫的店铺的状态，是否已经付款或是其他的状况
    :param ordernumber:天猫订单编号
    :return: 返回参数订单对应的订单状态:分为订单不存在（noorder），存在但是没有付款（ordernopay），付款成功（ordersuccess）三种状态
    """
    product = "battle-1"
    orderstatus= "ordernopay"
    return (orderstatus,product)

def updateOrderStatus(ordernumber, buyStatus):
    """
    该函数实现更新订单状态
    :param ordernumber: 唯一的订单号
    :param buyStatus: 现阶段的状态
    :return:
    """
    pass

def saveBuyProcessStatus(username, ordernumber, product, buyStatus, ordertime):
    """
    该函数实现的是保存订单号对应的状态
    :param username: 账户号
    :param ordernumber: 对应的订单号：唯一
    :param product: 购买的产品信息
    :param status: 该订单号处于购买的那个阶段:分为四种状态：支付前，支付后，购买完成状态：beforepay,afterpay,finish,还有账户余额不足(nomoney)
    :return:
    """
    pass

def checkBuyProcessStatus(ordernumber):
    """
    该函数实现的是查看某个订单的购买状态：查询的是后台数据库
    :param ordernumber: 订单号：唯一
    :return: 返回值分为两大类：没有对应的订单信息和有订单信息的真实状态
    """
    orderStatus = "beforepay"
    return orderStatus
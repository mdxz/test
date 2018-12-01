#!/usr/bin/env python
#-*- coding:utf-8 -*-

#该模块的作用实现时间格式的转换

import time

def timeToTimestamp(weibotime):
    """
    该函数作用：将统一格式的时间转换成该时间的时间戳
    :param weibotime: 传入的时间
    :return:
    """
    timestamp = time.mktime(time.strptime(weibotime, "%Y-%m-%d %H:%M:%S"))
    return timestamp

def timestampToTime(weibotime):
    """
    该函数的作用是：将时间戳转化成文字时间格式
    :param weibotime:
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(weibotime))

if __name__ == '__main__':
    print(timestampToTime(time.time()))
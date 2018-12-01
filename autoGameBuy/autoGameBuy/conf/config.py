#!/usr/bin/env python
#-*- coding:utf-8 -*-

#定义一个时间阈值来标识从用户开始登陆，到第一次反馈用户登录信息的时间间隔,单位为 s
loginfeedback = 60
#定义一个时间阈值：用来标识 从购买开始的到指定时间间隔内给用户发送购买结果,单位为s, 并同时发送一封邮件
buyfeedback = 5*60


#下面是数据包库相关配置
#mysql配置：本地mysql配置
MYSQL_LOCAL_HOST = "127.0.0.1"
MYSQL_LOCAL_PORT = 3306
MYSQL_LOCAL_USER = "root"
MYSQL_LOCAL_PASSWD = ""
#订单管理平台
MYSQL_LOCAL_DB = "OMP"
MYSQL_LOCAL_CHARSET = "utf8"


#!/usr/bin/env python
#-*- coding:utf-8 -*-

###该模块实现建立一个网站对于产品购买过程的控制：起流程逻辑是：

from flask import Flask,session,redirect,url_for,escape
from flask import request
import sqlite3
import time
from buy.autoBuy import (getLogin,inputEmailVcode,buyProcess)
from buy.dealorder import (getOrderStatus,checkBuyProcessStatus)
from db.gamedb import (saveBuyProcessStartStatus)


app = Flask(__name__, static_url_path='')
app.secret_key = '12345'
count= 1

global verifyEmail
#driver,wait始终保存的是当前最新的状态
global driver
global wait
# ########################数据库相关的操作：这个数据库初步决定保存的信息是之前登录成功的用户名和账号信息
# #目的不是为了验证，目的是为了下一次登录的时候操作方便
# #数据库
# DATABASE_URI = "mytest.db"
# #进行请求前的初始化，主要是数据的连接，表的创建等等
# @app.before_first_request  # 第一个视图函数被执行前执行(可以有不止一个这种东西)
# def create_db():
#     # 连接
#     conn = sqlite3.connect(DATABASE_URI)
#     c = conn.cursor()  # 获取光标
#     # 创建表
#     c.execute('''DROP TABLE IF EXISTS user''')  # 本来就存在user表则删除之
#     c.execute('''CREATE TABLE user (name TEXT, password TEXT)''')
#     # 执行SQL语句
#     # 数据格式：用户名,密码
#     # 提交！！！
#     conn.commit()
#     # 关闭
#     conn.close()
#
# #定义账户密码是否正确的判断函数
# #判断某个账户及对应的密码信息是否存在于数据库中
# def judge_if_in(username, password):
#     conn = sqlite3.connect(DATABASE_URI)
#     c = conn.cursor()
#     cursor = c.execute("SELECT name, password from user")
#     for row in cursor:
#         if row[0] == username and row[1] == password:
#             conn.close()
#             return True
#     conn.close()
#     return False
#
# #其实还需要向数据库内添加账号密码的函数
# #向数据库中插入用户，密码等信息
# def insert_password(name, password):
#     conn = sqlite3.connect(DATABASE_URI)
#     c = conn.cursor()
#     c.execute("INSERT INTO user (name, password)VALUES (? ,?)", (name, password))
#     conn.commit()
#     conn.close()
#
# ##########################数据库方面的操作

@app.route("/", methods=['GET','POST'])
def home():
    return '''
            欢迎来到自动购买系统！请输入origin平台的登录账户和密码!
            <form action="/signin" method="post">
            <p>用户名：<input name="username"></p>
            <p>密码：  <input name="password" type="password"></p>
            <p><button type="submit">登陆</button></p>
            </form>
    '''

#当在首页输入账号，密码，订单号以后，跳转的页面处理
@app.route("/signin", methods=['POST'])
def signin():
    global driver
    global wait
    global verifyEmail
    #获得在登录页面传入的参数
    username = request.form['username']
    password = request.form['password']
    # originLoginStatus = "worngnet"
    #这里调用登录origin平台函数登录函数
    returnoriginLoginStatus = getLogin(username,password)
    print("returnoriginLoginStatus={}".format(returnoriginLoginStatus))
    #
    #1： 使用账号和密码判断是否能够登录origin平台：调用接口一共返回4种状态：
    #    状态一： 服务器网络有问题，IP被封或是网络不好 originLoginStatus = "worngnet"
    if  returnoriginLoginStatus[0] == "loginworngnet":
        return '''
            网络异常，请重新登录!
            <a href="http://127.0.0.1:5000/">返回登录页面</a>
        '''
    #    状态二：originLoginStatus = "worngaccount": 账号密码错误或是服务器网络有问题，
    #            返回失败提示重新输入账号密码，订单号信息
    elif returnoriginLoginStatus[0] == "loginworngaccount":
        return '''
            你输入的账户或是密码有误，请重新登录!
            <a href="http://127.0.0.1:5000/">返回登录页面</a>
        '''
    #   状态三： originLoginStatus = "success"： origin平台登录成功，然后跳转到输入订单号的页面
    elif returnoriginLoginStatus[0] == "loginsuccess":
        driver = returnoriginLoginStatus[1]
        wait = returnoriginLoginStatus[2]
        return redirect(url_for('inputordernumber'))
    #   状态四： originLoginStatus = "verification"： 需要填入验证码状态，跳转到输入验证码的页面
    #   originLoginStatus保存的是返回的发送验证码的邮箱
    else:
        verifyEmail = returnoriginLoginStatus[0]
        driver = returnoriginLoginStatus[1]
        wait = returnoriginLoginStatus[2]
        return redirect(url_for('inputverification'))

@app.route("/inputverification",methods=['GET','POST'])
def verification():
    #先在origin平台执行一些列操作到输入验证码步骤
    # verifyEmail = "xxx"
    global verifyEmail
    return '''
         你的账户在origin平台进行了绑定，需要输入验证码，验证码已经发送
         {}邮箱，请检查，然后输入验证码！
        <form action="/dealverification" method="post">
        <p>验证码：<input name="vcode"></p>
        <p><button type="submit">确定</button></p>
        </form>
    '''.format(verifyEmail)

@app.route("/dealverification", methods=['POST'])
def dealverification():
    global driver
    global wait
    vcode = request.form['vcode']
    verifStatusInfor = inputEmailVcode(vcode,driver,wait)
    verifStatus = verifStatusInfor[0]
    #这里调用输入验证码函数
    #调用函数输入验证，返回返回输入后的状态：分为三种状态
    # 状态一： 网络出现问题 verifStatus = "worngnet"
    if verifStatus == "inputemailvcodeworngnet":
        return '''
                购买服务器异常，请重新登录或是联系 xxxx
                <a href="http://127.0.0.1:5000/">返回登录页面</a>
            '''
    # 状态二：验证失败 verifStatus = "veriffail"
    if verifStatus == "inputemailvcodefail":
        #????????这里暂时不确定，当验证码验证失败的时候，是完全重新执行一遍登录验证了还是再另外发送验证码即继续验证。这里暂时当做继续验证
        return '''
            验证失败，请重新验证!
            <a href="http://127.0.0.1:5000/inputverification">再次验证</a>
        '''
    # 状态三：验证成功跳转到正确页面,则是验证成功verifStatus = "verifsuccess"
    # 然后跳转到订单页面输入订单号
    if verifStatus == "inputemailvcodesuccess":
        driver = verifStatusInfor[1]
        wait = verifStatusInfor[2]
        return redirect(url_for('inputordernumber'))

@app.route("/inputordernumber", methods=['POST','GET'])
def inputordernumber():
    return '''
                成功的登录origin平台，请输入订单号！！！！
                <form action="/orderdeal" method="post">
                <p>订单号：<input name="ordernumber"></p>
                <p><button type="submit">确定</button></p>
                </form>
            '''

@app.route("/orderdeal", methods=['POST'])
def orderdeal():
    global driver
    global wait
    ordernumber = request.form['ordernumber']
    #在天猫中查询......
    #返回一个元组，包含订单状态和产品

    orderstates = getOrderStatus(ordernumber)

    #通过订单号在天猫平台上查询该订单号的状态：分为三种
    #状态2： 订单错误，在天猫中查询不到该订单的消息
    if orderstates[0] == "noorder":
        return '''
                    没有查询到订单 {} 信息，请重新输入需要查询的订单号
                    <a href="http://127.0.0.1:5000/inputordernumber">输入订单号</a>
                '''.format(ordernumber)
    #状态3： 该订单信息存在，但是还没有付款，所以不能进行购买操作
    if orderstates[0] == "ordernopay":
        return '''
            订单 {} 付款没有完成，请先进行付款.然后重新输入订单信息
            <a href="http://127.0.0.1:5000/inputordernumber">输入订单号</a>
        '''.format(ordernumber)
    # 状态1： 该订单在天猫中有信息，且已经完成付款，两类操作： 保存订单信息到数据库
    #        对该订单进行自动化购买操作
    if orderstates[0] == "ordersuccess":
        #1. 先将订单相关信息保存到后台数据库中.....
        product = orderstates[1]
        orderstatus =  "购买进行中......"
        backupinfo = "开始购买!"
        try:
            #这里需要添加username,从session中获取
            saveBuyProcessStartStatus(ordernumber,product,username,orderstatus, backupinfo)
        except:
            #当保存信息到数据库中失败的时候,跳转到重新输入订单号页面
            return '''
                后台保存订单号信息失败！请重新输入订单号或是联系xxxx处理!
                <a href="http://127.0.0.1:5000/inputordernumber">返回输入订单号页面</a>
            '''
        #2. 进行自动化购买........
        try:
            #在购买的过程的会涉及到不时的将阶段信息保存到数据库中：
            buyProcess(username, ordernumber, product, driver, wait)
            #显示正在购买中，然后让用户选择继续购买或是查询订单的购买状态
            return '''
                购买正在进行中............
                <a href="http://127.0.0.1:5000/">返回登录页面继续购买</a>
                <a href="http://127.0.0.1:5000/checkorderstatus">查询订单购买状态</a>
            '''
        except:
            pass

@app.route("/checkorderstatus", methods=["GET",'POST'])
def checkOrderStatus():
    return '''
                欢迎来到订单查询系统！请输入需要查询的订单号
                <form action="/getorderstatus" method="post">
                <p>订单号：<input name="ordernumber"></p>
                <p><button type="submit">查询</button></p>
                </form>
        '''

@app.route("/getorderstatus", methods=['POST'])
def getorderstatus():
    ordernumber = request.form['ordernumber']
    orderstatus = checkBuyProcessStatus(ordernumber)
    if orderstatus == "beforepay":
        return '''
                订单 {} 正在orgin平台自动购买中，目前还未完成支付!
                <a href="http://127.0.0.1:5000/">返回登录页面继续购买</a>
                <a href="http://127.0.0.1:5000/checkorderstatus">继续查询订单购买状态</a>
            '''.format(ordernumber)
    elif orderstatus == "afterpay":
        return '''
                订单 {} 正在orgin平台自动购买中，已经完成支付！
                <a href="http://127.0.0.1:5000/">返回登录页面继续购买</a>
                <a href="http://127.0.0.1:5000/checkorderstatus">继续查询订单购买状态</a>
            '''.format(ordernumber)
    elif orderstatus == "finish":
        return '''
                订单 {} 正在orgin平台自动购买中，已经完成支付，成功购买!
                <a href="http://127.0.0.1:5000/">返回登录页面继续购买</a>
                <a href="http://127.0.0.1:5000/checkorderstatus">继续查询订单购买状态</a>
            '''.format(ordernumber)
    elif orderstatus == "nomoney":
        return '''
                订单 {} 购买失败!所有账户资金余额不足，请联系xxx处理!
                <a href="http://127.0.0.1:5000/">返回登录页面继续购买</a>
                <a href="http://127.0.0.1:5000/checkorderstatus">继续查询订单购买状态</a>
            '''.format(ordernumber)
    else:
        return '''
                您所查询的订单 {} 不存在 !
                <a href="http://127.0.0.1:5000/">返回登录页面继续购买</a>
                <a href="http://127.0.0.1:5000/checkorderstatus">继续查询订单购买状态</a>
                '''.format(ordernumber)

if __name__ == '__main__':
    app.run(debug=True)


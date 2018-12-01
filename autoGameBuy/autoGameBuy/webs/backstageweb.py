#!/usr/bin/env python
#-*- coding:utf-8 -*-
#该模块的作用是创建一个简单的后台管理系统，该系统主要完成两个功能:查询所有订单，查询指定订单:订单信息的来源是本地的数据库
#且该数据库和购买网站指向的所创建的数据库是同一个数据库
#较为复杂的页面显示如：https://blog.csdn.net/baidu_36831253/article/details/78229810

from flask import Flask, session, redirect, url_for, escape
from flask import request
import sqlite3
from datetime import timedelta

app = Flask(__name__, static_url_path='')
app.secret_key = "123456"
# app.PERMANENT_SESSION_LIFETIME=timedelta(seconds=20)
DATABASE_URI = "testBackstageWeb.db"

# session.permanent = False

#查询所有订单：分为两种：一种情况：当网路有问题或是直接从天猫接口获取失败的情况下返回数据库中的以往订单信息。 一种情况是直接从天猫接口成功返回的情况
#查询某个订单详情：因为接口的调用需要花钱，所以这里就不缓存所有的已知的订单详情到数据库，所以查询订单详情的时候，每次都直接从天猫的接口信息中获取
#后台管理系统设置风格是：不设置注册界面，被允许登录系统查看信息的权限通过后台更改数据库来添加

def create_db():
    # 连接
    conn = sqlite3.connect(DATABASE_URI)
    c = conn.cursor()  # 获取光标
    # 创建表
    c.execute('''DROP TABLE IF EXISTS user''')  # 本来就存在user表则删除之
    c.execute('''CREATE TABLE user (name TEXT, password TEXT)''')
    # 执行SQL语句
    # 数据格式：用户名,密码
    # 提交！！！
    conn.commit()
    # 关闭
    conn.close()

#定义账户密码是否正确的判断函数
#判断某个账户及对应的密码信息是否存在于数据库中
def judge_if_in(username, password):
    conn = sqlite3.connect(DATABASE_URI)
    c = conn.cursor()
    cursor = c.execute("SELECT name, password from user")
    for row in cursor:
        if row[0] == username and row[1] == password:
            conn.close()
            return True
    conn.close()
    return False

#其实还需要向数据库内添加账号密码的函数
#向数据库中插入用户，密码等信息
def insert_password(name, password):
    conn = sqlite3.connect(DATABASE_URI)
    c = conn.cursor()
    c.execute("INSERT INTO user (name, password)VALUES (? ,?)", (name, password))
    conn.commit()
    conn.close()


@app.route("/", methods=['GET','POST'])
def home():
    if  'username' in session:
        return  '''
            欢迎 {} 登录订单管理平台
            <a href="http://127.0.0.1:5000/orderdeal">订单管理中心</a>
            <a href="http://127.0.0.1:5000/logout">退出登录</a>
        '''.format(session['username'])
    return '''<form action="/signin" method="post">
                  <p>账号：<input name="username"></p>
                  <p>密码：<input name="password" type="password"></p>
                  <p><button type="submit">登陆</button></p>
                  </form>
                '''

#登录界面
@app.route('/signin', methods=['POST'])
def signin():
    if judge_if_in(request.form['username'], request.form['password']):
        session['username'] = request.form['username']
        # return redirect(url_for('home'))
        #在密码账号符合要求的情况下跳转到处理订单的页面
        return redirect(url_for('orderdeal'))
    #如果用户名和密码不对，返回信息
    # return '用户名不存在或者密码不对！'
    return '''
        用户或是密码不正确
        <a href="http://127.0.0.1:5000/">返回登录页面</a>
    '''

#订单处理页面：这个页面完成两件事：1.查询所有的订单信息   2.查询指定订单的详细信息
@app.route('/orderdeal', methods=['GET','POST'])
def orderdeal():
    if 'username' in session:
        return '''
                请选择想要查看订单的类型
                <a href="http://127.0.0.1:5000/allorders">所有订单</a>
                <a href="http://127.0.0.1:5000/singleorder">单个订单详情</a>
                <a href="http://127.0.0.1:5000/">返回登录页面</a>
                <a href="http://127.0.0.1:5000/logout">退出登录</a>
        '''
    return '''
        请先登录
        <a href="http://127.0.0.1:5000/">返回登录页面</a>
    '''

#查单所有订单详情页面
@app.route('/allorders', methods=['GET','POST'])
def allorders():
    #操作数据库返回所有的订单信息,然后返回主页
    if 'username' in session:
        return '''
            这就是所有的订单信息
            <a href="http://127.0.0.1:5000/orderdeal">返回查询订单首页</a>
            <a href="http://127.0.0.1:5000/logout">退出登录</a>
        '''
    return '''
            请先登录
            <a href="http://127.0.0.1:5000/">返回登录页面</a>
        '''
#查看某个订单号指定单个订单详情
@app.route('/singleorder', methods=['GET','POST'])
def singleorder():
    if 'username' in session:
        return '''<form action="/temp" method="post">
                      <p>订单号：<input name="ordername"></p>
                      <p><button type="submit">查询</button></p>
                      <a href="http://127.0.0.1:5000/logout">退出登录</a>
                      </form>
        '''
    return '''
                请先登录
                <a href="http://127.0.0.1:5000/">返回登录页面</a>
            '''

@app.route('/temp', methods=['POST'])
def temp():
    if 'username' in session:
        ordername = request.form['ordername']
        #下面使用获得的订单号来获取订单详情
        return '''
            获得订单详细信息
            <a href="http://127.0.0.1:5000/orderdeal">返回查询订单首页</a>
            <a href="http://127.0.0.1:5000/logout">退出登录</a>
        '''
    return '''
                    请先登录
                    <a href="http://127.0.0.1:5000/">返回登录页面</a>
                '''
@app.route('/logout')
def logout():
    # remove the username from the session if it's there # #
    session.pop('username', None)
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    create_db()
    insert_password('jkj','123456')
    insert_password('python','12345')
    app.run(debug=True)
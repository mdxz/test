#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
# sys.path.append("D:\\anti_software\\autoGameBuy")
sys.path.append("C:\\projects\\autoGameBuy\\autoGameBuy")
import time
import re
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from buy.dealvcode import dealVCode
from db.gamedb import (getPamentAccountInfor,updateOrderDBInfor)
from conf.config import loginfeedback


#这个函数将在网页函数 buyweb.py中调用
def getLogin(username,password):
    """
    该函数实现使用特定的账户和密码登录origin平台
    :param username: 登录的账户信息
    :param password: 登录的密码信息
    :return: 返回登录的状态：成功(loginsuccess)或是失败(loginworngnet)账号密码错误(loginworngaccount)和绑定手机需要验证码的情况(验证码)
    """
    loginstatus = "loginworngnet"
    # 打开网页
    driver = webdriver.Chrome()
    url = "https://www.origin.com/hkg/zh-tw/store/battlefield/battlefield-1"
    wait = WebDriverWait(driver, 5)
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)
    # 找到首页登录按钮
    try:

        time.sleep(1)
        loginButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "origin-cta-primary[btn-text='登入']"
        )))
        try:
            # 使用鼠标点击登录按钮
            ActionChains(driver).move_to_element(to_element=loginButton).perform()
            ActionChains(driver).click(on_element=loginButton).perform()
        except:
            # 找到登录按钮失败的时候，说明网页有问题
            print("点击登录按钮失败！")
            driver.close()
            return (loginstatus, driver, wait)
    except:
        # 说明网页慢或是页面构造变化
        print("找到登录按钮失败！")
        driver.close()
        return (loginstatus, driver, wait)
    time.sleep(3)
    # 获得所有的窗口句柄
    all_hand = driver.window_handles
    # 切换到当前窗口句柄
    driver.switch_to_window(all_hand[-1])
    time.sleep(2)
    # 找到当前敞口的账户输入点
    try:
        accountButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "#email"
        )))
        # 向账户按钮中输入账户信息
        try:
            # account = "460288492@qq.com"
            accountButton.send_keys(username)
        except:
            print("输入账户信息失败！")
            driver.close()
            return (loginstatus, driver, wait)
    except:
        print("找到账户按钮失败")
        driver.close()
        return (loginstatus, driver, wait)
    # 找到密码按钮
    try:
        codeButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "#password"
        )))
        # 输入密码
        try:
            # passWord = "Jkj716122"
            codeButton.send_keys(password)
        except:
            print("输入密码信息失败！")
            driver.close()
            return (loginstatus, driver, wait)
    except:
        print("找到密码按钮失败")
        driver.close()
        return (loginstatus, driver, wait)
    # 在输入账户和密码以后点击登录
    try:
        # 找到登录按钮
        loginButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "#logInBtn"
        )))
        try:
            # 点击登录按钮
            ActionChains(driver).move_to_element(loginButton).perform()
            ActionChains(driver).click(loginButton).perform()
        except:
            print("点击登录按钮登录失败！")
            driver.close()
            return (loginstatus, driver, wait)
    except:
        print("找到登录按钮登录失败！")
        driver.close()
        return (loginstatus, driver, wait)
    # 休息5s等待跳转到登录后的页面
    time.sleep(5)
    # 跳转成功以后再是操作当前windows句柄
    # 获得所有的窗口句柄
    all_hand = driver.window_handles
    # 切换到当前窗口句柄
    driver.switch_to_window(all_hand[-1])
    time.sleep(1)
    # 通过在当前页面查看特定的元素来确定是否成功的登录
    # 如果当前页面还是包含#logInBtn的话，那说明登录失败
    try:
        # 再次找寻是否有登录按钮，如果有的话，说明登录是不成功的
        loginButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "#logInBtn"
        )))
        loginstatus = "loginworngaccount"
        driver.close()
        # 获得所有的窗口句柄
        all_hand = driver.window_handles
        # 切换到当前窗口句柄
        driver.switch_to_window(all_hand[-1])
        driver.close()
        return (loginstatus, driver, wait)
    except:
        #如果没有登录按钮的话就是账号密码正确登录或是需要验证码的情况
        #如果是包含tfa-login-panel-container-style标签的话则是需要验证码等操作，如果没有的话则是账号密码错误
        try:
            #找到含有emial信息的标签
            IDButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".tfa-login-panel-container-style"
            )))
            #从IDButton中提取emial
            emailText = ""
            try:
                emailText = IDButton.text
                print(emailText)
                vemail = re.findall(".*(\d+.*com).*", emailText)[0]
                #接下来是找到发送安全代码按钮并点击
                try:
                    sendButton = wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, "#btnSendCode>span>span"
                    )))
                    #点击安全发送代码按钮
                    try:
                        ActionChains(driver).move_to_element(sendButton).perform()
                        ActionChains(driver).click(sendButton).perform()
                        #点击跳转后看页面是否有 输入你的安全代码 的按钮
                        try:
                            saveButton = wait.until(EC.presence_of_element_located((
                                By.CSS_SELECTOR, ".origin-ux-textbox-label"
                            )))
                            print("成功的跳转到输入验证码页面！！！！！")
                            loginstatus = vemail
                            return (loginstatus, driver, wait)
                        except:
                            loginstatus = "loginworngnet"
                            print("找到输入安全代码按钮失败!")
                            return (loginstatus, driver, wait)
                    except:
                        loginstatus = "loginworngnet"
                        print("点击安全发送代码按钮失败!")
                        return (loginstatus, driver, wait)
                except:
                    loginstatus = "loginworngnet"
                    print("寻找安全发送代码按钮失败!")
                    return (loginstatus, driver, wait)
            except:
                loginstatus = "loginworngnet"
                print("提取email失败!")
                return (loginstatus, driver, wait)
        except:
            print("没有找到判断是否需要验证码的标签！则是代表账号密码正确")
            print("账号和密码是正确的，同时不需要验证码！")
            loginstatus = "loginsuccess"
            return (loginstatus, driver, wait)
#这个函数将在网页函数 buyweb.py中调用
def inputEmailVcode(vcode, driver, wait):
    """
    该函数向指定的窗口句柄输入验证码
    :param vcode:  待输入的验证码
    :param driver: 验证码页面对应的driver
    :param wait: 验证码页面对应的wait
    :return: 返回：操作输入验证码状态：三种：验证码正确成功登录(inputemailvcodesuccess)验证码错误验证失败(inputemailvcodefail)网络错误(inputemailvcodeworngnet)
    """
    inputemailvcodestatus = "inputemailvcodeworngnet"
    #第一步：找到输入email验证码的输入框并完成输入然后点击登录
    try:
        sendButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "#oneTimeCode"
        )))
        #输入验证码
        try:
            sendButton.send_keys(vcode)
            #当输入验证码没有问题的时候，然后找到找到登录按钮，点击登录
            try:
                vLogButton = wait.until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, "#btnSubmit>span"
                )))
                #然后点击登录按钮
                try:
                    ActionChains(driver).move_to_element(vLogButton).perform()
                    ActionChains(driver).click(vLogButton).perform()
                except:
                    print("点击验证码登录按钮失败!")
                    return (inputemailvcodestatus,driver,wait)
            except:
                print("找到验证码登录按钮失败!")
                return (inputemailvcodestatus, driver, wait)
        except:
            print("输入email验证码出现失败!")
            return (inputemailvcodestatus, driver, wait)
    except:
        print("找到输入email验证码的框失败!")
        return (inputemailvcodestatus, driver, wait)

    #第二步： 检测登录是否成功

    # 下面是验证是否登录成功
    # 休息5s等待跳转到登录后的页面
    time.sleep(5)
    # 跳转成功以后再是操作当前windows句柄
    # 获得所有的窗口句柄
    all_hand = driver.window_handles
    # 切换到当前窗口句柄
    driver.switch_to_window(all_hand[-1])
    time.sleep(1)
    try:
        # 再次找寻是否有登录按钮，如果有的话，说明登录是不成功的
        loginButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "#btnSubmit"
        )))
        driver.close()
        # 获得所有的窗口句柄
        all_hand = driver.window_handles
        # 切换到当前窗口句柄
        driver.switch_to_window(all_hand[-1])
        driver.close()
        inputemailvcodestatus = "inputemailvcodefail"
        return (inputemailvcodestatus, driver, wait)
    except:
        # 代表成功的情况
        inputemailvcodestatus = "inputemailvcodesuccess"
        print("输入验证码后，成功的登录!")
        return (inputemailvcodestatus, driver, wait)

def findProduct(product, driver, wait):
    """
    该函数实现的是找到对应产品的对应版本，然后点击购买，跳转到mycard的iframe界面
    :param product: 需要购买的产品
    :param driver:
    :param wait:
    :return: 返回的是否正确的跳转到对应页面的状态标志和当前的driver,wati组成的元组
    """

    #设置一个变量来保存在操作过程中的状态，初始值设置为失败！
    findproductstatus = "findProductfail"

    # 找到搜索框并输入产品
    try:
        time.sleep(1)
        searchButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "origin-global-search>div>form>label>.otkinput.otkinput-filter>input"
        )))
        try:
            productName = "Battlefield™ 1 革命"
            searchButton.send_keys(productName)
            # 经过手动的测试下面的点击是多余的，且是不起作用的，当向框内容输入内容的时候，就会自动的联想内容
            # try:
            #     clickButton = wait.until(EC.presence_of_element_located((
            #     By.CSS_SELECTOR, "origin-global-search>div>form>label>.otkinput.otkinput-filter>otkicon.otkicon-search.otkinput-icon"
            #     )))
            #     clickButton.click()
            # except:
            #     print("操作搜索框的点击动作失败")
        except:
            print("向搜索框了填写搜索内容失败!")
            return (findproductstatus, driver, wait)
    except:
        print("找寻搜索框失败!")
        return (findproductstatus,driver,wait)
    time.sleep(3)
    # 找到需要的产品--step1
    try:
        # 找到商品
        productButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".origin-search-section>ul>li>origin-store-premier-browse-tile>div>otkex-hometile>a"
        )))
        try:
            # 鼠标点击
            ActionChains(driver).move_to_element(to_element=productButton).perform()
            ActionChains(driver).click(on_element=productButton).perform()
        except:
            print("鼠标点击商品信息失败")
            return (findproductstatus, driver, wait)
    except:
        print("操作商品按钮失败---step1")
        return (findproductstatus, driver, wait)
    time.sleep(3)
    # 找到取得按钮并点击-----step 2
    try:
        getButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "ng-transclude>.origin-store-gdp-header-block>origin-store-gdp-primarycta>otkex-dropdown-cta\
                >.otkex-dropdown-cta>div>button"
        )))
        try:
            # 鼠标点击
            ActionChains(driver).move_to_element(to_element=getButton).perform()
            ActionChains(driver).click(on_element=getButton).perform()
        except:
            print("鼠标点击取得按钮失败")
            return (findproductstatus, driver, wait)
    except:
        print("找到取得按钮失败!")
        return (findproductstatus, driver, wait)
    time.sleep(3)
    # 找到立即购买按钮
    try:
        buyNowButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            ".otkex-headerwithcta-ctawrapper>origin-store-osp-interstitial-premier-purchase-cta>.origin-telemetry-cta-buy-osp"
        )))
        try:
            # 鼠标点击立即购买
            ActionChains(driver).move_to_element(to_element=buyNowButton).perform()
            ActionChains(driver).click(on_element=buyNowButton).perform()
        except:
            print("点击立即购买按钮失败!")
            return (findproductstatus, driver, wait)
    except:
        print("找到立即购买按钮失败!")
        return (findproductstatus, driver, wait)
    time.sleep(3)

    # 当上面的所有步骤都正确执行的时候，设置findproductstatus为findsuccess
    findproductstatus = "findProductSuccess"
    return (findproductstatus, driver, wait)

def paymentProcess(ordernumber,username,driver, wait):
    """
    该函数实现当找到想要的产品以后，后面的整个的购买流程的实现，返回的是购买的状态：购买的成功或是失败或是网络问题和
    :param ordernumber: 购买产品的订单号：唯一，用来保存数据库的时候使用
    :param username: 当前进行购买的用户： 用来赋值accout信息
    :param driver: 当前的driver
    :param wait: 当前的wait
    :return:返回的是购买的状态：失败(paymentprocessworngnet),成功返回(订单号和统计信息组成的字符串)如：完成购买: ordernumber={} 统计statistics={}
    """
    #首先是正确的跳转到mycard页面，进行账户选择：这里的账户可以是一个固定的任意账户，也可以使用用户的登录origin平台的账户信息
    account = username
    #调用获取支付账户信息的函数
    paymentAccountInfo = getPamentAccountInfor()
    paymentAccountNumbers = len(paymentAccountInfo)
    #这里需要一个循环。。。。。。
    #设置循环变量 paymentprocessscount = 0
    paymentprocessscount = 0
    #设置购买操作是否成功标志,初始值为网络错误
    paymentprocessstatus = "paymentprocessworngnet"
    #终止循环购买的条件是没有了可用支付账户或是购买成功
    while paymentprocessscount < paymentAccountNumbers and paymentprocessstatus != "paymentprocesssucess":
        #获取支付账户信息，支付密码信息，安全代码信息
        paymentaccount = paymentAccountInfo[paymentprocessscount][0]
        paymentpassword = paymentAccountInfo[paymentprocessscount][1]
        safecode = paymentAccountInfo[paymentprocessscount][2]

        #跳转到mycard页面选择账户信息然后完成账号信息操作：返回成功(chooseemailaccountsuccess)或是其他的失败(以网络问题代替:chooseemailaccountworngnet)
        (chooseemailaccountstatus,driver,wait) = chooseEmailAccount(account,driver,wait)
        if chooseemailaccountstatus == "chooseemailaccountworngnet":
            paymentprocessstatus = "paymentprocessworngnet"
            #更新数据库
            updateOrderDBInfor(ordernumber, "失败", chooseemailaccountstatus)
            #失败是关闭mycard操作页面
            driver.close()
        #当选择账户信息成功的时候，才继续后面的操作
        if chooseemailaccountstatus == "chooseemailaccountsuccess":
            # 更新数据库
            updateOrderDBInfor(ordernumber, "购买进行中......", chooseemailaccountstatus)
            #然后执行跳转到验证码页面或是更换支付账户页面(就是输入安全代码的页面):返回的是跳转成功(turntovcodepageorsafecodepagesucess)或是其他问题(以网络错误代替：turnToVcodePageOrsafecodePageworngnet)
            (turnToVcodePageOrsafecodePagestatus, driver, wait) = turnToVcodePageOrsafecodePage(driver, wait)
            print("turnToVcodePageOrsafecodePage 返回成功...............")
            print("turnToVcodePageOrsafecodePage = {}".format(turnToVcodePageOrsafecodePagestatus))
            if turnToVcodePageOrsafecodePagestatus == "turnToVcodePageOrsafecodePageworngnet":
                paymentprocessstatus = "paymentprocessworngnet"
                # 更新数据库
                updateOrderDBInfor(ordernumber, "失败", turnToVcodePageOrsafecodePagestatus)
                #失败时关闭操作mycard支付的页面
                driver.close()
            #只有在跳转网页成功的情况下，才继续后面的操作
            if turnToVcodePageOrsafecodePagestatus == "turntovcodepageorsafecodepagesucess":
                # 更新数据库
                updateOrderDBInfor(ordernumber, "购买进行中......", turnToVcodePageOrsafecodePagestatus)
                #changeAccount函数实现的(除网络问题以外，始终跳转到验证码页面)：返回的是最后是否跳转到验证码页面，成功(changeaccountsuccess)失败(changeaccountworngnet)
                (changeaccountstatus, driver, wait) = changeAccount(driver,wait)
                print("changeAccount 返回成功...............")
                print("changeaccountstatus = {}".format(changeaccountstatus))
                if changeaccountstatus == "changeaccountworngnet":
                    paymentprocessstatus = "paymentprocessworngnet"
                    # 更新数据库
                    updateOrderDBInfor(ordernumber, "失败", changeaccountstatus)
                    #失败时关闭mycard页面
                    driver.close()
                #只有在确认当前页面在验证码页面的情况下，才进行后面的操作
                if changeaccountstatus == "changeaccountsuccess":
                    # 更新数据库
                    updateOrderDBInfor(ordernumber, "购买进行中......", changeaccountstatus)
                    #在验证码页面输入支付账户信息和密码信息：返回：成功（inputPaymentAccountPasswordsucess）失败（inputPaymentAccountPasswordworngnet）
                    (inputPaymentAccountPasswordStatus, driver, wait) = inputPaymentAccountPassword(paymentaccount,paymentpassword,driver,wait)
                    if inputPaymentAccountPasswordStatus == "inputPaymentAccountPasswordworngnet":
                        paymentprocessstatus = "paymentprocessworngnet"
                        # 更新数据库
                        updateOrderDBInfor(ordernumber, "失败", inputPaymentAccountPasswordStatus)
                        #失败时关闭mycard页面
                        driver.close()
                    if inputPaymentAccountPasswordStatus == "inputPaymentAccountPasswordsucess":
                        # 更新数据库
                        updateOrderDBInfor(ordernumber, "购买进行中......", inputPaymentAccountPasswordStatus)
                        #在输入账户密码以后，处理验证码:返回：失败（dealnumbervcodefail），网络问题(dealnumbervcodeworngnet), 成功（dealnumbervcodesuccess）

                        (dealnumbervcodestatus, driver, wait) = dealNumberVcode(driver,wait)
                        if dealnumbervcodestatus == "dealnumbervcodeworngnet":
                            paymentprocessstatus = "paymentprocessworngnet"
                            # 更新数据库
                            updateOrderDBInfor(ordernumber, "失败", dealnumbervcodestatus)
                            #失败时关闭mycard页面
                            driver.close()
                        #代表着：输入了3次验证码还是失败，重新再来
                        if dealnumbervcodestatus == "dealnumbervcodefail":
                            paymentprocessstatus = "paymentprocessworngnet"
                            # 更新数据库
                            updateOrderDBInfor(ordernumber, "失败", dealnumbervcodestatus)
                            #失败时关闭mycard页面
                            driver.close()
                        #只有在成功的输入验证码情况下，才进行后面的操作
                        if dealnumbervcodestatus == "dealnumbervcodesuccess":
                            # 更新数据库
                            updateOrderDBInfor(ordernumber, "购买进行中......", dealnumbervcodestatus)
                            #处理验证码以后，处理 安全代码：返回：失败(inputsafepasswordfail),网咯问题(inputsafepasswordwrongnet),成功(订单号和统计信息组成的字符串)
                            (inputsafepasswordstatus, driver, wait) = inputSafePassword(safecode, driver, wait)
                            #余额不足等:重新来一次
                            if inputsafepasswordstatus == "inputsafepasswordfail":
                                paymentprocessstatus = "paymentprocessworngnet"
                                #当余额不足的时候需要保存提醒余额不足信息到数据库中
                                #定义提醒字符串变量
                                remindstr = "账户: {} 可能余额不足，请检查, 然后确定是否充值!".format(paymentaccount)
                                # 更新数据库
                                updateOrderDBInfor(ordernumber, "失败", remindstr)
                                #关闭
                                #失败时关闭mycard页面
                                driver.close()
                            #网络问题：重新来一次
                            elif inputsafepasswordstatus == "inputsafepasswordwrongnet":
                                paymentprocessstatus = "paymentprocessworngnet"
                                # 更新数据库
                                updateOrderDBInfor(ordernumber, "失败", inputsafepasswordstatus)
                                #失败时关闭mycard页面
                                driver.close()
                            #成功完成购买操作
                            else:
                                # 更新数据库
                                updateOrderDBInfor(ordernumber, "购买进行中......", inputsafepasswordstatus)
                                paymentprocessstatus = inputsafepasswordstatus
                                #购买完成以后，同样关闭页面
                                driver.close()

        #每循环一次计数 + 1
        paymentprocessscount = paymentprocessscount + 1
        #在开始下一次循环之前切换driver为当前的窗口
        # 获得所有的窗口句柄
        all_hand = driver.window_handles
        # 切换到当前窗口句柄
        driver.switch_to_window(all_hand[-1])

    return (paymentprocessstatus,driver, wait)

def getPaymentAccountInfo():
    """
    该函数实现的是操作数据库获得所有的支付账户信息!
    :return: 返回所有的支付账户信息的元组
    """
    accountinfors = (("jkj","123456","123456"),)
    return  accountinfors

def chooseEmailAccount(account, driver, wait):
    """
    该函数的功能是跳转到mycard界面，然后完成账户的选择，最后跳转到验证码页面
    :param account: 选择的账户
    :param driver:当前的driver
    :param wait:当前的wait
    :return: 返回的内容：操作的状态：成功（chooseemailaccountsuccess）或是网络问题导致的失败(chooseemailaccountworngnet)
    """
    #定义状态变量
    chooseemailaccountstatus = "chooseemailaccountworngnet"

    # 找到革命版本并立即购买
    try:
        revolutionBuyNowButton = wait.until(EC.presence_of_element_located((
            # 注意：.otkbtn.otkbtn-dropdown.otkex-dropdown-wrapper应该指定为第二个
            By.CSS_SELECTOR,
            "thead>tr[ng-if='::showCta']>th:nth-child(3)>div>origin-store-osp-comparison-table-cta>div>otkex-dropdown-cta>div>div>button"
        )))
        try:
            # 点击革命的立即购买按钮
            ActionChains(driver).move_to_element(to_element=revolutionBuyNowButton).perform()
            ActionChains(driver).click(on_element=revolutionBuyNowButton).perform()
        except:
            print("点击革命版本立即购买按钮失败")
            return (chooseemailaccountstatus, driver, wait)
    except:
        print("找到革命版本的立即购买按钮失败!")
        return (chooseemailaccountstatus, driver, wait)
    time.sleep(5)

    #当点击完 革命版本 的立即购买以后，会重新开启一个支付的网页
    # 切换到当前窗口
    # 获得所有的窗口句柄
    all_hand = driver.window_handles
    # 切换到当前窗口句柄
    driver.switch_to_window(all_hand[-1])
    # 切换iframe
    # 1：找到ifrme的节点
    try:
        iframe = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".origin-iframemodal-content>iframe"
        )))
        # 2：切换到ifrme框架
        try:
            driver.switch_to_frame(iframe)
        except:
            print("切换到iframe框架标签失败！")
            return (chooseemailaccountstatus, driver, wait)
    except:
        print("找到iframe框架标签失败！")
        return (chooseemailaccountstatus, driver, wait)

    # 找到mycard按钮并点击
    try:
        mycardButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "li[data-target='MYCARD_MEMBER']>a"
        )))
        # 点击mycard按钮
        try:
            ActionChains(driver).move_to_element(mycardButton).perform()
            ActionChains(driver).click(mycardButton).perform()
        except:
            print("点击mycard按钮失败！")
            return (chooseemailaccountstatus, driver, wait)
    except:
        print("找到mycard按钮失败!")
        return (chooseemailaccountstatus, driver, wait)
    # 这里得有一个判断：如果mycard下面没有之前的账号的情况和有之前的账号的情况和需要再次添加的状况
    # case 1: 该账户不是第一次登陆，且给的账户有记录的情况
    try:
        # 下面使用通过link_text的方式来查找，但是由于本身的原因，查找不成功，所以更换一种方式
        # 第一步：循环判断是否有for=MYCARD_MEMBER_info0的标签
        i = 0
        #emails：保存现在已经添加所有account嘻嘻
        emails = []
        while True:
            labelStr = "MYCARD_MEMBER_info{}".format(i)
            try:
                button = wait.until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, "label[for={}]".format(labelStr)
                )))
                # 在找到该标签后，首先找到email标签然后将该标签对应的email添加到emails中
                try:
                    emailB = wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, "label[for={}]>span".format(labelStr)
                    )))
                except:
                    print("找到 {} 下面的email标签失败".format(labelStr))
                # 将email添加到emails中
                print("emailB.text = {}".format(emailB.text))
                emails.append(emailB.text)
                i = i + 1
            except:
                print("{} 对应的标签不存在".format(labelStr))
                # 然后终止循环
                break
        # 然后看emails中是否有oldemail,如果有着找到标签然后点击，如果没有，则是新增等后面的判断
        try:
            #如果account对应的账号已经被添加，那么返回对应的下标，如果没有被添加，则会包异常，由except来捕捉
            index = emails.index(account)
            # 在得到index的基础上，然后找到对应的标签并选中
            try:
                labelStr = "MYCARD_MEMBER_info{}".format(index)
                emailB = wait.until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, "label[for={}]>span".format(labelStr)
                )))
                try:
                    ActionChains(driver).move_to_element(emailB).perform()
                    ActionChains(driver).click(emailB).perform()
                    # 在点击选中的情况下，选中继续前往
                    # 找到继续前往按钮
                    try:
                        continueButton = wait.until(EC.presence_of_element_located((
                            By.CSS_SELECTOR, ".otkmodal-footer.clearfix>a"
                        )))
                        time.sleep(2)
                        try:
                            # 移动鼠标点击按钮
                            ActionChains(driver).move_to_element(continueButton).perform()
                            ActionChains(driver).click(continueButton).perform()
                        except:
                            print("点击继续前往的按钮失败!")
                            return (chooseemailaccountstatus, driver, wait)
                    except:
                        print("找到继续前往失败!")
                        return (chooseemailaccountstatus, driver, wait)
                except:
                    print("在确认{}存在情况下，移动点击标签失败!".format(account))
                    return (chooseemailaccountstatus, driver, wait)
            except:
                print("在确认{}存在的情况下，找寻对应标签失败".format(account))
                return (chooseemailaccountstatus, driver, wait)
        except:
            print("账号信息: {} 没有添加".format(account))
            # case 2: 该账户不是第一次登陆，但是没有支付账户记录的情况
            # 在没有指定的账户信息的情况下，首先判断是否有新正按钮:通过ID ：MYCARD_MEMBER_newAccountInfo来判断
            try:
                newAccountButton = wait.until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, "label[for='MYCARD_MEMBER_newAccountInfo']"
                )))
                print("找到新添加按钮!")
                # 在有新增按钮的情况下：点击新增，然后输入内容
                try:
                    ActionChains(driver).move_to_element(newAccountButton).perform()
                    ActionChains(driver).click(newAccountButton).perform()
                    # 在没有失败的情况下：填入账户信息等
                    # 1. 找到email 并填入email
                    try:
                        newEmailButton = wait.until(EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            ".edit-card.clearfix.open>.row-1.clearfix>.col-1.clearfix>.otkform-group>.otkform-group-field>label>.otkinput >input"
                        )))
                        # 输入email
                        try:
                            newEmailButton.send_keys(account)
                        except:
                            print("在添加新账户的时候输入email失败!")
                            return (chooseemailaccountstatus, driver, wait)
                    except:
                        print("在新增账户信息的时候没有找到email账户信息")
                        return (chooseemailaccountstatus, driver, wait)
                    # 2. 找到名字并输入名字
                    try:
                        newNameButton = wait.until(EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            ".edit-card.clearfix.open>.row-2.clearfix>.col-1.clearfix>.otkform-group>.otkform-group-field>label>.otkinput>input"
                        )))
                        # 输入名字
                        try:
                            newNameButton.send_keys("no name")
                        except:
                            print("在添加新账户的时候输入name失败!")
                            return (chooseemailaccountstatus, driver, wait)
                    except:
                        print("在新增账户信息的时候没有找到名字信息")
                        return (chooseemailaccountstatus, driver, wait)
                    # 3. 找到姓氏并输入姓氏
                    try:
                        newMiddleButton = wait.until(EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            ".edit-card.clearfix.open>.row-2.clearfix>.col-2.clearfix>.otkform-group>.otkform-group-field>label>.otkinput>input"
                        )))
                        # 输入姓氏
                        try:
                            newMiddleButton.send_keys("no middle name")
                        except:
                            print("新增账户信息的时候输入姓氏失败!")
                            return (chooseemailaccountstatus, driver, wait)
                    except:
                        print("在新增账户信息的时候没有找到姓氏信息")
                        return (chooseemailaccountstatus, driver, wait)
                except:
                    print("点击新增账户按钮失败!")
                    return (chooseemailaccountstatus, driver, wait)
                # 找到继续前往按钮并点击
                try:
                    continueButton = wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, ".otkmodal-footer.clearfix>a"
                    )))
                    time.sleep(2)
                    try:
                        # 移动鼠标点击按钮
                        ActionChains(driver).move_to_element(continueButton).perform()
                        ActionChains(driver).click(continueButton).perform()
                    except:
                        print("点击继续前往的按钮失败!")
                        return (chooseemailaccountstatus, driver, wait)
                except:
                    print("找到继续前往失败!")
                    return (chooseemailaccountstatus, driver, wait)
            except:
                print("这里没有新增账户信息的按钮！")
                # 在没有新增账户信息的情况下，说明该用户是第一次使用，所以按照新的情况处理
                # case 3: 之前重来没有使用过的情况
                # 先是处理没有之前信息的状况
                try:
                    # 找到输入email的框
                    emailButton = wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        "section[data-section='MYCARD_MEMBER']>div>.account-table.no-saved-credit-cards>.edit-card.clearfix>.row-1.clearfix>.col-1.clearfix>.otkform-group>.otkform-group-field>label>.otkinput>input"
                    )))
                    # 输入emial
                    try:
                        email = "460288492@qq.com"
                        emailButton.send_keys(email)
                    except:
                        print("输入email失败！")
                except:
                    print("找到email输入口失败!")
                # 找到输入名字框
                try:
                    nameButton = wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        "section[data-section='MYCARD_MEMBER']>div>.account-table.no-saved-credit-cards>.edit-card.clearfix>.row-2.clearfix>.col-1.clearfix>.otkform-group>.otkform-group-field>label>.otkinput>input"
                    )))
                    try:
                        # 输入名字name
                        name = "little"
                        nameButton.send_keys(name)
                    except:
                        print("输入name失败！")
                except:
                    print("找到名字输入框失败！")
                # 找到姓氏框
                try:
                    middleButton = wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        "section[data-section='MYCARD_MEMBER']>div>.account-table.no-saved-credit-cards>.edit-card.clearfix>.row-2.clearfix>.col-2.clearfix>.otkform-group>.otkform-group-field>label>.otkinput>input"
                    )))
                    # 输入姓氏
                    try:
                        middle = "bawang"
                        middleButton.send_keys(middle)
                    except:
                        print("输入姓氏失败!")
                except:
                    print("找到姓氏框失败!")
                # 找到继续前往按钮
                try:
                    continueButton = wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, ".otkmodal-footer.clearfix>a"
                    )))
                    time.sleep(2)
                    try:
                        # 移动鼠标点击按钮
                        ActionChains(driver).move_to_element(continueButton).perform()
                        ActionChains(driver).click(continueButton).perform()
                    except:
                        print("点击继续前往的按钮失败!")
                        return (chooseemailaccountstatus, driver, wait)
                except:
                    print("找到继续前往失败!")
                    return (chooseemailaccountstatus, driver, wait)
    except:
        print("在操作email账户的过程中出现问题。。。。。")
        return (chooseemailaccountstatus, driver, wait)

    #当所有的上面进行完毕，然后没有被终止掉的话，那么所有的操作都是正确的
    chooseemailaccountstatus = "chooseemailaccountsuccess"
    return (chooseemailaccountstatus,driver,wait)

def turnToVcodePageOrsafecodePage(driver, wait):
    """
    该函数实现的是当选择账户确定以后，点击付费按钮和继续前往按钮，然后跳转到验证码页码或是更换支付账户页面
    :param payaccount: 支付
    :param driver: 传入的driver
    :param wait: 传入的wait
    :return: 返回：是否成功跳转的状态和当前的driver,wait
    """
    #定义一个初始变量 clickpaymentstatus 来保存是否成功的标志，初始值设置为网络错误
    turnToVcodePageOrsafecodePagestatus = "turnToVcodePageOrsafecodePageworngnet"

    # 先登上2s中等一切加载完毕，然后才点击立即付费按钮
    time.sleep(2)
    try:
        paybutton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".otkmodal-footer.clearfix>.otkbtn.otkbtn-primary"
        )))
        # 点击立即付费按钮
        try:
            ActionChains(driver).move_to_element(paybutton).perform()
            ActionChains(driver).click(paybutton).perform()
        except:
            print("点击立即付费按钮失败!")
            return (turnToVcodePageOrsafecodePagestatus,driver,wait)
    except:
        print("找寻立即付费按钮失败!")
        return (turnToVcodePageOrsafecodePagestatus, driver, wait)
    #这里当点击立即付费按钮以后，需要再次点击 继续前往付费服务提供者 的按钮
    #注意下面的这个按钮，初步定为：当首次登陆的时候，是没有这个按钮的，所以这里需要一个判断
    time.sleep(3)
    try:
        keeponButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".otkmodal-footer>.otkbtn.otkbtn-primary"
        )))
        print("找到 继续前往付费服务提供者 按钮 !")
        #点击继续前往付费服务提供者按钮
        try:
            ActionChains(driver).move_to_element(keeponButton).perform()
            ActionChains(driver).click(keeponButton).perform()
        except:
            print("点击 继续前往付费服务提供者 失败!")
            # return (turnToVcodePageOrsafecodePagestatus, driver, wait)
    except:
        print("是没有 继续前往付费服务提供者 的!")
        # return (turnToVcodePageOrsafecodePagestatus, driver, wait)
    time.sleep(10)
    # 获得所有的窗口句柄
    all_hand = driver.window_handles
    # 切换到当前窗口句柄
    driver.switch_to_window(all_hand[-1])
    # time.sleep(1)
    #如果上面的执行没有问题的话，就会跳转到验证码页面或是更换支付账户的页面
    turnToVcodePageOrsafecodePagestatus = "turntovcodepageorsafecodepagesucess"
    return (turnToVcodePageOrsafecodePagestatus, driver, wait)

def inputPaymentAccountPassword(paymentaccount,paymentpassword,driver,wait):
    """
    改函数完成在验证码页面输入支付账户和支付密码的输入
    :param paymentaccount: 支付账户信息
    :param paymentpassword: 支付密码信息
    :param driver: 当前的driver
    :param wait: 当前的密码
    :return: 返回的是操作是否成功状态和当前的driver,wati
    """
    inputPaymentAccountPasswordStatus = "inputPaymentAccountPasswordworngnet"
    # 然后转换到验证码页面
    # 首先在验证码页面找到MyCard會員帳號和MyCard會員密碼的输入框，并输入对应的内容
    # 找到MyCard會員帳號输入框
    try:
        mycardaccountButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".input_area>#TextBox1"
        )))
        #向 MyCard會員帳號输入框 输入内容
        try:
            mycardaccountButton.send_keys(paymentaccount)
        except:
            print("向 MyCard會員帳號输入框 输入内容失败")
            return (inputPaymentAccountPasswordStatus, driver, wait)
    except:
        print("找寻 MyCard會員帳號输入框  失败!")
        return (inputPaymentAccountPasswordStatus, driver, wait)
    #找到 MyCard會員密碼的输入框
    try:
        mycardPasswordButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".input_area>#TextBox2"
        )))
        #向 MyCard會員密碼的输入框 输入密码
        try:
            mycardPasswordButton.send_keys(paymentpassword)
        except:
            print("向 MyCard會員密碼的输入框 输入密码失败!")
            return (inputPaymentAccountPasswordStatus, driver, wait)
    except:
        print("找到 MyCard會員密碼的输入框 失败!")
        return (inputPaymentAccountPasswordStatus, driver, wait)

    #如果上面操作都没有问题的话，则是成功
    inputPaymentAccountPasswordStatus = "inputPaymentAccountPasswordsucess"
    return (inputPaymentAccountPasswordStatus, driver, wait)

def dealNumberVcode(driver,wait):
    """
    该函数完成验证码的处理，包括取得验证码和输入验证码:这里成功的取得解析后的6位数的验证码在失败的情况下最多要经过6次，这里在验证码错误的情况下最多尝试3次
    :param driver:
    :param wait:
    :return: 返回的是操作验证码的状态，成功或是其他问题带来的失败
    """
    #定义一个变量来标志操作验证码的状态
    dealnumbervcodestatus = "dealnumbervcodeworngnet"
    #定义一个变量：inputnumbervcodecount 来限制当验证码错误的时候重试的次数
    inputnumbervcodecount = 0
    inputnumbervcodestatus = "inputnumbervcodefail"
    print("在 dealNumberVcode 函数中  while 循环开始之前..............")
    while inputnumbervcodecount < 3 and inputnumbervcodestatus != "inputnumbervcodesuccess":
        #getNumberVcode函数实现的是获得一个6位数的数字验证码和当前的driver,wait
        (vcode,driver,wait) = getNumberVcode(driver,wait)
        #inputNumberVcode是输入验证码，返回的是输入后的状态：三种： 网络错误inputnumbervcodewrongnet，验证码错误 inputnumbervcodefail， 成功: inputnumbervcodesuccess
        (inputnumbervcodestatus,driver,wait) = inputNumberVcode(vcode,driver,wait)
        inputnumbervcodecount = inputnumbervcodecount + 1
        print("inputnumbervcodestatus = {}, inputnumbervcodecount = {}".format(inputnumbervcodestatus,inputnumbervcodecount))
    #如果在输入验证码的时候，出现网络错误，就直接返回网络错误，不用再进行后面的内容
    if inputnumbervcodestatus == "inputnumbervcodewrongnet":
        return (dealnumbervcodestatus, driver, wait)
    #如果在输入验证码的时候，出现输入验证吗失败，就直接返回失败，不用再进行和面的内容
    if inputnumbervcodestatus == "inputnumbervcodefail":
        dealnumbervcodestatus = "dealnumbervcodefail"
        return (dealnumbervcodestatus, driver, wait)
    if inputnumbervcodestatus == "inputnumbervcodesuccess":
        dealnumbervcodestatus = "dealnumbervcodesuccess"
        return (dealnumbervcodestatus, driver, wait)

def getNumberVcode(driver,wait):
    """
    该函数实现的多次获取数字验证码，并装换成数字，最后返回6为数字的验证码(确保得到6位数的数字验证码)
    :param driver:
    :param wait:
    :return: 6位数字的验证码
    """
    count = 0
    numbercode = ""
    #在不够5次且验证码长度不满足要求的情况下才进行下一次的循环
    print("在 getNumberVcode 中 开始 while 循环之前")
    while count < 5  and len(numbercode) != 6:
        (numbercode,driver,wait) = dealVCode(count,driver,wait)
        print("numbercode = {}, count = {}".format(numbercode,count))
        count = count + 1
    print("numbercode = {}".format(numbercode))
    return (numbercode,driver,wait)

def inputNumberVcode(vcode, driver, wait):
    """
    该函数实现的是输入验证码，然后成功的跳转到 最后输入安全代码的页面
    :param vcode: 需要输入的验证码
    :param driver: 当前的driver
    :param wait: 当前的wait
    :return: 该函数返回的是：输入验证码后的状态和当前的driver,wait组成的元组： 状态包括： 成功，网络问题，失败
    """
    inputNumberVcodeStatus  = "inputnumbervcodesuccess"
    #首先找到输入验证码的框并输入
    try:
        vcodeButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".login_cap>div>div>input[name='CaptchaControl1']"
        )))
        #向输入验证码的框里面输入验证码
        try:
            vcodeButton.send_keys(vcode)
        except:
            print("向框里输入验证码失败!")
            inputNumberVcodeStatus = "inputnumbervcodewrongnet"
            return (inputNumberVcodeStatus, driver, wait)
    except:
        print("找寻  输入验证码的框 失败!")
        inputNumberVcodeStatus = "inputnumbervcodewrongnet"
        return (inputNumberVcodeStatus, driver, wait)

    #当验证码输入完毕以后，点击登录按钮:首先是找到登录按钮
    try:
        vLoginButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "#Button1"
        )))
        #找到按钮后，点击登录
        try:
            ActionChains(driver).move_to_element(vLoginButton).perform()
            ActionChains(driver).click(vLoginButton).perform()
        except:
            print("点击登录按钮失败!")
            inputNumberVcodeStatus = "inputnumbervcodewrongnet"
            return (inputNumberVcodeStatus, driver, wait)
    except:
        print("找到 验证码输入页面的 登录按钮失败")
        inputNumberVcodeStatus = "inputnumbervcodewrongnet"
        return (inputNumberVcodeStatus, driver, wait)

    #当点击登录按钮以后，如果是成功登录的话，则是会成功跳转到输入安全代码的页面，若是不成功的话则在页面可以找到验证码对应的按钮
    #判断的依据是跳转多的页面是否有  你目前登录的账号为 的标签
    try:
        judgeButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_Label1"
        )))
        #如果找到验证码的按钮，则是成功跳转
        #这里使用一个状态标志
        print("找到 你目前登录的账号为 说明成功的跳转到页面!")
        inputNumberVcodeStatus = "inputnumbervcodesuccess"
        return (inputNumberVcodeStatus, driver, wait)
    except:
        print("没有找到 你目前登录的账号为 说明跳转失败!!")
        inputNumberVcodeStatus = "inputnumbervcodefail"
        return (inputNumberVcodeStatus, driver, wait)

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
                print("显示弹出框!")
                time.sleep(10)
                #操作键盘输入安全代码:  只有这里没有测通了.........网络问题****************
                try:
                    # try:
                    #     #这里先测试是否能够找到任意一个
                    #     oneButton = wait.until(EC.presence_of_element_located((
                    #         By.CSS_SELECTOR, "#keypad-div>.keypad-row:nth-child(0)"
                    #     )))
                    #     print("oneButton = {}".format(oneButton))
                    #     try:
                    #         ActionChains(driver).move_to_element(oneButton).perform()
                    #         ActionChains(driver).click(oneButton).perform()
                    #         print("成功点击 oneButton!")
                    #         time.sleep(6)
                    #     except:
                    #         print("点击 oneButton失败")
                    # except:
                    #     print("找到 oneButton 失败 ！")
                    #定义四个列表用来保存获取的数据
                    l1 = []
                    l2 = []
                    l3 = []
                    l4 = []
                    #找寻所有的数字
                    try:
                        #找到第一排数据
                        try:
                            firstRowButton = wait.until(EC.presence_of_element_located((
                            By.CSS_SELECTOR, "#keypad-div>.keypad-row:nth-child(1)"
                            )))
                            #遍历第一排下面的所有标签并保存标签对应的内容
                            for button in firstRowButton:
                                #循环获取标签的数字内容
                                try:
                                    content = button.text
                                    l1.append(content)
                                except:
                                    print("在获取第一排数字内容的过程的中出现问题!")
                        except:
                            print("找第1排数字出错")
                        #找到第二排数据
                        try:
                            secondRowButton = wait.until(EC.presence_of_element_located((
                            By.CSS_SELECTOR, "#keypad-div>.keypad-row:nth-child(2)"
                            )))
                            # 遍历第2排下面的所有标签并保存标签对应的内容
                            for button in secondRowButton:
                                # 循环获取标签的数字内容
                                try:
                                    content = button.text
                                    l2.append(content)
                                except:
                                    print("在获取第二排数字内容的过程的中出现问题!")
                        except:
                            print("找第2排数字出错")
                        #找到第三排数据
                        try:
                            thirdRowButton = wait.until(EC.presence_of_element_located((
                            By.CSS_SELECTOR, "#keypad-div>.keypad-row:nth-child(3)"
                            )))
                            # 遍历第一排下面的所有标签并保存标签对应的内容
                            for button in thirdRowButton:
                                # 循环获取标签的数字内容
                                try:
                                    content = button.text
                                    l2.append(content)
                                except:
                                    print("在获取第三排数字内容的过程的中出现问题!")
                        except:
                            print("找第3排数字出错")
                        #找到第四排数据
                        try:
                            fourthRowButton = wait.until(EC.presence_of_element_located((
                            By.CSS_SELECTOR, "#keypad-div>.keypad-row:nth-child(4)"
                            )))
                            # 遍历第一排下面的所有标签并保存标签对应的内容
                            for button in fourthRowButton:
                                # 循环获取标签的数字内容
                                try:
                                    content = button.text
                                    l4.append(content)
                                except:
                                    print("在获取第四排数字内容的过程的中出现问题!")
                        except:
                            print("找第4排数字出错")
                    except:
                        print("在找寻所有的数字过程中出现问题!")

                    #找到数字以后确定密码的位置
                    #定义一个位置列表变量
                    locations = []
                    for singleword in safecode:
                        #在第一排中查找是否有数字
                        try:
                            lo1 = l1.index(singleword) + 1
                            print("在 第一排 中的 位置 {} 找到 {}".format(lo1,singleword))
                            #如果没有发生异常，这是找到了位置，将位置添加在位置列表中
                            locations.append([singleword, 1,lo1])
                        except:
                            #如果在第一排中没有找到就在第二排中寻找
                            try:
                                lo2 = l2.index(singleword) + 1
                                print("在 第二排 中的 位置 {} 找到 {}".format(lo2, singleword))
                                # 如果没有发生异常，这是找到了位置，将位置添加在位置列表中
                                locations.append([singleword, 2, lo2])
                            except:
                                ##如果在第二排中没有找到就在第三排中寻找
                                try:
                                    lo3 = l3.index(singleword) + 1
                                    print("在 第三排 中的 位置 {} 找到 {}".format(lo3, singleword))
                                    # 如果没有发生异常，这是找到了位置，将位置添加在位置列表中
                                    locations.append([singleword, 3, lo3])
                                except:
                                    ##如果在第三排中没有找到就在第四排中寻找
                                    try:
                                        lo4 = l4.index(singleword) + 1
                                        print("在 第四排 中的 位置 {} 找到 {}".format(lo4, singleword))
                                        # 如果没有发生异常，这是找到了位置，将位置添加在位置列表中
                                        locations.append([singleword, 4, lo4])
                                    except:
                                        print(" 在 1,2,3,4 排中都没有找到数字，找寻数字失败!")
                    #确定了位置以后就开始点击
                    for location in locations:
                        #找到按钮
                        try:
                            cssstr = "#keypad-div>.keypad-row:nth-child({})>.keypad-key:nth-child({})".format(location[2],location[3])
                            print("cssstr = {}".format(cssstr))
                            Button = wait.until(EC.presence_of_element_located((
                                By.CSS_SELECTOR, cssstr
                            )))
                            #找到按钮后，点击按钮
                            try:
                                ActionChains(driver).move_to_element(Button).perform()
                                ActionChains(driver).click(Button).perform()
                            except:
                                print("点击 {} 对应的按钮失败!".format(location[0]))
                        except:
                            print("找寻 {}对应的按钮失败!".format(location[0]))






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

def changeAccount(driver,wait):
    """
    该函数实现的是首先判断是验证码页码或是输入安全代码页面，如果是安全代码页面则是跳转到验证码页面
    :param driver: 当前的driver
    :param wait:  当前的wait
    :return: 返回是否成功跳转到验证码页面的状态标志和当前的driver,wait
    """
    #定义一个状态标志，
    changeaccountstatus = "changeaccountworngnet"
    #首先 找到 是否有刷新 按钮
    try:
        vcodeRefreshButton = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".captcha_refresh"
        )))
        #如果找打刷新按钮设置状态返回
        changeaccountstatus = "changeaccountsuccess"
        return (changeaccountstatus, driver, wait)
    except:
        print("找打 刷新验证码 按钮失败 !")
        #如果没有找到 刷新验证码 按钮，则看是否有 这不是我的账号的标签
        try:
            changeAccountButton = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_btnAgain"
            )))
            #如果找到 更换账号 按钮 则点击，跳转到 验证码页面
            try:
                ActionChains(driver).move_to_element(changeAccountButton).perform()
                ActionChains(driver).click(changeAccountButton).perform()
                #如果点击成功的话，则是重置状态并返回
                print("点击 这不是我的账号的标签 成功，跳转到验证码页面!")
                changeaccountstatus = "changeaccountsuccess"
                return (changeaccountstatus, driver, wait)
            except:
                print("点击 这不是我的账号的标签 失败 !")
                #点击失败说明是网络问题
                return (changeaccountstatus, driver, wait)
        except:
            print("找到 这不是我的账号的标签 失败")
            #不是验证码页面，也不是 安全代码页面 则是网络问题
            return (changeaccountstatus, driver, wait)
#这个函数将在网页函数 buyweb.py中调用
def buyProcess(username, ordernumber, product, driver, wait):
    """
    在校验过各种参数：登录账号，密码，验证码，订单号等过后，开始后面的继续购买
    :param username: 对应的账户名
    :param ordernumber: 订单号
    :param product: 购买的产品
    :param driver: 当前的
    :param wait:
    :return：返回为：购买的状态：成功或是失败
    """
    #定义变量标志购买过程是否成功,初始值设置为失败，定义标量来标志失败的原因
    buyprocessstatus = "buyfail"
    # 首先按照购买的产品输入然后点击，跳转到支付页面
    (findproductstatus, driver, wait) = findProduct(product, driver, wait)
    if findproductstatus == "findProductfail":
        driver.close()
        #当在搜索产品信息的时候，如果失败，更新订单在数据库中的信息
        #updateOrderDBInfor(ordernumber,orderstatus,backupinfo)
        #当在搜索购买产品环节的时候，如果失败了，更新数据库信息，并同时返回购买失败!
        updateOrderDBInfor(ordernumber, "失败", findproductstatus)
        return (buyprocessstatus)
    #只有在正确的找打需要购买的产品的前提下，才开始支付环节:返回失败(paymentprocessworngnet)和成功(paymentprocesssucess)
    if findproductstatus == "findProductSuccess":
        #在正确的找到产品信息的状况下，更新保存状态:
        updateOrderDBInfor(ordernumber,"购买进行中......", findproductstatus)
        #返回：:返回失败(paymentprocessworngnet)和成功（paymentprocesssucess）
        (paymentprocessstatus,driver,wait) = paymentProcess(ordernumber,username,driver,wait)
        if paymentprocessstatus == "paymentprocessworngnet":
            driver.close()
            #更新数据表
            updateOrderDBInfor(ordernumber, "失败", paymentprocessstatus)
            return (buyprocessstatus)
        if paymentprocessstatus == "paymentprocesssucess":
            driver.close()
            updateOrderDBInfor(ordernumber,"成功",paymentprocessstatus)
            buyprocessstatus = "buysuccess"
            return (buyprocessstatus)

if __name__ == '__main__':
    #没有绑定手机的号
    account = "460288492@qq.com"
    passWord = "Jkj716122"
    #绑定了手机需要验证码的号
    # account = "676178367@qq.com"
    # passWord = "Hc123456789"
    #成功(loginsuccess)或是失败(loginworngnet)账号密码错误(loginworngaccount)和绑定手机需要验证码的情况(验证码)
    returnoriginLoginStatus = getLogin(account, passWord)
    if returnoriginLoginStatus[0] == "loginworngnet":
        print("网络错误!")
    elif returnoriginLoginStatus[0] == "loginworngaccount":
        print("账号密码问题!")
    elif returnoriginLoginStatus[0] == "loginsuccess":
        driver = returnoriginLoginStatus[1]
        wait = returnoriginLoginStatus[2]
        product = "Battlefield™ 1 革命"
        buyoutcomes = buyProcess(account,"11111",product,driver,wait)
        print("outcomes = {}".format(buyoutcomes))
    else:
        print("需要验证码")

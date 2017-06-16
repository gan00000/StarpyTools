#-*- coding: UTF-8 -*-

import cookielib
import urllib2

import requests


class Login:

    def __init__(self):
        self.loginPageUrl = ''
        self.loginUrl = ''
        self.postVaule = ''
        self.headers = ''
        self.cookieFileName = ''
        self.session = None
        pass

    def session_login(self,loginPageUrl, loginUrl,postVaule,headers,cookieFileName):

        self.loginPageUrl = loginPageUrl
        self.loginUrl = loginUrl
        self.postVaule = postVaule
        self.headers = headers
        self.cookieFileName = cookieFileName


        # 使用登录cookie信息
        if cookieFileName:
            pass
        else:
            cookieFileName = 'cookies'

        session = requests.session()
        session.cookies = cookielib.LWPCookieJar(filename=cookieFileName)
        try:
            session.cookies.load(ignore_discard=True)
        except:
            print("Cookie 未能加载")

        urllib2.urlopen(loginPageUrl)
        # mainPage = session.get(loginPageUrl)
        # print mainPage.text
        #
        # url = "http://47.89.21.166/master/duoluotaitanGM/index/login"
        # values = {'username': 'tw001',
        #           'password': '123456',
        #           'submitid': '提交'}
        # # product_cookies(session)
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        #     ,
        #     'Cookie': 'PHPSESSID=d7ivboe6vm67a8r0all3mrp5a3',
        #     'Host': '47.89.21.166',
        #     'Referer': 'http://47.89.21.166//master/duoluotaitanGM/index/login/?url=http://47.89.21.166/master/duoluotaitanGM/index'
        # }
        # 不需要验证码直接登录成功

        login_success_page = session.post(loginUrl, data=postVaule, headers=headers)
        session.cookies.save()
        self.session = session

        return login_success_page, session

    def product_cookies(self,msession):
        cookies_str = ''
        for item in msession.cookies:
            print item.name + ':' + item.value
            cookies_str = cookies_str + item.name + ':' + item.value + ';'
        cookies_str = cookies_str[:-1]
        print 'cookies_str-->' + cookies_str
        return cookies_str
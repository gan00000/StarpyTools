# ! /usr/bin/env python
# coding:utf-8

import sys
import re
import urllib2
import urllib
import requests
import cookielib

## 这段代码是用于解决中文报错的问题
reload(sys)
sys.setdefaultencoding("utf8")
#####################################################
# 登录人人
# loginurl = 'http://www.renren.com/PLogin.do'
# logindomain = 'renren.com'


class Login2(object):
    def __init__(self):
        pass
        # self.cj = cookielib.LWPCookieJar()

    # def setLoginInfo(self, username, password):
    #     '''设置用户登录信息'''
    #     self.name = username
    #     self.pwd = password

    def login(self,reqeustUrl,loginparams,headers,cookieFileName):
        '''登录网站'''
        # loginparams = { 'username': self.name, 'password': self.pwd}
        self.cj = cookielib.LWPCookieJar(filename=cookieFileName)
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

        req = urllib2.Request(reqeustUrl, urllib.urlencode(loginparams), headers=headers)
        response = urllib2.urlopen(req)
        self.operate = self.opener.open(req)
        thePage = response.read()
        return thePage,urllib2



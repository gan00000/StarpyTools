#-*- coding: UTF-8 -*-

import time
import datetime

def timestamp_to_strtime(timestamp):
    """将 13 位整数的毫秒时间戳转化成本地普通时间 (字符串格式)
    :param timestamp: 13 位整数的毫秒时间戳 (1456402864242)
    :return: 返回字符串格式 {str}'2016-02-25 20:21:04.242000'
    """
    local_str_time = datetime.datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
    return local_str_time
def timestamp_to_datetime(timestamp):
    """将 13 位整数的毫秒时间戳转化成本地普通时间 (datetime 格式)
    :param timestamp: 13 位整数的毫秒时间戳 (1456402864242)
    :return: 返回 datetime 格式 {datetime}2016-02-25 20:21:04.242000
    """
    local_dt_time = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    return local_dt_time
def datetime_to_strtime(datetime_obj):
    """将 datetime 格式的时间 (含毫秒) 转为字符串格式
    :param datetime_obj: {datetime}2016-02-25 20:21:04.242000
    :return: {str}'2016-02-25 20:21:04.242'
    """
    local_str_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
    return local_str_time


def datetime_to_timestamp(datetime_obj):
    """将本地(local) datetime 格式的时间 (含毫秒) 转为毫秒时间戳
    :param datetime_obj: {datetime}2016-02-25 20:21:04.242000
    :return: 13 位的毫秒时间戳  1456402864242
    """
    local_timestamp = long(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    return local_timestamp


def strtime_to_datetime(timestr):
    """将字符串格式的时间 (含毫秒) 转为 datetiem 格式
    :param timestr: {str}'2016-02-25 20:21:04.242'
    :return: {datetime}2016-02-25 20:21:04.242000
    """
    local_datetime = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
    return local_datetime


def strtime_to_timestamp(local_timestr):
    """将本地时间 (字符串格式，含毫秒) 转为 13 位整数的毫秒时间戳
    :param local_timestr: {str}'2016-02-25 20:21:04.242'
    :return: 1456402864242
    """
    local_datetime = strtime_to_datetime(local_timestr)
    timestamp = datetime_to_timestamp(local_datetime)
    return timestamp


def current_datetime():
    """返回本地当前时间, 包含datetime 格式, 字符串格式, 时间戳格式
    :return: (datetime 格式, 字符串格式, 时间戳格式)
    """
    # 当前时间：datetime 格式
    local_datetime_now = datetime.datetime.now()
    # 当前时间：字符串格式
    local_strtime_now = datetime_to_strtime(local_datetime_now)
    # 当前时间：时间戳格式 13位整数
    local_timestamp_now = datetime_to_timestamp(local_datetime_now)
    return local_datetime_now, local_strtime_now, local_timestamp_now

def current_timestamp():
    local_datetime_now = datetime.datetime.now()
    local_timestamp_now = datetime_to_timestamp(local_datetime_now)
    return local_timestamp_now

def get_current_time():
    # print time.time()
    t = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    return t

def get_current_time2():
    # print time.time()
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return t

def get_tomorrow_time():
    today = datetime.date.today()  # 获得今天的日期
    print today   # 输出今天日期
    tomorrow = today + datetime.timedelta(days=1)  # 用今天日期加上时间差，参数为1天，获得明天的日期
    print tomorrow
    return tomorrow


if __name__ == '__main__':

    time_str = '2016-02-25 20:21:04.242000'
    timestamp1 = strtime_to_timestamp(time_str)
    datetime1 = strtime_to_datetime(time_str)
    time_str2 = datetime_to_strtime(datetime1)
    timestamp2 = datetime_to_timestamp(datetime1)
    datetime3 = timestamp_to_datetime(timestamp2)
    time_str3 = timestamp_to_strtime(timestamp2)
    current_time,local_strtime_now,local_timestamp_now = current_datetime()
    print 'timestamp1: ', timestamp1
    print 'datetime1: ', datetime1
    print 'time_str2: ', time_str2
    print 'timestamp2: ', timestamp2
    print 'datetime3: ', datetime3
    print 'time_str3: ', time_str3
    print 'current_time: ', current_time
    print 'local_strtime_now: ', local_strtime_now
    print 'local_timestamp_now: ', local_timestamp_now

    get_tomorrow_time()
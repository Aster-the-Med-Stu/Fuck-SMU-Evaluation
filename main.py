# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 20:22:22 2019

@author: Aster-the-Med-Stu

Always believe something pawsome is about to happen🐾🐾
"""

import requests, json, re
from datetime import date, datetime, timedelta
# Excel 的习惯
import urllib.parse as encodeurl

session = requests.Session()

cookies = {
    'JSESSIONID': '别忘了填上！！！',
}

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}


def GetEvaluationInfo(cookies, headers, date):

    data = {
        'kkrq': date,
        'page': '1',
        'rows': '60',
        'sort': 'kcmc',
        'order': 'asc'
    }

    response = session.post(
        'http://zhjw.smu.edu.cn/xswjktxx!getDataList.action',
        headers=headers,
        cookies=cookies,
        data=data).json()

    if response.get("total") > 0:
        # 需要剔除已经评教的课程，zt 为 0 即已评教
        # 也是一个我不熟悉的操作
        # 参考： https://stackoverflow.com/questions/31068162/removing-a-dictionary-from-a-list-of-dictionaries-in-python
        for lesson in response.get("rows"):
            zt = {info['zt'] for info in lesson}
    else:
        return None


def GetQuestionInfo(cookies, headers, params):

    # 正常情况下的 params
    # params = (
    #     ('jxhjmc', '%25u5B9E%25u9A8C'),
    #     ('jxhjdm', ['02', '02']),
    #     ('kcmc', '%25u673A%25u80FD%25u5B9E%25u9A8C%25u5B66%25u4E00'),
    #     ('kcdm', '103410'),
    #     ('kcrwdm', '1034625'),
    #     ('dgksdm', '1453774'),
    #     ('xnxqdm', '201802'),
    #     ('teadm', '051022'),
    #     ('teaxm', '%25u66FE%25u5D58'),
    #     ('teabh', '051022'),
    #     ('kcptdm', '14171'),
    # )

    response = session.get('http://zhjw.smu.edu.cn/xswjktxx!pjKt.action',
                           params=params,
                           cookies=cookies)

    return response


def EvaluateTeacher():
    pass


# 用于生成时间序列，参考 https://stackoverflow.com/questions/10688006/generate-a-list-of-datetimes-between-an-interval
def perdelta(start, end, delta):
    curr = start
    while curr <= end:
        # yield 这个用法我不熟悉！！
        yield curr
        curr += delta


if __name__ == '__main__':
    begin_date = date(*map(int,
                           input("请输入自动评教起始日期（格式为 YYYY-MM-DD）：\n").split('-')))
    end_date = date(*map(int, input("请输入结束日期：\n").split('-')))

    for someday in perdelta(begin_date, end_date, timedelta(days=1)):
        evaluation_info_for_someday = GetEvaluationInfo(
            cookies, headers, someday)
        # 判断当天是否没课
        if evaluation_info_for_someday is None:
            break
        else:
            print(evaluation_info_for_someday)

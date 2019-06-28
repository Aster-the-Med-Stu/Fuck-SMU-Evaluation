# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 20:22:22 2019

@author: Aster-the-Med-Stu

Always believe something pawsome is about to happen🐾🐾
"""

import requests, re
from datetime import date, timedelta  #, datetime
# Excel 的习惯
# from urllib.parse import quote as encodeurl
# 貌似用不上嘞

session = requests.Session()
cookies = {
    'JSESSIONID': '别忘了填上！！',
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
        # 以及 [:]，即切片操作
        # 参考： https://www.runoob.com/python/python-lists.html
        # 以及： https://www.cnblogs.com/ifantastic/p/3811145.html
        response_json = response.get("rows")
        # return response_json
        # 这里的写法参考： https://stackoverflow.com/questions/1235618/python-remove-dictionary-from-list
        response_json[:] = [d for d in response_json if d.get('zt') != "0"]
        if response_json == []:
            return None
        else:
            return response_json
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

    question_params = {
        'jxhjmc': params['jxhjmc'],
        'jxhjdm': [params['jxhjdm'], params['jxhjdm']],
        'kcdm': params['kcdm'],
        'kcrwdm': params['kcrwdm'],
        'dgksdm': params['dgksdm'],
        'xnxqdm': params['xnxqdm'],
        'teadm': params['teadm'],
        'teaxm': params['teaxm'],
        'teabh': params['teabh'],
        'kcptdm': params['kcptdm']
    }
    response = session.get('http://zhjw.smu.edu.cn/xswjktxx!pjKt.action',
                           params=question_params,
                           cookies=cookies)

    return response


def ParseEvaluation(HTML):
    # 参考：https://www.cnblogs.com/deerchao/archive/2006/08/24/zhengzhe30fengzhongjiaocheng.html
    regex_wt = re.compile("(?<=wt = JSON\.parse\(')\[(.*?)\]")
    wt = regex_wt.findall(question_HTML)
    regex_wtxm = re.compile("(?<=wtxm = JSON\.parse\(')\[(.*?)\]")
    wtxm = regex_wtxm.findall(HTML)
    regex_wj = re.compile("(?<=wj = JSON\.parse\(')\[(.*?)\]")
    wj = regex_wj.findall(HTML)
    return wt, wj, wtxm


def EvaluateTeacher(result_tuple, evaluation_info):
    pass
    wt, wj, wjxm = result_tuple
    post_data = {
        'wjdm': wj[0]['wjdm'],
        'pjdxlxdm': '1',
        'pjlxdm': '1',
        'kcptdm': evaluation_info['kcptdm'],
        'pjdxbh': evaluation_info['teabh'],
        'pjdxdm': evaluation_info['teadm'],
        'xnxqdm': evaluation_info['xnxqdm'],
        'kcrwdm': evaluation_info['kcrwdm'],
        'dgksdm': evaluation_info['dgksdm'],
        'kcdm': evaluation_info['kcdm'],
        'pjdxmc': evaluation_info['teaxm'],
        'wtpf': '100',
        'yxf': '100',
        'jy': '',
        'wtdms': '149612,156330,156366,156390',
        'xmdmvals': '149613,156331,156367,156391',
        'xmmcs':
        '\u662F,\u975E\u5E38\u540C\u610F,\u975E\u5E38\u540C\u610F,\u975E\u5E38\u540C\u610F',
        'xzfzs': '20.00,24.00,32.00,24.00'
    }
    return post_data


def PostEvaluation(cookies, headers, data):
    #    data = {
    #      'wjdm': '202001',
    #      'pjdxlxdm': '1',
    #      'pjlxdm': '1',
    #      'kcptdm': '001058',
    #      'pjdxbh': '067025',
    #      'pjdxdm': '000000765',
    #      'xnxqdm': '201802',
    #      'kcrwdm': '1034555',
    #      'dgksdm': '1484074',
    #      'kcdm': '000381',
    #      'pjdxmc': '\u5F90\u82B3',
    #      'wtpf': '100',
    #      'yxf': '100',
    #      'jy': '',
    #      'wtdms': '149612,156330,156366,156390',
    #      'xmdmvals': '149613,156331,156367,156391',
    #      'xmmcs': '\u662F,\u975E\u5E38\u540C\u610F,\u975E\u5E38\u540C\u610F,\u975E\u5E38\u540C\u610F',
    #      'xzfzs': '20.00,24.00,32.00,24.00'
    #    }

    response = requests.post('http://zhjw.smu.edu.cn/xswjktxx!savePj.action',
                             headers=headers,
                             cookies=cookies,
                             data=data)
    if response == 1:
        return
    else:
        print("Something is wrong.....")


# 用于生成时间序列，参考 https://stackoverflow.com/questions/10688006/generate-a-list-of-datetimes-between-an-interval
def perdelta(start, end, delta):
    curr = start
    while curr <= end:
        # while curr < end:
        # yield 这个用法我不熟悉！！
        yield curr
        curr += delta


if __name__ == '__main__':
    print('''
          Author: Aster-the-Med-Stu
          如果有任何问题的话，麻烦到 GitHub 开个 issue~
          另外，如果您对某节课真的有意见的话，请提前评教，因为本脚本会自动跳过已经评价过的课程。
          ''')
    #    begin_date = date(*map(int,
    #                           input("请输入自动评教起始日期（格式为 YYYY-MM-DD）：\n").split('-')))
    #    end_date = date(*map(int, input("请输入结束日期：\n").split('-')))

    # 测试用
    begin_date = date(*map(int, "2019-06-27".split('-')))
    end_date = date(*map(int, "2019-06-27".split('-')))

    for someday in perdelta(begin_date, end_date, timedelta(days=1)):
        evaluation_info_for_someday = GetEvaluationInfo(
            cookies, headers, someday)
        # 判断当天是否没课
        if evaluation_info_for_someday is None:
            break
        else:
            for d in evaluation_info_for_someday:
                question_HTML = GetQuestionInfo(cookies, headers, d).text
                PostEvaluation(
                    cookies, headers,
                    EvaluateTeacher(ParseEvaluation(question_HTML), d))

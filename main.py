# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 20:22:22 2019

@author: Aster-the-Med-Stu

Always believe something pawsome is about to happen🐾🐾
"""

import requests, regex, json
from datetime import date, timedelta  #, datetime
from getch import pause
# Excel 的习惯
# from urllib.parse import quote as encodeurl
# 貌似用不上嘞

session = requests.Session()

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
    # PCRE 和 python 包不完全兼容这点坑我好久，这里不该用 fullmatch
    wt = json.loads(
        regex.search(r"(?<=wt = JSON\.parse\(')\[(.*?)\]",
                     question_HTML).group())
    wtxm = json.loads(
        regex.search(r"(?<=wtxm = JSON\.parse\(')\[(.*?)\]", HTML).group())
    wj = json.loads(
        regex.search(r"(?<=wj = \$\.parseJSON\(')\[(.*?)\]", HTML).group())
    return wt, wj, wtxm


def EvaluateTeacher(result_tuple, evaluation_info):
    pass
    wt, wj, wjxm = result_tuple
    #print(type(wj))
    #print(wj)
    
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
    if response.text == "1":
        return
    else:
        print(response.text)
        print(type(response.text))
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
          另外，如果您对某节课真的有意见的话，请提前评教，因为本脚本会自动跳过已经评价过的课程。\n
          ''')
    cookies = {
        'JSESSIONID': input('请输入 JSESSIONID（需要使用浏览器的开发者工具）：\n'),
    }
    begin_date = date(*map(int,
                           input('请输入自动评教起始日期（格式为 YYYY-MM-DD）：\n').split('-')))
    end_date = date(*map(int, input('请输入结束日期：\n').split('-')))

    # 测试用
    # begin_date = date(*map(int, "2019-06-26".split('-')))
    # end_date = date(*map(int, "2019-06-26".split('-')))

    for someday in perdelta(begin_date, end_date, timedelta(days=1)):
        evaluation_info_for_someday = GetEvaluationInfo(
            cookies, headers, someday)
        # 判断当天是否没课
        if evaluation_info_for_someday is None:
            print(someday.strftime('%Y-%m-%d')+'没有需要评教的课程', end='\r')
            continue
        else:
            print('正在对'+someday.strftime('%Y-%m-%d')+'的课程进行评教',end='\r')
            for d in evaluation_info_for_someday:
                question_HTML = GetQuestionInfo(cookies, headers, d).text
                parse_result = ParseEvaluation(question_HTML)
                PostEvaluation(cookies, headers,
                               EvaluateTeacher(parse_result, d))
    print(
        '\n\n如果前面没有报错的话，评教应该已经完成。请不要忘记再到教务系统上看一眼评教是否完成。\n如果本脚本帮助到了您，不妨在 GitHub 上赏个 Star？\n'
    )
    pause('请按任意键退出……')

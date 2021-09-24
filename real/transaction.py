#-*- coding: UTF-8 -*-

import urllib
import datetime
import urllib.request
import urllib.parse



DAY_PRICE_COLS = ['date', 'open', 'high', 'close', 'low', 'volume', 'chg', '%chg', 'ma5', 'ma10', 'ma20', 'vma5', 'vma10', 'vma20', 'turnover']
DAY_PRICE_URL = '%sapi.finance.%s/%s/?code=%s&type=last'
INDEX_KEY = ['SH', 'SZ', 'HS300', 'SZ50', 'GEB', 'SMEB']
INDEX_LIST = {'SH': 'sh000001', 'SZ': 'sz399001', 'HS300': 'sz399300', 'SZ50': 'sh000016', 'GEB': 'sz399006', 'SMEB': 'sz399005'}
INDEX_DAY_PRICE_COLS= ['date', 'open', 'high', 'close', 'low', 'volume','chg', '%chg', 'ma5', 'ma10', 'ma20','vma5', 'vma10', 'vma20']
K_TYPE_KEY = ['D', 'W', 'M']
K_TYPE_MIN_KEY = ['5', '15', '30', '60']
K_TYPE = {'D': 'akdaily', 'W': 'akweekly', 'M': 'akmonthly'}
MIN_PRICE_URL = '%sapi.finance.%s/akmin?scode=%s&type=%s'
PAGE_TYPE = {'http': 'http://', 'ftp': 'ftp://'}
PAGE_DOMAIN = {'sina': 'sina.com.cn', 'ifeng': 'ifeng.com'}
URL_ERROR_MSG = '获取失败，请检查网络状态，或者API端口URL已经不匹配！'



import pandas as pd
import json
from urllib import request
ktype='D'
code='sz000538'

url = DAY_PRICE_URL % (PAGE_TYPE['http'], PAGE_DOMAIN['ifeng'], K_TYPE[ktype], code)

#url = 'http://hq.sinajs.cn/list=%s' %(code)

try:
    text = request.urlopen(url,timeout=10).read()
    if len(text) < 15:
        raise IOError('no data!')
except Exception as e:
    print(e)

df_dict = json.loads(text)
df = pd.DataFrame(df_dict['record'])
df.columns = DAY_PRICE_COLS

print(df)



# def download_stock_data(stock_list):
#     for sid in stock_list:
#         url = 'http://table.finance.yahoo.com/table.csv?s=' + sid
#
#         # 侦测股票是否存在
#         s = urllib.request.urlopen(url)
#         code = s.getcode()
#         if code != 200:
#    print("The %s 's record does not exist!" % (sid))
#    continue
#
#         fname = sid + '.csv'
#         print('downloading %s from %s' % (fname, url))
#         urllib.request.urlretrieve(url, fname)
#
#
# def download_stock_data_period(stock_list,start,end):
# #s为股票id
#     for sid in stock_list:
#         params = {'a': start.month - 1, 'b': start.day, 'c': start.year,
#      'd': end.month - 1, 'e': end.day, 'f': end.year, 's': sid}
#         url = 'http://table.finance.yahoo.com/table.csv?'
#         qs = urllib.parse.urlencode(params)
#         url = url + qs
#
# # 侦测股票是否存在
#         s = urllib.request.urlopen(url)
#         code = s.getcode()
#         if code != 200:
#    print ("The %s's record does not exist!" %(sid))
#    continue
#
#         fname = '%s_%d%d%d_%d%d%d.csv' % (sid,start.year,start.month,start.day,end.year,end.month,end.day)
#         print('downloading %s from %s' % (fname, url))
#         urllib.request.urlretrieve(url, fname)
#
#
# if __name__ == '__main__':
#     stock_list =  ["000538.sz"]
#     end = datetime.date(year=2021,month=9,day=22)
#     start = datetime.date(year=2021,month=9,day=23)
#     download_stock_data_period(stock_list,start,end)
#     download_stock_data(stock_list)
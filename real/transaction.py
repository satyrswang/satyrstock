#-*- coding: UTF-8 -*-

import urllib
import datetime
import urllib.request
import urllib.parse

import pandas_datareader.data as web
df_stockload = web.DataReader("000538.SZ", "yahoo", datetime.datetime(2021, 9, 1), datetime.datetime(2021, 9, 23))
print(df_stockload)


df = ts.get_tick_data('600797',date='2019-08-08',src='tt')
print(df.head(10))

# def download_stock_data(stock_list):
#     for sid in stock_list:
#         url = 'http://table.finance.yahoo.com/table.csv?s=' + sid
#
#         # 侦测股票是否存在
#         s = urllib.request.urlopen(url)
#         code = s.getcode()
#         if code != 200:
#             print("The %s 's record does not exist!" % (sid))
#             continue
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
#                   'd': end.month - 1, 'e': end.day, 'f': end.year, 's': sid}
#         url = 'http://table.finance.yahoo.com/table.csv?'
#         qs = urllib.parse.urlencode(params)
#         url = url + qs
#
# # 侦测股票是否存在
#         s = urllib.request.urlopen(url)
#         code = s.getcode()
#         if code != 200:
#             print ("The %s's record does not exist!" %(sid))
#             continue
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
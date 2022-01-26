import datetime
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np
import baostock as bs
import pandas as pd
import os
import pandas as pd
import json
from urllib import request

from utils.log_in import login_bs, bs_exit

DAY_PRICE_COLS = ['date', 'open', 'high', 'close', 'low', 'volume', 'chg', '%chg', 'ma5', 'ma10', 'ma20',
                  'vma5', 'vma10', 'vma20', 'turnover']
DAY_PRICE_URL = '%sapi.finance.%s/%s/?code=%s&type=last'
INDEX_KEY = ['SH', 'SZ', 'HS300', 'SZ50', 'GEB', 'SMEB']
INDEX_LIST = {'SH': 'sh000001', 'SZ': 'sz399001', 'HS300': 'sz399300', 'SZ50': 'sh000016', 'GEB': 'sz399006',
              'SMEB': 'sz399005'}
INDEX_DAY_PRICE_COLS = ['date', 'open', 'high', 'close', 'low', 'volume', 'chg', '%chg', 'ma5', 'ma10', 'ma20',
                        'vma5', 'vma10', 'vma20']
K_TYPE_KEY = ['D', 'W', 'M']
K_TYPE_MIN_KEY = ['5', '15', '30', '60']
K_TYPE = {'D': 'akdaily', 'W': 'akweekly', 'M': 'akmonthly'}
MIN_PRICE_URL = '%sapi.finance.%s/akmin?scode=%s&type=%s'
PAGE_TYPE = {'http': 'http://', 'ftp': 'ftp://'}
PAGE_DOMAIN = {'sina': 'sina.com.cn', 'ifeng': 'ifeng.com'}
URL_ERROR_MSG = '获取失败，请检查网络状态，或者API端口URL已经不匹配！'



class History(object):

    def __init__(self, code='000538.SZ', s_date='2020-09-22', e_date='2021-09-21', path='./000538'):
        self.code = code
        self.s_date = s_date
        self.e_date = e_date
        self.path = path

        self.df = None
        self.dir = './' + str(code)
        if  not os.path.exists(self.dir):
            os.mkdir(self.dir)


    def get_daily_df(self):
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        login_bs()
        rs = bs.query_history_k_data_plus(self.code,
                                          "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                          start_date=self.s_date, end_date=self.e_date,
                                          frequency="d", adjustflag="3")
        print('query_history_k_data_plus respond error_code:' + rs.error_code)
        print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        df = pd.DataFrame(data_list, columns=rs.fields)

        df.index = pd.to_datetime(df['date'])
        df.index.name = 'Date'
        df = df.drop("date", axis=1)

        for i in ["open", "high", "low", "close", "preclose", "amount"]:
            df[i] = df[i].apply(lambda x: float(x))

        for i in ["volume"]:
            df[i] = df[i].apply(lambda x: int(x))

        path = './' + str(self.code) + '_d'
        df.to_csv(self.dir + '/' + path, index=True)

        self.df = df
        bs_exit()


    def plot_daily_df(self):

        mpf.plot(self.df, type='candle', mav=(5, 20, 30, 60), volume=True, title=str(self.code))  # 绘制K线走势
        mpf.show()

    def get_daily_df_2(self):


        ktype = 'D'

        code_num = self.code.split(".")[0]
        code = 'sz' + str(code_num)


        url = DAY_PRICE_URL % (PAGE_TYPE['http'], PAGE_DOMAIN['ifeng'], K_TYPE[ktype], code)

        # url = 'http://hq.sinajs.cn/list=%s' %(code)

        try:
            text = request.urlopen(url, timeout=10).read()
            if len(text) < 15:
                raise IOError('no data!')
        except Exception as e:
            print(e)

        df_dict = json.loads(text)
        df = pd.DataFrame(df_dict['record'])
        df.columns = DAY_PRICE_COLS

        path = './' + str(self.code) + '_d2'
        df.to_csv(self.dir + '/' + path, index=False)
        print(df)


    def get_minute_df(self, minu=30):
        login_bs()
        path = './' + str(self.code) + '_' + str(minu) + 'min'

        #title = "Kline-30min-" + str(self.code)

        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg

        rs = bs.query_history_k_data_plus(self.code,
                                          "date,time,code,open,high,low,close,volume,amount,adjustflag",
                                          start_date=self.s_date, end_date=self.e_date,
                                          frequency=str(minu), adjustflag="2")
        print('query_history_k_data_plus respond error_code:' + rs.error_code)
        print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        df = pd.DataFrame(data_list, columns=rs.fields)

        for i in ["open", "high", "low", "close", "amount"]:
            df[i] = df[i].apply(lambda x: round(float(x), 2))

        for i in ["volume"]:
            df[i] = df[i].apply(lambda x: int(x))

        print(df)

        df.to_csv(self.dir + '/' + path, index=False)

        bs_exit()


# import pandas_datareader.data as web
# df_stockload = web.DataReader("600797.SS", "yahoo", datetime.datetime(2018, 1, 1), datetime.datetime(2019, 1, 1))
# print(df_stockload.head(5))


if __name__ == '__main__':
    d = History()
    d.get_daily_df()
    #d.get_minute_df(30)

    d.get_daily_df_2()
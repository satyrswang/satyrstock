"""
获得分笔数据
"""

import tushare as ts
import numpy as np
import pandas as pd
import datetime
import time
import datetime
import csv
import os
from utils.pandas_print import pandas_pretty_printing
from utils.log_in import login_tushare



class transac(object):

    def __init__(self):

        self.ts,self.pro = login_tushare()


    def get_stock_fbData(self,code, start, end, fb_file):
        # 获取2021-03-01到2021-03-31所有股票的分笔数据
        # 格式：code=get_stock_code返回的值  start='2021-03-01'  end='2021-03-31' fb_file='stock_fb.csv' 字符类型

        # 1. 创建文件对象
        f = open(fb_file, 'w', encoding='utf-8')
        # 2. 基于文件对象构建 csv写入对象
        writer = csv.writer(f)
        # 3. 构建列表头
        writer.writerow(['', 'date', 'time', 'price', 'change', 'volume', 'amount', 'type', 'code'])
        f.close()

        len_code = len(code)
        # 直接把日期字符串拆分转换成    年 / 月 / 日  对应的整数
        begin = datetime.date(*map(int, start.split('-')))  # str 转为 datetime.date
        end = datetime.date(*map(int, end.split('-')))
        delta = datetime.timedelta(days=1)
        df = pd.read_csv(fb_file)
        len_df = len(df)
        for j in range(0, len_code):
            d = begin  # 日期
            while d <= end:
                da = d.strftime("%Y-%m-%d")
                zb = ts.get_tick_data(code.zfill(6), date=str(da), src='tt')  # 旧版tushare的接口获取分笔数据， zfill(6):高位填充0位6位数
                zb = np.array(zb)
                if zb.all() is not None:  # 该股票改日有分笔数据
                    len_zb = len(zb)
                    date = np.array([str(da)] * len_zb)  # 日期
                    c = np.array([str(code).zfill(6)] * len_zb)  # 股票代码
                    zb = np.c_[date, zb[:, 0:], c]
                    df2 = []
                    for i in range(0, len_zb):
                        df2.append(i + len_df)
                    len_df += len_zb
                    df2 = np.array(df2)
                    zb = np.c_[df2, zb]  # 格式化

                    if os.path.isfile(fb_file):  # 写入
                        with open(fb_file, 'a', encoding='utf-8') as f:
                            writer = csv.writer(f, lineterminator='\n')
                            writer.writerows(zb)
                d += delta
        print('get_stock_fbData ok')

        print(df)


if __name__ == '__main__':

    tc = transac()

    tc.get_stock_fbData('000538','2021-09-21','2021-09-27','ynby.csv')

    # df = ts.get_tick_data('000538', date='2021-09-22')
    # print(df)
    # 当日历史分
    df = ts.get_today_ticks('000538')
    print(df)
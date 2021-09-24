"""
:param
"""
# =======
import itchat

code = '000538'
thre_price_high = 98
thre_price_low = 91
thre_chg = 0.01
thre_chg_ng =  -0.01

# =======


import tushare as ts

token = "a4dc47e4087e6b65380021711192e5abdf5ca4783d8840690435ddec"
ts.set_token(token)
pro = ts.pro_api()

from io import StringIO
from tabulate import tabulate
from subprocess import call
import numpy as np
import pandas as pd
import tushare as ts
import datetime
import time
import datetime
import csv
import os

itchat.auto_login(hotReload=True)


def get_stock_code(date, basic_file):
    # date:截取1992-01-01前上市的股票
    # 如 date='1992-01-01'  basic_file='stock_code.csv'
    code = pd.read_csv(basic_file, index_col='list_date', parse_dates=['list_date'])
    code = code[:date]  # 截取date前上市的股票
    print('get_stock_code ok')
    return code


def get_stock_fbData(code, start, end, fb_file):
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


def get_stock_basicData(basic_file):
    # 获取股票基本信息,存储到CSV文件
    # basic_file:股票基本信息的文件名（含后缀）
    # basic_file='stock_code.csv'
    # list_status='L' L：股票状态为上市
    stock_code = pro.stock_basic(exchange='', list_status='L',
                                 fields='ts_code,symbol,name,area,industry,list_date')  # 新版tushare的接口
    stock_code.to_csv(basic_file)
    print('get_stock_basicData ok')


# get_stock_fbData('000538','2021-03-01','2021-03-07','ynby.csv') #perfect
#
# df = ts.get_tick_data('000538', date='2021-09-22')
# print(df)
# # 当日历史分
# df = ts.get_today_ticks('000538')
# print(df)
# 实时分笔

def float_format(x):
    if abs(x) >= 1e10 or 0 < abs(x) < 1e-3:
        return "%e" % x
    else:
        return "%.4f" % x


def pandas_pretty_printing():
    pd.set_option('display.max_rows', None)  # 解决行显示不全
    pd.set_option('display.max_columns', None)  # 解决列显示不全
    pd.set_option('max_colwidth', 1000)  # 解决列宽不够
    pd.set_option('display.width', 1000)  # 解决列过早换行
    pd.set_option('display.float_format', float_format)  # 解决浮点数总是科学计数法


curtime = time.strftime("%Y-%m-%d", time.localtime())
pandas_pretty_printing()


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


"""

    DataFrame 实时交易数据
          属性:0：name，股票名字
        1：open，今日开盘价
        2：pre_close，昨日收盘价
        3：price，当前价格
        4：high，今日最高价
        5：low，今日最低价
        6：bid，竞买价，即“买一”报价
        7：ask，竞卖价，即“卖一”报价
        8：volumn，成交量 maybe you need do volumn/100
        9：amount，成交金额（元 CNY）
        10：b1_v，委买一（笔数 bid volume）
        11：b1_p，委买一（价格 bid price）
        12：b2_v，“买二”
        13：b2_p，“买二”
        14：b3_v，“买三”
        15：b3_p，“买三”
        16：b4_v，“买四”
        17：b4_p，“买四”
        18：b5_v，“买五”
        19：b5_p，“买五”
        20：a1_v，委卖一（笔数 ask volume）
        21：a1_p，委卖一（价格 ask price）
        ...
        30：date，日期；
        31：time，时间；
"""

while True:
    time.sleep(1)
    try:
        df = ts.get_realtime_quotes(code)
        now_price = df.iloc[0, 3]
        close_p = df.iloc[0, 2]
        open_p = df.iloc[0, 1]
        now_chg = round(float((float(now_price) - float(close_p)) / float(open_p)), 3)

        df['chg'] = now_chg

        dfp = df[["time","chg","price","bid","ask",   "volume","amount","open","pre_close","high",  "low",
                  "b1_v","b1_p","b2_v","b2_p","b3_v","b3_p","b4_v","b4_p","b5_v","b5_p",
                  "a1_v","a1_p","a2_v","a2_p","a3_v","a3_p","a4_v","a4_p","a5_v","a5_p","date","name"]]

        dfp.to_csv("./" + str(curtime) + '_' + str(code) + '.csv', header=False, mode="a+", index=False)

        # 对于某个阈值进行提醒
        if float(now_price) >= float(thre_price_high) or float(now_price) <= float(thre_price_low) or float(now_chg) >= float(thre_chg) or float(now_chg) <= float(thre_chg_ng):
            print("==========NOTIFY==========")
            content = str(code) + " HIT " + str(now_price) +' chg ' + str(now_chg)
            cmd = 'display notification \"' + \
                  "Notificaton memo" + '\" with title \"' + str(content) + '\"'
            call(["osascript", "-e", cmd])

            # 发wechat
            # 发送给指定联系人
            itchat.send(content, toUserName='filehelper')


        # print(tabulate(dfp, headers='keys', tablefmt='psql',showindex=False))
        # 时间到3点01分则抛出exception
        donett = time.strftime("%H%M%S", time.localtime())
        if int(donett) > 150050:
            raise Exception("TIME REACHED")


    except Exception as e:
        print("DONE")
        # 开始处理csv，将同样的行删除，time按照秒还是会有重复的

        break

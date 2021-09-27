import itchat
import tushare as ts
from io import StringIO
from tabulate import tabulate
from subprocess import call
import numpy as np
import pandas as pd
import datetime
import time
import datetime
import csv
import os
from utils.pandas_print import pandas_pretty_printing
from utils.log_in import login_tushare


class RT(object):
    def __init__(self,code = '000538',thre_price_high = 103,thre_price_low = 100,thre_chg = 0.03,thre_chg_ng =  -0.01,auto=True):

        self.code = code
        self.thre_price_high = thre_price_high
        self.thre_price_low = thre_price_low
        self.thre_chg = thre_chg
        self.thre_chg_ng =  thre_chg_ng

        self.auto = auto

        login_tushare()
        pandas_pretty_printing()


    def distinct(self,file):

        tmp = pd.read_csv(file)
        tmp.drop_duplicates(inplace=True,ignore_index=True)
        tmp.to_csv('./tmp.csv',index=False)

        os.system("cp -rf ./tmp.csv " + file)
        os.system("rm -rf ./tmp.csv")




    def start_recording(self):
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

        dir = './' + str(self.code)+'_real'
        if not os.path.exists(dir):
            os.mkdir(dir)

        if not self.auto:
            itchat.auto_login(hotReload=True)

        curtime = time.strftime("%Y-%m-%d", time.localtime())

        print(f"MY STOCK PROGRAM PIDP:{os.getpid()}")
        filename = dir+"/" + str(curtime) + '_' + str(self.code) + '.csv'

        while True:
            time.sleep(1)
            try:

                # 时间到3点01分则抛出exception
                donett = time.strftime("%H%M%S", time.localtime())

                if int(donett) > 113001 and int(donett) < 125050:
                    time.sleep(600)
                    print(donett)
                    continue
                else:

                    df = ts.get_realtime_quotes(self.code)
                    now_price = df.iloc[0, 3]
                    close_p = df.iloc[0, 2]
                    open_p = df.iloc[0, 1]
                    now_chg = round(float((float(now_price) - float(close_p)) / float(open_p)), 3)

                    df['chg'] = now_chg

                    dfp = df[
                        ["time", "chg", "price", "bid", "ask", "volume", "amount", "open", "pre_close", "high", "low",
                         "b1_v", "b1_p", "b2_v", "b2_p", "b3_v", "b3_p", "b4_v", "b4_p", "b5_v", "b5_p",
                         "a1_v", "a1_p", "a2_v", "a2_p", "a3_v", "a3_p", "a4_v", "a4_p", "a5_v", "a5_p", "date",
                         "name"]]

                    dfp.to_csv(filename, header=False, mode="a+", index=False)

                    # 对于某个阈值进行提醒
                    if float(now_price) >= float(self.thre_price_high) or float(now_price) <= float(self.thre_price_low) \
                            or float(now_chg) >= float(self.thre_chg) or float(now_chg) <= float(self.thre_chg_ng):
                        print("==========NOTIFY==========")
                        content = str(self.code) + " HIT " + str(now_price) + ' chg ' + str(now_chg)
                        cmd = 'display notification \"' + \
                              "Notificaton memo" + '\" with title \"' + str(content) + '\"'
                        call(["osascript", "-e", cmd])

                        # 发wechat
                        # 发送给指定联系人
                        if not self.auto:
                            itchat.send(content, toUserName='filehelper')

                    print(tabulate(dfp, headers='keys', tablefmt='psql', showindex=False))

                    if int(donett) > 150150:
                        raise Exception("TIME REACHED")



            except Exception as e:
                print("DONE")
                # 开始处理csv，将同样的行删除，time按照秒还是会有重复的

                self.distinct(filename)


                break




if __name__ == '__main__':
    rt = RT()
    rt.start_recording()
    #rt.distinct('000538.SZ/2021-09-27_000538.csv')


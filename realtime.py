import itchat
import tushare as ts
from io import StringIO
from tabulate import tabulate
from subprocess import call
import  easyquotation
import numpy as np
import pandas as pd
import datetime
import time
import datetime
import csv
import os
from utils.pandas_print import pandas_pretty_printing
from utils.log_in import login_tushare
import  sys
import logging

logname = '/Users/wyq/PycharmProjects/stock/000538_real/out_'+str(time.strftime("%Y-%m-%d", time.localtime()))+'.log'
# f_handler=open(logname, 'a+')
# sys.stdout=f_handler
logging.basicConfig(format='%(asctime)s %(message)s', filename=logname)
logging.getLogger().setLevel(logging.INFO)

class RT(object):
    def __init__(self, code='000538', thre_price_high=101, thre_price_low=98, thre_chg=0.03, thre_chg_ng=-0.02,
                 auto=True, prefix='/Users/wyq/PycharmProjects/stock/'):

        self.code = code
        self.thre_price_high = thre_price_high
        self.thre_price_low = thre_price_low
        self.thre_chg = thre_chg
        self.thre_chg_ng = thre_chg_ng
        self.dir_prefix = prefix

        self.auto = auto

        login_tushare()
        pandas_pretty_printing()

    def distinct(self, file):

        tmp = pd.read_csv(file,low_memory=False)
        tmp.drop_duplicates(inplace=True, ignore_index=True)
        tmp.to_csv('./tmp.csv', index=False)

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

        dir = self.dir_prefix + str(self.code) + '_real'
        if not os.path.exists(dir):
            os.mkdir(dir)

        if not self.auto:
            itchat.auto_login(hotReload=True)

        curtime = time.strftime("%Y-%m-%d", time.localtime())

        logging.info(f"MY STOCK PROGRAM PIDP:{os.getpid()}")
        filename = dir + "/" + str(curtime) + '_' + str(self.code) + '.csv'
        logging.info(f"SavedFileName:{filename}")

        while True:
            time.sleep(0.5)
            try:

                # 时间到3点01分则抛出exception
                donett = time.strftime("%H%M%S", time.localtime())

                if int(donett) > 113110 and int(donett) < 125050:
                    time.sleep(600)
                    logging.info(donett)
                    continue
                else:

                    #df = ts.get_realtime_quotes(self.code)
                    df = easyquotation.use("sina").stocks(self.code)
                    tmp = df[self.code]
                    for k in tmp:
                        tmp[k] = [tmp[k]]
                    df = pd.DataFrame.from_dict(tmp)

                    now_price = df.iloc[0, 3]
                    close_p = df.iloc[0, 2]
                    open_p = df.iloc[0, 1]

                    now_chg = round(float((float(now_price) - float(close_p)) / float(open_p)), 5)

                    df['chg'] = now_chg

                    # dfp = df[
                    #     ["time", "chg", "price", "bid", "ask", "volume", "amount", "open", "pre_close", "high", "low",
                    #      "b1_v", "b1_p", "b2_v", "b2_p", "b3_v", "b3_p", "b4_v", "b4_p", "b5_v", "b5_p",
                    #      "a1_v", "a1_p", "a2_v", "a2_p", "a3_v", "a3_p", "a4_v", "a4_p", "a5_v", "a5_p", "date",
                    #      "name"]]

                    dfp = df[
                        ["time", "chg",  "volume", "open", "high", "low",
                         "bid1_volume", "bid1", "bid2_volume", "bid2", "bid3_volume", "bid3", "bid4_volume", "bid4", "bid5_volume", "bid5",
                         "ask1_volume", "ask1", "ask2_volume", "ask2", "ask3_volume", "ask3", "ask4_volume", "ask4", "ask5_volume", "ask5", "date",
                         "name"]]


                    dfp.to_csv(filename, header=False, mode="a+", index=False)

                    # 对于某个阈值进行提醒
                    if float(now_price) >= float(self.thre_price_high) or float(now_price) <= float(self.thre_price_low) \
                            or float(now_chg) >= float(self.thre_chg) or float(now_chg) <= float(self.thre_chg_ng):
                        logging.info("==========NOTIFY==========")
                        content = str(self.code) + " HIT " + str(now_price) + ' chg ' + str(now_chg)
                        cmd = 'display notification \"' + \
                              "Notificaton memo" + '\" with title \"' + str(content) + '\"'
                        call(["osascript", "-e", cmd])

                        # 发wechat
                        # 发送给指定联系人
                        if not self.auto:
                            itchat.send(content, toUserName='filehelper')

                    logging.info(tabulate(dfp, headers='keys', tablefmt='psql', showindex=False))

                    if int(donett) > 150150:
                        logging.info(f"TIME:{donett}")
                        raise Exception("TIME REACHED")

            except Exception as e:
                logging.info("DONE")
                # 开始处理csv，将同样的行删除，time按照秒还是会有重复的
                donett = time.strftime("%H%M%S", time.localtime())
                if int(donett) > 150150:
                    self.distinct(filename)
                    break
                else:
                    logging.info(f"Exception:{e}")
                    continue


if __name__ == '__main__':
    thre_price_high = 101
    thre_price_low = 92
    thre_chg = 0.03
    thre_chg_ng = -0.02

    rt = RT(thre_price_high=thre_price_high,thre_price_low=thre_price_low,thre_chg=thre_chg,thre_chg_ng=thre_chg_ng)
    rt.start_recording()
    # rt.distinct('000538.SZ/2021-09-27_000538.csv')

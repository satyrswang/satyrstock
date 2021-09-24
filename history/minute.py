import datetime
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np
import baostock as bs
import pandas as pd
from snapshot_selenium import snapshot

import talib
from pyecharts.charts import Line, Kline, Candlestick
from pyecharts.render import make_snapshot
from typing import List, Sequence, Union

from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Kline, Line, Bar, Grid


if __name__ == "__main__":
    code = '000538.SZ'
    s_date = '2020-09-22'
    e_date = '2021-01-01'
    title = "Kline-30min-"+str(code)

    lg = bs.login()
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    rs = bs.query_history_k_data_plus(code,
                                      "date,time,code,open,high,low,close,volume,amount,adjustflag",
                                      start_date=s_date, end_date=e_date,
                                      frequency="30", adjustflag="2")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    df = pd.DataFrame(data_list, columns=rs.fields)

    bs.logout()
    # df['time'] = df['time'].apply(lambda x: x[:12])
    # df.index = pd.to_datetime(df['time'])
    # df.index.name = 'time'
    # df = df.drop("date", axis=1)
    # df = df.drop("time", axis=1)

    for i in ["open", "high", "low", "close", "amount"]:
        df[i] = df[i].apply(lambda x: round(float(x),2))

    for i in ["volume"]:
        df[i] = df[i].apply(lambda x: int(x))

    print(df)
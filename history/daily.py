import datetime
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np
import baostock as bs
import pandas as pd

# import pandas_datareader.data as web
# df_stockload = web.DataReader("600797.SS", "yahoo", datetime.datetime(2018, 1, 1), datetime.datetime(2019, 1, 1))
# print(df_stockload.head(5))


code = '000538.SZ'
s_date = '2020-09-22'
e_date = '2021-09-21'

lg = bs.login()
print('login respond error_code:' + lg.error_code)
print('login respond  error_msg:' + lg.error_msg)

# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
# 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
rs = bs.query_history_k_data_plus(code,
                                  "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                  start_date=s_date, end_date=e_date,
                                  frequency="d", adjustflag="3")
print('query_history_k_data_plus respond error_code:' + rs.error_code)
print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
df = pd.DataFrame(data_list, columns=rs.fields)

bs.logout()

df.index = pd.to_datetime(df['date'])
df.index.name = 'Date'
df = df.drop("date",axis=1)

for i in ["open","high","low","close","preclose","amount"]:
    df[i] = df[i].apply(lambda x:float(x))

for i in ["volume"]:
    df[i] = df[i].apply(lambda x:int(x))

mpf.plot(df,type='candle',mav=(5,20,30,60),volume=True,show_nontrading=True) # 绘制K线走势

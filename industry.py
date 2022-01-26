import concurrent.futures
import multiprocessing
from multiprocessing import Queue
import time
import baostock as bs
import pandas as pd
from utils.log_in import login_bs, bs_exit, login_tushare
import os
import tushare as ts


def get_all_codes_num(path='./code_num.csv'):
    login_bs()
    rs = bs.query_stock_industry()
    print('query_stock_industry error_code:' + rs.error_code)
    print('query_stock_industry respond  error_msg:' + rs.error_msg)
    industry_list = []
    while (rs.error_code == '0') & rs.next():
        industry_list.append(rs.get_row_data())
    result = pd.DataFrame(industry_list, columns=rs.fields)
    result.to_csv(path, index=False)
    print(result.head(5))
    code_l = list(result.code)
    bs_exit()
    return code_l


def get_all_codes_basic(code_l, s_d, e_d, freq='m', path='./all_code_basic.csv'):
    login_bs()

    # 保存所有的代码基本信息,start_y和end_y的年线信息
    c = 0
    allbasic = []
    for i in code_l:
        #     i = i.split('.')[1]
        #     pre = i.split('.')[0]
        #     if pre == "sh":
        #         i = i+'.SH'
        #     elif pre == "sz":
        #         i = i+'.SZ'
        c = c + 1
        print(f"{str(c)}:{i} ALL:{str(len(code_l))}")
        df = bs.query_history_k_data_plus(i, "date,code,open,high,low,close,pctChg",
                                          start_date=s_d, end_date=e_d,
                                          frequency=freq, adjustflag="2")
        tmp = []
        while (df.error_code == '0') & df.next():
            tmp.append(df.get_row_data())

        if len(tmp) > 0:
            allbasic.append(tmp)
        elif len(tmp) == 0:
            print(f"NO DATA:{i}", file=open('./退市.txt', 'a'))

    allbasic_fn = []
    for v in allbasic:
        for t in v:
            allbasic_fn.append(t)

    basic_df = pd.DataFrame(allbasic_fn)
    basic_df.columns = ["date", "code", "open", "high", "low", "close", "pctChg"]

    basic_df.to_csv(path, index=False)
    bs_exit()

    return basic_df

def get_profit_data(c,start_y,end_y,cols):
    alldata = []
    for y in range(start_y, end_y):
        for q in [1, 2, 3, 4]:
            print(f"STOCK :{c} , {y, q}")
            rs_profit = bs.query_profit_data(code=c, year=y, quarter=q)
            alldata.append(rs_profit.get_row_data())

    data = pd.DataFrame(alldata, columns=cols)
    data.to_csv('./' + c + '.csv', index=False,mode='a+')

    return c+"_DONE"

@DeprecationWarning
def get_all_codes_profit_multi(code_l, start_y=2005, end_y=2021, path='/Users/wyq/PycharmProjects/stock/15y_profit.csv'):
    # if not os.path.exists(profit_prefix):
    #     os.mkdir(profit_prefix)
    print(f"MY STOCK PROGRAM PIDP:{os.getpid()}")
    login_bs()

    cols = ["code", "pubDate", "statDate", "roeAvg", "npMargin", "gpMargin", "netProfit", "epsTTM", "MBRevenue",
            "totalShare", "liqaShare"]

    pool = multiprocessing.Pool(5)
    result = []
    for c in code_l:
        result.append(pool.apply_async(func=get_profit_data, args=(c,2005,2021,cols,)))

    pool.close()
    pool.join()

    for res in result:
        print(res.get())
    bs_exit()
    print('ALL END')


def profit_vs_chg(mon_path, mon_cols, profit_path, profit_cols):
    # 期间内月开盘和结束

    mon = pd.read_csv(mon_path, columns=mon_cols)
    mong = mon.groupby("code")

    profit = pd.read_csv(profit_path, columns=profit_cols)
    profit_g = profit.groupby("code")

#最早只有2007年的数据。。。
@DeprecationWarning
def get_all_codes_profit1( code_l, start_y = 2005 , end_y = 2021 ,path = './15y_profit.csv'):

    login_bs()

    cols = ["code", "pubDate", "statDate", "roeAvg", "npMargin", "gpMargin", "netProfit", "epsTTM", "MBRevenue",
            "totalShare", "liqaShare"]



    count = 0

    for c in code_l:
        count = count +1
        alldata = []
        for q in [1, 2, 3, 4]:
            for y in range(start_y, end_y):
                print(f"STOCK NO.{str(count)}:{c} , {y,q}")
                profit_list = []
                rs_profit = bs.query_profit_data(code=c, year=y, quarter=q)
                while (rs_profit.error_code == '0') & rs_profit.next():
                    profit_list.append(rs_profit.get_row_data())
                print(profit_list)
                if len(profit_list) == 1:
                    profit_list = profit_list[0]
                    alldata.append(profit_list)
                elif len(profit_list) > 1:
                    print(profit_list,file=open('./格式错误.txt','a'))

        if len(alldata)==0:
            continue

        profit_df = pd.DataFrame(alldata)
        profit_df.columns = cols

        profit_df.to_csv('/Users/wyq/PycharmProjects/stock/profit_data/' +  str(c) +'.csv',index=False)

    bs_exit()

def get_all_codes_profit(start_y = 2005 , end_y = 2021):

    for y in range(start_y,end_y+1):
        print(f"YEAR:{y}")
        for p in [1,2,3,4]:
            profit = ts.get_profit_data(y, p)
            profit.to_csv('/Users/wyq/PycharmProjects/stock/profit_data/'+str(y)+'_'+str(p)+'.csv')


if __name__ == '__main__':



    # code = get_all_codes_num()
    #get_all_codes_basic(code,'2005-01-01','2021-09-01')
    code = ['sz.000538', 'sh.600000', 'sh.600096', 'sh.600095', 'sh.600094', 'sh.600006', 'sh.600010']
    get_all_codes_profit()




import tushare as ts
import  baostock as bs



def login_tushare():
    token = "a4dc47e4087e6b65380021711192e5abdf5ca4783d8840690435ddec"
    ts.set_token(token)
    pro = ts.pro_api()
    return ts,pro


def login_bs():
    lg = bs.login()
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

def bs_exit():
    bs.logout()

import tushare as ts




def login_tushare():
    token = "a4dc47e4087e6b65380021711192e5abdf5ca4783d8840690435ddec"
    ts.set_token(token)
    pro = ts.pro_api()
    return ts,pro
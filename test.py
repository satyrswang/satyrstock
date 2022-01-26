import tushare as ts
import  os
from urllib.request import getproxies
print(getproxies())
item = os.environ.items()
proxies = {}
# in order to prefer lowercase variables, process environment in
# two passes: first matches any, second pass matches lowercase only
for name, value in item:
    name = name.lower()
    if value and name[-6:] == '_proxy':
        proxies[name[:-6]] = value

if 'REQUEST_METHOD' in os.environ:
    proxies.pop('http', None)
for name, value in os.environ.items():
    if name[-6:] == '_proxy':
        name = name.lower()
        if value:
            proxies[name[:-6]] = value
        else:
            proxies.pop(name[:-6], None)

# os.system("unset HTTP_PROXY")
# os.system("unset HTTPS_PROXY")
#pro = ts.pro_api()
# df = pro.query('daily', ts_code='000001.SZ', start_date='20180701', end_date='20180718')

# df = ts.get_realtime_quotes("000538")
# print(df)

import easyquotation
import pandas as pd
res = easyquotation.use("sina").stocks("000538")
df = easyquotation.use("sina").stocks("000538")
tmp = df["000538"]
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
print(dfp)

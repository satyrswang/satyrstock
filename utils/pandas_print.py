import pandas as pd


#print utils
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


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

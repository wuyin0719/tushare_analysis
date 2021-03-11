# -*- coding:utf-8 -*
import pandas as pd
import datetime,os
import numpy as np
import glob
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from pylab import arrow
# kplot_name = r'E:\中科天启\StockAnaysis\SkyImage\tushare量化分析流程\1数据下载\K线\平安银行.csv'

import itertools

def cross_point(kplot_data,delta,delta1):
    kplot_data['Ma1'] = kplot_data['close'].rolling(window=delta1).mean()
    kplot_data['Ma2'] = kplot_data['close'].rolling(window=delta).mean()

    M1 = kplot_data['Ma1'].values
    M2 = kplot_data['Ma2'].values

    import numpy
    def zcr(y):
        return numpy.diff(numpy.sign(y), prepend=0) != 0
    cross_point = zcr(M1 - M2)
    points = np.where(cross_point)[0]
    return points


def profits_rate(price_sell_p,price_buy_p,flag=">"):

    if flag==">":
        sell_temp=price_sell_p[price_sell_p>price_buy_p]
        buy_temp=price_buy_p[price_sell_p>price_buy_p]

    else:
        sell_temp = price_sell_p[price_sell_p <price_buy_p]
        buy_temp = price_buy_p[price_sell_p < price_buy_p]

    # return numpy.mean((sell_temp-buy_temp)/buy_temp)
    if len(sell_temp) == 0:
        return 0
    return np.mean((sell_temp - buy_temp)/buy_temp)
def kelly(p, q, rW, rL):
    """
    计算凯利公式

    Args:
        p (float): 获胜概率
        q (float): 失败概率
        rW (float): 净利润率
        rL (float): 净亏损率

    Returns:
        float: 最大化利润的投资本金占比(%)
    """
    return (p*rW - q*rL)/rW * rL
def linespace(para):
    if isinstance(para,list):
        return list(range(para[0],para[1],para[2]))
    else:
        return [para]

def trade_rate(close,flag_buy,keep_Time):
    price_buy_p, price_sell_p=close[flag_buy + 1], close[flag_buy + 1 + keep_Time]
    success_rate = sum((price_sell_p - price_buy_p) > 0) / len(price_buy_p)
    gains_rate = profits_rate(price_sell_p, price_buy_p, flag=">")
    loss_rate = profits_rate(price_sell_p, price_buy_p, flag="<")
    hold_rate = kelly(success_rate, 1 - success_rate, 1 + gains_rate, 1 + loss_rate)
    return success_rate, gains_rate, loss_rate ,hold_rate


def evaluate(folder,fun,param,num=100):
    # 对fun函数进行可行性评估，param是参数列表，num是评估的数量
    values=(linespace(v) for v in param.values())
    keys=list(param.keys())
    keys=keys+['meanSuccess','WeightedProfit','LossRate','hold_rate']
    res_df=[]
    for v in list(itertools.product(*values)):
        evaluate=[]
        for kplot_name in glob.glob(folder+'\\*.csv')[:num]:
            try:
                close, flag_buy, keep_Time=fun(kplot_name,*v)
                success_rate, gains_rate, loss_rate, hold_rate=trade_rate(close, flag_buy, keep_Time)
                evaluate.append([success_rate, gains_rate, loss_rate ,hold_rate])
                # break
            except:
                continue
        mean_keep=np.mean(evaluate,axis=0)
        temp=list(v)+mean_keep.tolist()
        res_df.append(temp)
        # temp_slice=(i for i in temp)
        # print(temp_slice)
        print(v,"mean Success:%.4f,gains_rate:%.4f,loss_rate%.4f,hold_rate%.4f"%(temp[-4],temp[-3],temp[-2],temp[-1],))
    res_df = pd.DataFrame(res_df, columns=keys)
    res_df.to_csv("res.csv", encoding='utf_8_sig')

def meam_Screem():
    pass
if __name__ == '__main__':
    import glob
    from collections import OrderedDict

    kplot_name = r'C:\Users\吴隐\Desktop\Python\StockAnaysis\ImageSky\tushare量化分析流程\1数据下载\K线'
    param = OrderedDict()
    param["mean_Window1"] = 5
    param["mean_Window2"] = 60
    param["keep_Time"] = [60, 120, 10]
    evaluate(kplot_name, meam_Screem, param)
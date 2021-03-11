#!/usr/bin/python
# -*- coding:utf-8 -*
import pandas as pd
import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from Evaluate_fun import evaluate, trade_rate


def cross_point(kplot_data, delta, delta1):
    kplot_data['Ma1'] = kplot_data['close'].rolling(window=delta1).mean()
    kplot_data['Ma2'] = kplot_data['close'].rolling(window=delta).mean()

    M1 = kplot_data['Ma1'].values
    M2 = kplot_data['Ma2'].values

    import numpy
    def zcr(y):
        return numpy.diff(numpy.sign(y), prepend=0) != 0
    cross_point2 = zcr(M1 - M2)
    points = np.where(cross_point2)[0]
    return points


def meam_Screem(kplot_name,devariation=0.1,bb_threshod=1,window=10,keep_Time=5,max_interval=5,cross_time=10):
    kplot_data = pd.read_csv(kplot_name, encoding='utf-8')
    name=os.path.basename(kplot_name).split('.')[0]
    kplot_data=kplot_data.reindex(index=kplot_data.index[::-1])
    stockline = [datetime.datetime.strptime(str(d), '%Y%m%d').date() for d in kplot_data['trade_date']]

    # 加这个两句 可以显示中文
    plt.rcParams['font.sans-serif'] = [u'SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 画5，60日移动平均线
    # delta1=5
    # delta=60
    delta1 = 5;delta = 60

    # 构造列表形式的绘图数据
    close=kplot_data['close'].values[delta - 1:]
    low=kplot_data['low'].values[delta - 1:]
    high=kplot_data['high'].values[delta - 1:]
    kplot_data['Ma1'] = kplot_data['close'].rolling(window=delta1).mean()
    kplot_data['Ma2'] = kplot_data['close'].rolling(window=delta).mean()

    M1 = kplot_data['Ma1']
    M2 = kplot_data['Ma2']
    MM = kplot_data['close']

    M1 = M1.values[delta - 1:]
    M2 = M2.values[delta - 1:]
    MM = MM.values[delta - 1:]
    stockline = stockline[delta - 1:]
    stockline = np.array(stockline)
    import numpy
    def zcr(y):
        return numpy.diff(numpy.sign(y), prepend=0) != 0

    cross_point = zcr(M1 - M2)
    points = np.where(cross_point)[0]
    flag_buy = []
    # time_interval = 5, time_interval2 = 30,
    # stock_Status = stock()
    holds_df = []
    j = 0
    for i in range(2, len(points) - 1):

        from_i = points[i - 1]
        from_i2 = points[i - 2]
        to_i = points[i]
        to_i2 = points[i + 1]
        # print(from_i,to_i,to_i2)
        time_delta = (stockline[to_i] - stockline[from_i]).days
        time_delta2 = (stockline[from_i] - stockline[from_i2]).days
        pp = [points[i - n] for n in range(3)]
        # percent = 0.01 * uppercent
        # cross_point3 = [M1[i] for i in pp] + [min(M1[from_i2:to_i]), max(M1[from_i2:to_i]),
        #                                       (1 - percent) * min(M1[from_i2:to_i]),
        #                                       (1 + percent) * max(M1[from_i2:to_i])]
        # print(time_delta)
        price = M1[to_i]
        price2 = max(M1[from_i2:to_i])

        if to_i2 == points[-1]:
            # print(to_i2)
            to_i2 = len(stockline)
        if j > to_i:
            continue
        else:
            j = to_i
        windows = 5
        dt=5
        while j < to_i2:
            # for j in range(to_i,to_i2,1):
            dp = ((MM[j] - MM[j - dt]) / dt)
            con2 = abs((M1[j] - M2[j]) / M2[j])
            # if M1[j]<min(M1[from_i2:to_i]):
            if (dp >0)and (con2<0.05) :
                flag_buy.append(j)
                j = j + windows
            else:
                j = j + 1

    # max_lower_i=np.array(max_lower_i)
    # flag_buy=[]
    # for lower_i in max_lower_i:
    #     nearst_points=min(abs(points-lower_i))
    #     # nearst_points=max(points[points<=lower_i])
    #     if nearst_points>cross_time:
    #         flag_buy.append(lower_i)

        # print(lower_i,nearst_points)
    flag_buy=np.array(flag_buy)+1
    while flag_buy[-1]+keep_Time>len(stockline):
        flag_buy=flag_buy[:-1]

    # success_rate, gains_rate, loss_rate, hold_rate=trade_rate(close[flag_buy+1], close[flag_buy+1+keep_Time])


    # print(success_rate, gains_rate, loss_rate ,hold_rate)
    # print(flag_buy)

    price_buy_p, price_sell_p = close[flag_buy], low[flag_buy+ keep_Time]

    price_high_p=high[flag_buy]
    price_close_before=close[flag_buy-1]
    stockline_buy_p, stockline_sell_p = stockline[flag_buy], stockline[flag_buy + keep_Time]
    out=pd.DataFrame()
    # gains=[]
    # stock_Status = stock()
    # # print(close)
    # stock_Status.add_share(1, close[0])
    # for f in flag_buy:
    #     stock_Status.add_share(0, close[f])
    #     stock_Status.add_share(1, close[f+keep_Time])
    #     gains.append(stock_Status.sum(close[f+keep_Time]))

    out['stockline_buy_p']=stockline_buy_p
    # out['bb']=x[flag_buy-1]
    out['price_buy_p']=price_buy_p
    out['price_high_p']=price_high_p
    out['price_close_before']=price_close_before
    out['best_sell_precent']=100*(price_high_p-price_close_before)/price_close_before

    out['stockline_sell_p']=stockline_sell_p
    out['price_sell_p']=price_sell_p

    # for i in range(keep_Time):
    #     out['price_%s'%i]=close[flag_buy+ i]
    # max_price=[max(close[f+1:f+keep_Time+1])for f in flag_buy]
    # # min_price_index=[close[f+1:f+keep_Time+1].index(min(close[f+1:f+keep_Time+1]))for f in flag_buy]
    # min_price_index=[]
    # for f in flag_buy:
    #     price_list=close[f+1:f+keep_Time+1].tolist()
    #     min_price_index.append(price_list.index(max(price_list)))
    # # print(min_price_index)
    # out['min_price'] = max_price
    # out['gains_end'] = 100*(price_sell_p - price_buy_p)/price_buy_p
    # out['minus_max'] = 100*(np.array(max_price)-price_buy_p)/price_buy_p
    # out['min_price_index'] = min_price_index
    # # out['gains'] = gains
    # out.to_csv("temp//%s.csv"%name,encoding='utf_8_sig')
    min_price = [min(close[f + 1:f + keep_Time + 1]) for f in flag_buy]
    # min_price_index=[close[f+1:f+keep_Time+1].index(min(close[f+1:f+keep_Time+1]))for f in flag_buy]
    min_price_index = []
    for f in flag_buy:
        price_list = close[f + 1:f + keep_Time + 1].tolist()
        min_price_index.append(price_list.index(min(price_list)))
    # print(min_price_index)
    out['min_price'] = min_price
    out['gains_end'] = 100 * (price_sell_p - price_buy_p) / price_buy_p
    out['minus_min'] = 100 * (np.array(min_price) - price_buy_p) / price_buy_p
    out['min_price_index'] = min_price_index
    # out['gains'] = gains
    out.to_csv("temp//%s.csv" % name, encoding='utf_8_sig')


    success_rate, gains_rate, loss_rate ,hold_rate=trade_rate(close,flag_buy,keep_Time)
    print(name,
          "mean Success:%.4f,gains_rate:%.4f,loss_rate%.4f,hold_rate%.4f" % (success_rate, gains_rate, loss_rate ,hold_rate))
    return close,flag_buy,keep_Time
    # return success_rate, gains_rate, loss_rate ,hold_rate


# 创两个焦点新高
# mean_Window1	mean_Window2	keep_Time   1	60	20    金叉5天



if __name__ == '__main__':
    from collections import OrderedDict

    # kplot_name=r'E:\中科天启\StockAnaysis\SkyImage\tushare量化分析流程\1数据下载\K线Selected\海螺水泥.csv'
    # meam_Screem(kplot_name,keep_Time=20)

    kplot_name = r'E:\中科天启\StockAnaysis\SkyImage\tushare量化分析流程\1数据下载\K线Selected'
    param=OrderedDict()
    # devariation = 0.1, bb_threshod = 1, window = 10, keep_Time = 5, max_interval = 5, cross_time = 10
    # param["mean_Window1"] = 5
    # param["mean_Window2"] = 60
    param["devariation_above60"] =0.05
    param["bb_threshod"] =0.1
    param["window"] =10
    param["keep_Time"] =10
    param["max_interval"] = 3
    evaluate(kplot_name, meam_Screem, param)

#!/usr/bin/python
# -*- coding:utf-8 -*
import pandas as pd
import datetime,os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from Evaluate_fun import evaluate,trade_rate,stock
from plotGains import hold_analysis
def cal_bool(close):
    time_period = 20  # SMA的计算周期，默认为20
    stdev_factor = 2  # 上下频带的标准偏差比例因子
    history = []  # 每个计算周期所需的价格数据
    sma_values = []  # 初始化SMA值
    upper_band = []  # 初始化阻力线价格
    lower_band = []  # 初始化支撑线价格
    width = []
    bb = []
    for close_price in close:
        #
        history.append(close_price)
        # 计算移动平均时先确保时间周期不大于20
        if len(history) > time_period:
            del (history[0])
        # 将计算的SMA值存入列表
        sma = np.mean(history)
        sma_values.append(sma)
        # 计算标准差
        stdev = np.sqrt(np.sum((history - sma) ** 2) / len(history))
        upper_band.append(sma + stdev_factor * stdev)
        lower_band.append(sma - stdev_factor * stdev)
        sdt_interval=2*stdev_factor * stdev
        if sdt_interval==0:
            bb_i=0
            width_i=0
        else:
            bb_i=(close_price-(sma - stdev_factor * stdev))/(2*stdev_factor * stdev)
            width_i=(2*stdev_factor * stdev)/sma
        bb.append(bb_i)
        width.append(width_i)
    return bb,width
def meam_Screem(kplot_name,bb_threshod=1,keep_Time=5,max_interval=5):
    kplot_data = pd.read_csv(kplot_name, encoding='utf-8')
    name=os.path.basename(kplot_name).split('.')[0]
    kplot_data=kplot_data.reindex(index=kplot_data.index[::-1])
    stockline = [datetime.datetime.strptime(str(d), '%Y%m%d').date() for d in kplot_data['trade_date']]

    # 加这个两句 可以显示中文
    plt.rcParams['font.sans-serif'] = [u'SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 构造列表形式的绘图数据
    close=kplot_data['close'].values
    low=kplot_data['low'].values
    high=kplot_data['high'].values
    pct_chg=kplot_data['pct_chg'].values

    stockline=np.array(stockline)
    bb,width=cal_bool(close)
    kplot_data['bb']=bb
    kplot_data['bb6'] = kplot_data['bb'].rolling(window=6).mean()
    bb6=kplot_data['bb6'].values
    x=np.array(bb)
    max_i=argrelextrema(x, np.greater)[0]
    max_lower_i=[]
    for i in range(1,len(max_i)):
        flag2=pct_chg[max_i[i]+1]>0  #第二天涨幅大于零
        if flag2 :
            flag3 = (max_i[i] - max_i[i - 1]) < max_interval  #bb顶与顶间隔小于max_interval 天
            flag4 = x[max_i[i]] > 0.7 * bb_threshod      #bb顶比顶低阈值
            buy_flag1=x[max_i[i]] > bb_threshod   #bb 大于阈值
            buy_flag2=(x[max_i[i]]<x[max_i[i-1]]) and flag3 and flag4
            if buy_flag1:
                max_lower_i.append(max_i[i])
            elif buy_flag2:
                max_lower_i.append(max_i[i])
    flag_buy=np.array(max_lower_i)+1
    while flag_buy[-1]+keep_Time>len(stockline):
        flag_buy=flag_buy[:-1]

    # hold_analysis(flag_buy,kplot_data,keep_Time=keep_Time,ifshow=True,name=name)

    price_buy_p, price_sell_p = close[flag_buy], close[flag_buy+ keep_Time]

    # price_high_p=high[flag_buy]
    # price_close_before=close[flag_buy-1]
    stockline_buy_p, stockline_sell_p = stockline[flag_buy], stockline[flag_buy + keep_Time]
    out=pd.DataFrame()
    out['stockline_buy_p']=stockline_buy_p
    out['pct_chg']=pct_chg[flag_buy]

    for i in range(keep_Time+1):
        out['buy_%s'%i] = close[flag_buy+ i]
    # out['bb']=x[flag_buy-1]
    # out['price_buy_p']=price_buy_p
    # out['pct_chg']=pct_chg[flag_buy]
    # out['price_high_p']=price_high_p
    # out['price_close_before']=price_close_before
    # out['best_sell_precent']=100*(price_high_p-price_close_before)/price_close_before
    #
    # out['stockline_sell_p']=stockline_sell_p
    # out['price_sell_p']=price_sell_p
    min_price=[min(low[f:f+keep_Time+1])for f in flag_buy]
    min_price_index=[]
    for f in flag_buy:
        price_list=low[f+1:f+keep_Time+1].tolist()
        min_price_index.append(price_list.index(min(price_list)))
    # out['min_price'] = min_price
    out['gains'] = 100*(price_sell_p - price_buy_p)/price_buy_p
    out['chance'] = 100*(np.array(min_price)-price_buy_p)/price_buy_p
    # out['chance_i'] = min_price_index
    out.to_csv("temp//%s.csv"%name,encoding='utf_8_sig')


    success_rate, gains_rate, loss_rate ,hold_rate=trade_rate(close,flag_buy,keep_Time)
    print(name,
          "mean Success:%.4f,gains_rate:%.4f,loss_rate%.4f,hold_rate%.4f" % (success_rate, gains_rate, loss_rate ,hold_rate))
    return close,flag_buy,keep_Time

# 创两个焦点新高
# mean_Window1	mean_Window2	keep_Time   1	60	20    金叉5天
if __name__ == '__main__':
    from collections import OrderedDict
    kplot_name = r'E:\中科天启\StockAnaysis\SkyImage\tushare量化分析流程\1数据下载\K线Selected'
    param=OrderedDict()
    # param["devariation_above60"] =0.05
    param["bb_threshod"] =1
    # param["window"] =10
    param["keep_Time"] =10
    param["max_interval"] = 5
    evaluate(kplot_name, meam_Screem, param)

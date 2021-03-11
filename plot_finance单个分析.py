#!/usr/bin/python
# -*- coding:utf-8 -*
import pandas as pd
import datetime,os
import numpy as np
import matplotlib.pyplot as plt
from pylab import arrow
from plotGains import hold_analysis, evaluate,stock_choose,kelly

kplot_name = r'E:\中科天启\StockAnaysis\SkyImage\tushare量化分析流程\1数据下载\K线\平安银行.csv'

# import numpy as np
def axis_Divide(value,flag,zero_point=None):
    # [3, 6, 9, 12]
    zero_point=np.array(zero_point)
    zero_point.sort()
    # flag=0
    if flag==0:
        return value<zero_point[0]
    if flag>0 and flag<len(zero_point):
        return value>zero_point[flag-1] and value<zero_point[flag]
    if flag==len(zero_point):
        return value>zero_point[flag-1]

# def price_Index(value,zero_point=None):
#     # [3, 6, 9, 12]
#     zero_point2=np.array(zero_point)
#     zero_point2.sort()
#
    # flag=0
    # if flag==0:
    #     return value<zero_point[0]
    # if flag>0 and flag<len(zero_point):
    #     return value>zero_point[flag-1] and value<zero_point[flag]
    # if flag==len(zero_point):
    #     return value>zero_point[flag-1]
class stock:
    def __init__(self):
        self.share=0
        self.price=0
        self.profit=1
        self.times=0
        self.percent=0
    def add_share(self,percent,price):
        #持股比例，价格
        if abs(percent-self.percent)>0.2:
            self.percent=percent
            self.times =self.times+1
            if percent>0:
                if self.share==0:
                    self.share=(percent*self.profit)/price
                    self.price=price

                    self.profit=self.profit-self.share*self.price
                else:
                    temp_money=self.profit+self.share*price
                    self.share =(percent*temp_money)/price
                    self.price=price
                    self.profit=(1-percent)*temp_money
            else:
                self.profit = self.profit + self.share * price
                self.share = 0
                self.price = 0

    def sum(self,price):
        return self.profit + self.share * price-self.times*0.0005

def price_Index(target,theList=None):
    low = 0
    high = len(theList) - 1
    while low <= high:
        mid = (high + low) // 2
        if theList[mid] == target:
            return mid
        elif target < theList[mid]:
            high = mid -1
        else:
            low = mid + 1
    return low
def combine_info(price_info,conpany_info):
    success_rate=price_info[0]+(1-price_info[0])*conpany_info[0]
    gains_rate=price_info[1]+(1-price_info[0])*conpany_info[1]
    loss_rate=price_info[2]+(1-price_info[0])*conpany_info[2]
    # hold_rate=kelly(p, q, rW, rL)
    hold_rate = kelly(success_rate, 1 - success_rate, 1 + gains_rate, 1 + loss_rate)
    return hold_rate
    # [success_rate, gains_rate, loss_rate, hold_rate]
def meam_Screem(kplot_name,conpany_info,delta1=5,delta=60,uppercent=32,ifshow=False,dt=5):
    kplot_data = pd.read_csv(kplot_name, encoding='utf-8')
    name=os.path.basename(kplot_name).split('.')[0]

    kplot_data=kplot_data.reindex(index=kplot_data.index[::-1])
    stockline = [datetime.datetime.strptime(str(d), '%Y%m%d').date() for d in kplot_data['trade_date']]


    hold_status = pd.read_csv("均值大于零.csv", encoding='utf-8')
    hold_percent = hold_status[hold_status['price_position'] == 0]['hold_rate'].values[0]
    # hold_percent = price_flag.values[0]

    # 加这个两句 可以显示中文
    plt.rcParams['font.sans-serif'] = [u'SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 画5，60日移动平均线
    # delta1=5
    # delta=60
    # time_interval=10
    kplot_data['Ma1'] = kplot_data['close'].rolling(window=delta1).mean()
    kplot_data['Ma2'] = kplot_data['close'].rolling(window=delta).mean()

    M1=kplot_data['Ma1']
    M2=kplot_data['Ma2']
    MM=kplot_data['close']

    M1 = M1.values[delta-1:]
    M2 = M2.values[delta-1:]
    MM = MM.values[delta - 1:]
    stockline=stockline[delta-1:]
    stockline=np.array(stockline)
    import numpy
    def zcr(y):
        return numpy.diff(numpy.sign(y), prepend=0) != 0
    cross_point=zcr(M1-M2)
    points=np.where(cross_point)[0]
    flag_buy=[]
    # time_interval = 5, time_interval2 = 30,
    stock_Status=stock()
    holds_df = []
    j=0
    for i in range(2,len(points)-1):

        from_i=points[i-1]
        from_i2=points[i-2]
        to_i=points[i]
        to_i2=points[i+1]
        # print(from_i,to_i,to_i2)
        time_delta=(stockline[to_i]-stockline[from_i]).days
        time_delta2=(stockline[from_i]-stockline[from_i2]).days
        pp=[points[i-n] for n in range(3)]
        percent=0.01*uppercent
        cross_point3=[M1[i]for i in pp]+[min(M1[from_i2:to_i]),max(M1[from_i2:to_i]),(1-percent)*min(M1[from_i2:to_i]),(1+percent)*max(M1[from_i2:to_i])]
        # print(time_delta)
        price=M1[to_i]
        price2=max(M1[from_i2:to_i])

        if to_i2==points[-1]:
            # print(to_i2)
            to_i2=len(stockline)
        if j>to_i:
            continue
        else:
            j=to_i
        windows=5
        while j<to_i2:
        # for j in range(to_i,to_i2,1):
            dp=((MM[j]-MM[j-dt])/dt)
            con2=abs((M1[j]-M2[j])/M2[j])
            # if M1[j]<min(M1[from_i2:to_i]):
            if (dp>0) or (con2<0.05):
                index = price_Index(M1[j], cross_point3)
                # ['meanSuccess', 'meanGains', 'meanLoss']
                price_info=hold_status[hold_status['price_position'] == index].values[0][6:9]
                hold_percent=combine_info(price_info, conpany_info)
                # conpany_info
                # print(hold_percent)
                # hold_percent=hold_status[hold_status['price_position'] == index]['hold_rate'].values[0]
                if hold_percent==stock_Status.percent:
                    j = j + 1
                    continue
                if hold_percent>0.61:
                    stock_Status.add_share(hold_percent,MM[j])
                    holds_df.append([stockline[j],stock_Status.share,stock_Status.profit,M1[j],stock_Status.sum(M1[j]),stock_Status.percent])
                    j=j+windows

            else:
                stock_Status.add_share(0.0, MM[j])
                holds_df.append([stockline[j],stock_Status.share,stock_Status.profit,MM[j],stock_Status.sum(MM[j]),stock_Status.percent])
            j = j + 1
            # print(j)



            # if axis_Divide(M1[j],price_position,zero_point=cross_point3) and (dp<=0):
            # if (M1[j]>price2) :
                # if  (time_interval<time_delta<time_interval2)and (time_interval<time_delta2<time_interval2):
                #     flag_buy.append(j)
                #     break
    # flag_buy=np.array(flag_buy)
    # success_rate, gains_rate,loss_rate=hold_analysis(flag_buy, kplot_data, [delta1,delta], keep_Time=keep_Time, ifshow=ifshow, name=name)
    # print(stock_Status.share)
    # print(stock_Status.profit)
    # print(stock_Status.price)
    profit=stock_Status.sum(M1[-1])
    # print(stock_Status.times)
    holds_df.append([stockline[-1], stock_Status.share,stock_Status.profit, M1[-1],stock_Status.sum(M1[-1]),stock_Status.percent])
    res_df = pd.DataFrame(holds_df, columns=['time','share','profit','price','Gains','Percent'])
    res_df.to_csv("temp\\%s_Strategy.csv"%name, encoding='utf_8_sig')
    mornal_gains=(M1[-1]-M1[0])/M1[0]
    return name,profit,stock_Status.times,stock_Status.percent,mornal_gains

# delta1=10, delta=75,keep_Time=6,  ifshow=False,dt=5  success_rate:84%   0.0249
# delta1=11, delta=59,keep_Time=8,  ifshow=False,dt=5  success_rate:81.6%   0.029

# 创两个焦点新高
# delta1=11, delta=59,keep_Time=8,   success_rate:88.4%   0.048
# delta1=11, delta=59,keep_Time=54 --57,   success_rate:64.7%   0.056--0.0531  之后收益开始减少
# delta1=11, delta=59,keep_Time=12,  success_rate:84.7%   0.054               之后增长速度放缓
# 创两个11，59均线交叉点新高 持仓时间  12天以下胜率最高，59收益最多，100极限
if __name__ == '__main__':
    # import glob
    # import glob
    from collections import OrderedDict

    param = OrderedDict()
    # folder=r'C:\Users\吴隐\Desktop\Python\StockAnaysis\ImageSky\tushare量化分析流程\1数据下载\K线'
    param["mean_Window1"] =10
    param["mean_Window2"] = 60
    # param["keep_Time"] = 20
    # param["keep_Time"] = 20
    # param["price_position"] = 7
    # param["price_position"] = [0, 8, 1]
    # param["uppercent"] = 32

    # print(param.keys())
    folder = r'K线Selected'
    # from Enumerate_All import evaluate

    # evaluate(folder, meam_Screem, param)
    import glob
    status=[]
    for kplot_name in glob.glob(folder + '\\*.csv'):
        # try:
        canpany_info=stock_choose(kplot_name,windows =60)

        if canpany_info[-1]>0:
            name, profit,times,percent,mornal_gains=meam_Screem(kplot_name, canpany_info[:-1],delta1=5, delta=60,  uppercent=32, ifshow=False,
                        dt=1)
            status.append([name,canpany_info[-1], profit,times,percent,mornal_gains])
        # except:
        #     pass
    status = pd.DataFrame(status, columns=['name','hold_rate' ,'profit','times','hold_status','mornal_gains'])
    status.to_csv("profit_all.csv", encoding='utf_8_sig')
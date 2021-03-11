import numpy
import matplotlib.pyplot as plt
import datetime
import itertools
import glob
import pandas as pd
import numpy as np
def increase_decrease(stockline,M1,time_buy_p,price_buy_p, time_sell_p,price_sell_p,tag='increase'):
    if tag=='increase':
        time_buy_p2 = time_buy_p[price_buy_p < price_sell_p]
        time_sell_p2 = time_sell_p[price_buy_p < price_sell_p]
        price_sell_p2 = price_sell_p[price_buy_p < price_sell_p]
        price_buy_p2 = price_buy_p[price_buy_p < price_sell_p]
    else:
        time_buy_p2 = time_buy_p[price_buy_p>price_sell_p]
        time_sell_p2 = time_sell_p[price_buy_p > price_sell_p]

        price_sell_p2 = price_sell_p[price_buy_p > price_sell_p]
        price_buy_p2 = price_buy_p[price_buy_p > price_sell_p]
    if tag=='increase':
        color='coral'
    else:
        color='g'
    for i in range(len(time_buy_p2)):
        index = numpy.where((time_buy_p2[i] < stockline) & (stockline <= time_sell_p2[i]))
        x = stockline[index]
        y = M1[index]
        min_y = min(M1)
        y2 = [min_y for i in range(len(y))]
        if i == 0:
            plt.fill_between(x, y, y2, facecolor=color, label="收益（%）")
        else:
            plt.fill_between(x, y, y2, facecolor=color)

        gains = '%.1f' % (100 * (price_sell_p2[i] - price_buy_p2[i]) / price_buy_p2[i])
        plt.annotate("",
                     xy=(time_buy_p2[i], price_buy_p2[i]),
                     xycoords='data',
                     xytext=(-30, -30),
                     textcoords='offset points',
                     arrowprops=dict(headwidth=2, width=1, color='r',  # '#363d46',
                                     connectionstyle="angle3,angleA=0,angleB=-90"),
                     fontsize=12)
        m = x.min()
        plt.text((m + (x - m).mean()), min_y, gains, horizontalalignment='center',verticalalignment = 'center')

def hold_analysis(flag_buy,kplot_data,windows,keep_Time=5,ifshow=False,name=''):
    # 无差别卖出，只有时间限制
    stockline = [datetime.datetime.strptime(str(d), '%Y%m%d').date() for d in kplot_data['trade_date']]
    stockline = numpy.array(stockline)
    for w in windows:
        kplot_data['Ma%s'%w] = kplot_data['close'].rolling(window=w).mean()
    # kplot_data['Ma2'] = kplot_data['close'].rolling(window=delta).mean()

    M1 = kplot_data['Ma%s'%windows[0]].values[windows[-1] - 1:]
    stockline=stockline[windows[-1] - 1:]

    flag_buy=numpy.array(flag_buy)
    flag_sell=[]
    for p in flag_buy:
        time_buy_p = stockline[p]
        sell_time=time_buy_p+datetime.timedelta(days=keep_Time)
        try:
            sell_point=numpy.where(stockline>sell_time)[0][0]
            flag_sell.append(sell_point)
        except:
            flag_sell.append(len(stockline)-1)
    flag_sell=numpy.array(flag_sell)
    # print(flag_buy,flag_sell)
    time_sell_p = stockline[flag_sell]
    price_sell_p = M1[flag_sell]
    time_buy_p=stockline[flag_buy]
    price_buy_p=M1[flag_buy]

    year = numpy.array([i.days / 365.00 for i in (time_sell_p - time_buy_p)])
    success_rate = sum((price_sell_p - price_buy_p) > 0)/len(price_buy_p)

    # price_sell_p
    gains_rate = numpy.mean((price_sell_p - price_buy_p)/price_buy_p)
    if ifshow:
        print("success_rate: %3.4f, gains_rate: %3.4f"%(success_rate, gains_rate))
        plt.rcParams['font.sans-serif'] = [u'SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        increase_decrease(stockline, M1, time_buy_p, price_buy_p, time_sell_p, price_sell_p, tag='increase')
        increase_decrease(stockline, M1, time_buy_p, price_buy_p, time_sell_p, price_sell_p, tag='decrease')
        plt.plot(stockline,M1,label='M%s'%windows[0])
        for i in windows[1:]:
            M = kplot_data['Ma%s' % i].values[windows[-1] - 1:]
            plt.plot(stockline, M, label='M%s' % i)
        plt.title(name+" keepTime:%s d"%keep_Time)
        plt.legend()
        plt.show()

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
        return numpy.mean((sell_temp - buy_temp)/buy_temp)
        # if sell_temp

    gains_rate=profits_rate(price_sell_p,price_buy_p,flag=">")
    # if np.isnan(gains_rate):
    #     gains_rate=
    #     print(price_sell_p,price_buy_p)
    loss_rate=profits_rate(price_sell_p,price_buy_p,flag="<")
    # if np.isnan(loss_rate):
    #     print(price_sell_p,price_buy_p)
    # print(gains_rate,loss_rate)
    return success_rate, gains_rate,loss_rate


def linespace(para):
    if isinstance(para,list):
        return list(range(para[0],para[1],para[2]))
    else:
        return [para]

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

def evaluate(folder,fun,param):
    values=(linespace(v) for v in param.values())
    keys=list(param.keys())
    keys=keys+['meanSuccess','meanGains','meanLoss','hold_rate']
    res_df=[]
    for v in list(itertools.product(*values)):
        evaluate=[]
        for kplot_name in glob.glob(folder+'\\*.csv'):
            # success_rate, gains_rate, loss_rate = fun(kplot_name, *v)
            # success_rate, gains_rate, loss_rate = fun(kplot_name, *v)
            try:
                success_rate, gains_rate,loss_rate=fun(kplot_name,*v)
                # if np.isnan(gains_rate) or np.isnan(loss_rate):
                #     continue
                # print(success_rate)
                evaluate.append([success_rate, gains_rate,loss_rate])
            except:

                # print("plotGains,124 Line")
                continue

            # if (np.isnan(gains_rate) or np.isnan(loss_rate)):
            #     evaluate.append([success_rate, gains_rate, loss_rate])


        # print(evaluate)
        succ,profit,loss=np.mean(evaluate,axis=0)

        hold_rate=kelly(succ, 1-succ, 1+profit, 1+loss)
        temp=list(v)+[succ,profit,loss,hold_rate]
        res_df.append(temp)
        # print(succ,profit,loss)
        print(v,"success_rate: %.4f,gains_rate:%.4f,loss_rate:%.4f,hold_rate:%.4f"%(succ,profit,loss,hold_rate))
    res_df = pd.DataFrame(res_df, columns=keys)
    res_df.to_csv("res.csv", encoding='utf_8_sig')


def stock_choose(kplot_name,windows = 60):
    import os
    kplot_data = pd.read_csv(kplot_name, encoding='utf-8')
    name = os.path.basename(kplot_name).split('.')[0]
    kplot_data = kplot_data.reindex(index=kplot_data.index[::-1])
    # stockline = [datetime.datetime.strptime(str(d), '%Y%m%d').date() for d in kplot_data['trade_date']]


    # print(int(len(kplot_data)/windows))

    flag_buy = [windows * i for i in range(int(len(kplot_data) / windows))]
    # stockline = numpy.array(stockline)
    success_rate, gains_rate, loss_rate,hold_rate=0,0,0,0,
    try:
        success_rate, gains_rate, loss_rate = hold_analysis(flag_buy, kplot_data, [3, 50], keep_Time=50, ifshow=False,
                                                            name='')

        hold_rate = kelly(success_rate, 1 - success_rate, 1 + gains_rate, 1 + loss_rate)

        print('name:%s success_rate:%.2f, gains_rate:%.2f,loss_rate:%.2f,hold_rate:%.2f' % (
        name, success_rate, gains_rate, loss_rate, hold_rate))
    except:
        pass

    return [success_rate, gains_rate, loss_rate,hold_rate]

if __name__ == '__main__':
    import pandas as pd
    import os

    folder = r'C:\Users\吴隐\Desktop\Python\StockAnaysis\ImageSky\tushare量化分析流程\1数据下载\K线'
    for kplot_name in glob.glob(folder + '\\*.csv'):
        kplot_data = pd.read_csv(kplot_name, encoding='utf-8')
        name = os.path.basename(kplot_name).split('.')[0]
        kplot_data = kplot_data.reindex(index=kplot_data.index[::-1])
        # stockline = [datetime.datetime.strptime(str(d), '%Y%m%d').date() for d in kplot_data['trade_date']]

        windows=60
        # print(int(len(kplot_data)/windows))

        flag_buy=[windows*i for i in range(int(len(kplot_data)/windows))]
        # stockline = numpy.array(stockline)
        try:
            success_rate, gains_rate, loss_rate=hold_analysis(flag_buy, kplot_data,[3,50], keep_Time = 50, ifshow = False, name = '')

            hold_rate = kelly(success_rate, 1 - success_rate, 1 + gains_rate, 1 + loss_rate)

            print('name:%s success_rate:%.2f, gains_rate:%.2f,loss_rate:%.2f,hold_rate:%.2f'%(name,success_rate, gains_rate,loss_rate,hold_rate))
        except:pass
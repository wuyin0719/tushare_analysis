# from itertools import combinations
import itertools
import glob
import numpy as np
import pandas as pd
# a = ["foo", "melon"]
# b = [True, False]
# d= [1,2]
# c = list(itertools.product(a, b,d))
# print(c)
# comb = combinations([2, 1, 3], [2,3])
# for c in list(comb):
#     print(c)
# def fun(x,y,z):
#     print(x,y,z)

def linespace(para):
    if isinstance(para,list):
        return list(range(para[0],para[1],para[2]))
    else:
        return [para]
def evaluate(folder,fun,param):
    values=(linespace(v) for v in param.values())
    keys=list(param.keys())
    keys=keys+['meanSuccess','WeightedProfit','LossRate','hold_rate']
    res_df=[]
    for v in list(itertools.product(*values)):
        evaluate=[]
        for kplot_name in glob.glob(folder+'\\*.csv')[:150]:
            try:
                success_rate, gains_rate,loss_rate=fun(kplot_name,*v)
                evaluate.append([success_rate, gains_rate])
            except:
                continue
        succ,profit=np.mean(evaluate,axis=0)
        temp=list(v)+[succ,profit,succ*profit,loss_rate]
        res_df.append(temp)
        print(v,"mean Success:%.4f,success:%.4f,%.4f,mean_profit%.4f"%(np.mean(arr),succ,profit,succ*profit))
    res_df = pd.DataFrame(res_df, columns=keys)
    res_df.to_csv("res.csv", encoding='utf_8_sig')



if __name__ == '__main__':
    dict_r={1:2}
    print(list(dict_r.keys()))
    # evaluate(fun,0)
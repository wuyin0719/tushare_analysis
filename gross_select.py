import pandas as pd
import numpy as np
report1 = pd.read_csv('select_gross_profit_rate.csv', encoding='utf-8')

per30=[]
for i,row in report1.iterrows():
    values=row.values[2:]
    quantile=np.percentile(values,30)
    per30.append(quantile)
    # print(quantile)
    # break
report1["per30"]=per30

report1.to_csv('select_gross_profit_rate2.csv', encoding='utf_8_sig')
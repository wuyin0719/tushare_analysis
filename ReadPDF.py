#!/usr/bin/python
# -*- coding:utf-8 -*


# path=r"E:\中科天启\StockAnaysis\SkyImage\anumualReport\report.pdf"
path=r"E:\中科天启\StockAnaysis\SkyImage\tushare量化分析流程\res\anumualReport\良品铺子：良品铺子股份有限公司2020年年度报告.PDF"
# import camelot
# tables = camelot.read_pdf(path) #类似于Pandas打开CSV文件的形式
# # tables[0].df # get a pandas DataFrame!
# tables.export('foo.csv', f='csv', compress=True) # json, excel, html, sqlite，可指定输出格式


import os,pdfplumber
import pandas as pd

def read_PDF_table(path,text_Flag=['企业集团的构成','在子公司的持股比例不同于表决权比例的说明'],headers_n=2):
    # path = r"E:\中科天启\StockAnaysis\SkyImage\anumualReport\report.pdf"
    file = os.path.expanduser(path)
    # text_Flag=['企业集团的构成','重要非全资子公司']   //表格开始和结束时候的描述信息
    # headers_n=2  //表头为自定，原始表头有有几行
    flag=False
    values=[]
    with pdfplumber.open(file) as pdf:

        first_page = pdf.pages[0]
        for i,first_page in enumerate(pdf.pages):
            # print(first_page)
            table = first_page.extract_table()
            if table==None:
                continue
            text = first_page.extract_text()
            if text_Flag[0] in text:
                # line0=table[0]
                # line1=table[1]
                # headers_str=[line0[i] if line0[i] is not None else line1[i] for i in range(len(line0))]

                flag=True

            if flag:
                # table = first_page.extract_table()
                print(i)
                # if table!=None:
                for t in table[headers_n:]:
                    values.append(t)
                    # print(t)
                # break
            if text_Flag[1] in text:
                break
                # flag=False
    headers_str=['子公司全称', '主要经营地', '注册地', '业务性质',  '直接持股比例 (%)', "间接持股比例 (%)", '取得方式']#'注册资本',
    status = pd.DataFrame(values, columns=headers_str)
    status.to_csv("subsidiaries_info.csv", encoding='utf_8_sig')

if __name__ == '__main__':
    read_PDF_table(path)
    path2="subsidiaries_info.csv"
    subsidiaries_info = pd.read_csv(path2, encoding='utf-8')
    location=subsidiaries_info["主要经营地"]
    summary=location.value_counts()

    import io
    keys=summary.keys().values
    keys=[k.replace("\n","")for k in keys]
    str_keys=",".join(keys)
    values=[str(v)for v in summary.values]
    str_values=",".join(values)
    print(str_keys)
    import codecs
    # with open("summary.txt","w") as f:
    with codecs.open('summary.txt', 'w', encoding='utf-8') as f:
        f.write(str_keys)
        f.write("\n")
        f.write(str_values)

    # summary.to_csv("summary.csv", encoding='utf_8_sig')
    # print(summary.keys().values)
    # print(summary.values)
    # for index, row in summary.iterrows():
    #     print(index,row)  # 输出每行的索引值
    # print(summary)
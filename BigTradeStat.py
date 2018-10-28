# conding=utf-8

from WindPy import w
from OperFunc import *
from ReadFunc import *
from WriteFunc import *
import time

#####################
#codelist = ['RB.SHF','I.DCE','J.DCE']
code = 'RB.SHF'
bigline = 1000     #手动指定大单标准线
#bigline = [x for x in range(0,500,100)]    #等差列表产生一系列大单标准线
'''
红: {2:'空平',4:'多开',6:'多换',7:'双开'}
绿: {1:'空开',3:'空换',5:'多平',8:'双平'}
'''
output_title()
#####################

df = ReadTradeInfo(code)    #读取之前的交易数据,{index:dataframe}
#print(df.rt_nature)

for index, row in df.iterrows():
    if index >= 10230:
        rowdate = row.rt_date
        rowtime = row.rt_time
        dfindex = df[:index+1]  #切片获取到index为止的数据
        dfbig = df[:index+1].loc[dfindex['rt_last_vol'] >= bigline]
        #print(dfindex)
        #print(dfbig)
        total_vol = dfindex.iloc[:,4].sum()     #到index为止的总交易量
        total_oi = dfindex.iloc[:,5].sum()      #到index为止的总增仓量
        big_vol = dfbig.iloc[:,4].sum()     #到index为止的大单总交易量
        big_oi = dfbig.iloc[:,5].sum()      #到index为止的大单总增仓量

        vol_nature, oi_nature, big_vol_nature, big_oi_nature = split_big_group(dfindex, dfbig)

        output(rowdate,rowtime,total_vol,total_oi,big_vol,big_oi,vol_nature, oi_nature, big_vol_nature, big_oi_nature)

        #print(grouped.loc[grouped['rt_nature']==1,'rt_last_vol'])
#column_vol_sum = df[code].iloc[:,4].sum()
#print(code,column_vol_sum)
#df2[code] = df[code].loc[df[code]['rt_last_vol'] > bigline]

#grouped = df2[code].groupby('rt_nature').sum()
#print(grouped)
#amt1 = grouped.ix[1].rt_last_vol
#print(amt1)
#print(amt1/column_vol_sum)



#codes = ','.join(codelist)
#rt_date = {}
#rt_time = {}
#rt_last = {}
#rt_last_vol = {}
#rt_nature = {}
#codefile = {}
#
#for item in codelist:
#    rt_date[item] = ''
#    rt_time[item] = ''
#    rt_last[item] = ''
#    rt_last_vol[item] = ''
#    rt_nature[item] = 0
    #filename = item+".csv"
    #if os.path.isfile(filename):
    #    codefile[item] = open(filename, 'a')
    #else:
    #    codefile[item] = open(filename, 'a')
    #    print('rt_date','rt_time','rt_last','rt_last_vol','rt_nature',sep=',',file=codefile[item])
    #    codefile[item].flush()
#def test(indata):
    #print(indata)
    #return(indata.Codes)

#w.start()
#tradeinfo = w.wsq(codes, "rt_date,rt_time,rt_last,rt_last_vol,rt_nature",func=test)
#print(tradeinfo)
    #实时绘图
#w.stop()
#  w.cancelRequest(0)
# conding=utf-8

from WindPy import w
from OperFunc import *
from ReadFunc import *
from WriteFunc import *
import time

#####################
#codelist = ['RB.SHF','I.DCE','J.DCE']
code = 'RB.SHF'
bigline = 2000     #手动指定大单标准线
#bigline = [x for x in range(0,500,100)]    #等差列表产生一系列大单标准线
'''
红: {2:'空平',4:'多开',6:'多换',7:'双开'}
绿: {1:'空开',3:'空换',5:'多平',8:'双平'}
'''

#####################
df = {}
df2 = {}

df[code] = ReadTradeInfo(code)    #读取之前的交易数据,{index:dataframe}
column_vol_sum = df[code].iloc[:,4].sum()
print(code,column_vol_sum)
df2[code] = df[code].loc[df[code]['rt_last_vol'] > bigline]

grouped = df2[code].groupby('rt_nature').sum()
print(grouped)
amt1 = grouped.ix[1].rt_last_vol
print(amt1)
print(amt1/column_vol_sum)



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
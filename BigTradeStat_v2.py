# conding=utf-8
'''
读取多个文件（以往数据+实时数据），根据秒级数据，以所有数据计算，（每隔1分钟）实时更新vol、oi、分nature数据等信息。
'''
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
start = datetime.now()
print('开始：',start.strftime('%Y%m%d %H:%M:%S'))


oldfiles, livefile = get_files(code)
olddf = read_old_files(oldfiles)

now = datetime.now().strftime('%Y%m%d')
outfile = open('test_' + now + '.csv', mode='w')
output_title(outfile)

total = []
total_nature = []

### 读取以往数据，逐行计算各参量 ###
for index, row in olddf.iterrows():
    rowdate = row.rt_date
    rowtime = row.rt_time
    dfindex = olddf[:index+1]  #切片获取到index为止的所有数据
    dfbig = olddf[:index+1].loc[dfindex['rt_last_vol'] >= bigline]  #切片获取到index为止的大单数据
    total = sum_big_vol(dfindex, dfbig)
    total_nature = split_big_group(dfindex, dfbig)
    output(outfile,rowdate,rowtime,total,total_nature)

end = datetime.now()
print('结束：',end.strftime('%Y%m%d %H:%M:%S'))
print('用时：',(end-start).seconds)
#output_title()
######################
#
#df = ReadTradeInfo(code)    #读取之前的交易数据,{index:dataframe}
##print(df.rt_nature)
#
#for index, row in df.iterrows():
#    if index >= 10230:
#        rowdate = row.rt_date
#        rowtime = row.rt_time
#        dfindex = df[:index+1]  #切片获取到index为止的数据
#        dfbig = df[:index+1].loc[dfindex['rt_last_vol'] >= bigline]
#        #print(dfindex)
#        #print(dfbig)
#        total_vol = dfindex.iloc[:,4].sum()     #到index为止的总交易量
#        total_oi = dfindex.iloc[:,5].sum()      #到index为止的总增仓量
#        big_vol = dfbig.iloc[:,4].sum()     #到index为止的大单总交易量
#        big_oi = dfbig.iloc[:,5].sum()      #到index为止的大单总增仓量
#
#        vol_nature, oi_nature, big_vol_nature, big_oi_nature = split_big_group(dfindex, dfbig)
#
#        output(rowdate,rowtime,total_vol,total_oi,big_vol,big_oi,vol_nature, oi_nature, big_vol_nature, big_oi_nature)

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
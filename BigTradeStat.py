# conding=utf-8

from WindPy import w
from OperFunc import *
from ReadFunc import *
from WriteFunc import *
import time

#####################
timelist = ["8:00","23:59"]
timeinterval = 0.5
codelist = ['RB.SHF','I.DCE','J.DCE']
#codelist = ['RB.SHF']
bigline = [200]     #手动指定大单标准线
#bigline = [x for x in range(0,500,100)]    #等差列表产生一系列大单标准线
#####################

tradedata = ReadOldTradeInfo(codelist)    #读取之前的交易数据,{index:dataframe}
#print(tradedata)
w.start()
while CheckTime(timelist):  #检查是否在交易时间段内
    interval = CalcInterval(timeinterval, timelist)    #返回读取当天交易数据的时间间隔
    time.sleep(interval)    #暂停时间间隔后再进行操作
    livetradedata = ReadTradeInfo(codelist)  #获取各品种的实时交易数据
    tradedata = WriteTickMergeData(codelist,livetradedata,tradedata)   #保存实时交易数据,并与以往数据合并
    # 合并数据
    #ratiodata = StatBigTrade(codelist,bigline,livetradedata)
    #计算实时大单比例
    #实时绘图
w.stop()
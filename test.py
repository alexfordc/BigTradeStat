# conding=utf-8

from WindPy import w
from OperFunc import *
from ReadFunc import *
from WriteFunc import *
import time

f1 = open('test.txt',mode='w')
i = 1
while i > 0:
    print(i)
    print(i,file=f1)
    f1.flush()
    i += 1
    time.sleep(1)












###
#timelist = ["8:00","23:00"]
#timeinterval = 0.5
#codelist = ['RB.SHF','I.DCE','J.DCE']
##codelist = ['RB.SHF']
#bigline = 200


#olddata = ReadOldTradeInfo(codelist)    #读取之前的交易数据,{index:dataframe}

#w.start()
#while CheckTime(timelist):  #检查是否在交易时间段内
#    interval = CalcInterval(timeinterval, timelist)    #返回读取当天交易数据的时间间隔
#    time.sleep(interval)    #暂停时间间隔后再进行操作
#    tradedata = ReadTradeInfo(codelist)  #获取各品种的实时交易数据
#    WriteTick(codelist,tradedata)   #保存实时交易数据
    # 合并数据
    #ratiodata = StatBigTrade(codelist,bigline,tradedata)
    #计算实时大单比例
    #实时绘图

#w.stop()
# conding=utf-8

from WindPy import w
from OperFunc import *
from ReadFunc import *
from WriteFunc import *
import time

###
timelist = ["9:00","23:00"]
timeinterval = 1
codelist = ['RB.SHF','I.DCE','J.DCE']
#codelist = ['RB.SHF']


w.start()
while CheckTime(timelist):  #检查是否在交易时间段内
    interval = CalcInterval(timeinterval, timelist)    #返回读取当天交易数据的时间间隔
    time.sleep(interval)    #暂停时间间隔后再进行操作
    tradedata = ReadTradeInfo(codelist)  #返回列表中各品种的交易数据
    #print(tradedata)
    WriteTick(codelist,tradedata)

w.stop()
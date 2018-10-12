# conding=utf-8

from WindPy import w
from Functions import *
import time,gc

timelist = ["9:00","11:30","15:00","17:30","21:00","23:59"]
timeinterval = 0.1
codelist = ['RB.SHF','HC.SHF','I.DCE','J.DCE','JM.DCE']
#codelist = ['RB.SHF']

w.start()
while CheckTime(timelist):  #检查是否在交易时间段内
    interval = CalcInterval(timeinterval, timelist)    #返回读取当天交易数据的时间间隔
    time.sleep(interval)    #暂停时间间隔后再进行操作
    tradedata = ReadTradeInfo2(codelist)  #获取各品种的实时交易数据
    WriteTick2(codelist,tradedata)   #保存实时交易数据
    clearvalue(tradedata)
w.stop()
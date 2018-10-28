# conding=utf-8
from datetime import datetime, date, timedelta
#import xlrd,time,os, operator, calendar
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def split_big_group(dfindex, dfbig):
    vol_nature = {}
    oi_nature = {}
    big_vol_nature = {}
    big_oi_nature = {}
    for i in range(1,9):
        vol_nature[i] = 0
        oi_nature[i] = 0
        big_vol_nature[i] = 0
        big_oi_nature[i] = 0
    grouped = dfindex.groupby('rt_nature')['rt_last_vol', 'rt_oi_change'].sum()  # 根据性质分组并求和
    grouped_big = dfbig.groupby('rt_nature')['rt_last_vol', 'rt_oi_change'].sum()  # 根据性质分组并求和
    for index, row in grouped.iterrows():
        vol_nature[index] = row.rt_last_vol
        oi_nature[index] = row.rt_oi_change
    for index, row in grouped_big.iterrows():
        big_vol_nature[index] = row.rt_last_vol
        big_oi_nature[index] = row.rt_oi_change
    return (vol_nature,oi_nature,big_vol_nature,big_oi_nature)


#def sumredgreen(groupedsum):
#    vol_red = 0
#    oi_red = 0
#    vol_green = 0
#    oi_green = 0
#    for index, row in groupedsum.iterrows():
#        if (index == 2) or (index == 4) or (index == 6) or (index == 7):
#            vol_red += row.rt_last_vol
#            oi_red += row.rt_oi_change
#        elif (index == 1) or (index == 3) or (index == 5) or (index == 8):
#            vol_green += row.rt_last_vol
#            oi_green += row.rt_oi_change
#    return (vol_red,oi_red,vol_green,oi_green)
#
#
#
#
#
#
#### 检查指定的时间节点是否为偶数个、按时间先后顺序，并转换为datetime格式
#def TransTimeList(timelist):
#    nowtime = datetime.now()
#    timelist2 = []
#    if (len(timelist)%2) != 0:  #时间节点应为偶数个。起始，结束，起始，结束，……
#        print(u"时间范围首尾不配对！")
#        exit()
#    for i in range(0, len(timelist)):   #替换当前时间中的小时/分钟为指定的时间节点
#        tt = timelist[i].split(':')
#        timelist2.append(nowtime.replace(hour=int(tt[0]), minute=int(tt[1]), second=0))
#    for i in range(0,len(timelist2)-1): #时间节点应该先后顺序排列
#        if not (timelist2[i] < timelist2[i+1]):
#            print(u"时间先后顺序不对",timelist2[i],timelist2[i+1])
#            exit()
#    return timelist2
#
#### 检查当前时间是否已过当天收盘时间
#def CheckTime(timelist):
#    timelist2 = TransTimeList(timelist)
#    nowtime = datetime.now()
#    if nowtime > timelist2[-1]:     #默认时间列表中最后一个应为收盘时间点
#        print(u"现在时间%r,已过结束时间%r" % (nowtime.strftime("%H:%M:%S"),timelist2[-1].strftime("%H:%M:%S")))
#        return False
#    else:
#        return True
#
#### 计算时间间隔
#def CalcInterval(initinterval,timelist):
#    timelist2 = TransTimeList(timelist)
#    nowtime = datetime.now()
#    if nowtime < timelist2[0]:  #当前时间还未到最早开盘时间，时间间隔为两者时间差秒数与1秒的最大值。（避免差0.*秒到开盘时间，时间差秒数为0的情况）
#        print(u"尚未到开始时间，等待：",timelist2[0])
#        interval = max((timelist2[0]-nowtime).seconds,1)
#    else:
#        for i in range(0, int(len(timelist2)/2)):   #以（开始-结束）时间对为索引
#            if (timelist2[2*i] <= nowtime) and (nowtime <= timelist2[2*i+1]):   #在交易时间段内时，时间间隔为初始时间间隔
#                interval = initinterval
#                break
#            elif (timelist2[2*i+1] < nowtime) and (nowtime < timelist2[2*i+2]): #在两个交易时间段之间时，时间间隔为当前时间与后一个开盘时间的时间差秒数与1秒的最大值
#                interval = max((timelist2[2*i+2]-nowtime).seconds,1)
#                break
#    return interval
#
## 统计各品种的大单比例
#def StatBigTrade(codelist,bigline,tradedata):
#    for i in range(len(codelist)):
#        print()

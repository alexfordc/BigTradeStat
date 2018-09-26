# conding=utf-8
from WindPy import w
from datetime import datetime
import pandas as pd
import csv,os

def strlist(list):
    for i in range(len(list)):
        list[i] = str(list[i])
    return  list

def WriteTick(codelist,tradedata):
    today = datetime.now().strftime('%Y%m%d')
    for i in range(len(codelist)):
        codename = codelist[i]
        filename = codename+'_'+today+'.csv'
        if os.path.isfile(filename):
            tempfile = open(filename, 'r')
            reader = csv.reader(tempfile)
            lastline = list(reader)[-1]
            tempfile.close()
            if (lastline != strlist(tradedata[i])):
                csvfile = open(filename, 'a', newline='')
                writeCSV = csv.writer(csvfile)
                writeCSV.writerow(strlist(tradedata[i]))
                print(codelist[i],':',strlist(tradedata[i]))
                csvfile.close()
            else:
                print('重复数据:',codelist[i], ',', strlist(tradedata[i]))
        else:
            csvfile = open(filename, 'w', newline='')
            writeCSV = csv.writer(csvfile)
            writeCSV.writerow(["Date","Time","LastPX","Last_Vol","OI_Change","Nature"])
            writeCSV.writerow(strlist(tradedata[i]))
            print(codelist[i], ':', strlist(tradedata[i]))
            csvfile.close()

# 获取实时交易数据
def ReadTradeInfo(codelist):
    naturedict = {1:'空开',2:'空平',3:'空换',4:'多开',5:'多平',6:'多换',7:'双开',8:'双平'}
    tradedata = {}
    code = ','.join(codelist)
    tradeinfo = w.wsq(code, "rt_date,rt_time,rt_last,rt_last_vol,rt_oi_change,rt_nature").Data
    for i in range(len(codelist)):
        tradecode = codelist[i]
        rt_date = str(tradeinfo[0][i]).split('.')[0]
        rt_timeorigin = str(tradeinfo[1][i]).split('.')[0]
        rt_time = ("%s:%s:%s") % (rt_timeorigin[:-4],rt_timeorigin[-4:-2],rt_timeorigin[-2:])
        rt_last = tradeinfo[2][i]
        rt_last_vol = tradeinfo[3][i]
        rt_oi_change = tradeinfo[4][i]
        rt_nature = naturedict[int(tradeinfo[5][i])]
        tradedata[i] = [rt_date,rt_time,rt_last,rt_last_vol,rt_oi_change,rt_nature]
    return tradedata

### 检查指定的时间节点是否为偶数个、按时间先后顺序，并转换为datetime格式
def TransTimeList(timelist):
    nowtime = datetime.now()
    timelist2 = []
    if (len(timelist)%2) != 0:  #时间节点应为偶数个。起始，结束，起始，结束，……
        print(u"时间范围首尾不配对！")
        exit()
    for i in range(0, len(timelist)):   #替换当前时间中的小时/分钟为指定的时间节点
        tt = timelist[i].split(':')
        timelist2.append(nowtime.replace(hour=int(tt[0]), minute=int(tt[1]), second=0))
    for i in range(0,len(timelist2)-1): #时间节点应该先后顺序排列
        if not (timelist2[i] < timelist2[i+1]):
            print(u"时间先后顺序不对",timelist2[i],timelist2[i+1])
            exit()
    return timelist2

### 检查当前时间是否已过当天收盘时间
def CheckTime(timelist):
    timelist2 = TransTimeList(timelist)
    nowtime = datetime.now()
    if nowtime > timelist2[-1]:     #默认时间列表中最后一个应为收盘时间点
        print(u"现在时间%r,已过结束时间%r" % (nowtime.strftime("%H:%M:%S"),timelist2[-1].strftime("%H:%M:%S")))
        return False
    else:
        return True

### 计算时间间隔
def CalcInterval(initinterval,timelist):
    timelist2 = TransTimeList(timelist)
    nowtime = datetime.now()
    if nowtime < timelist2[0]:  #当前时间还未到最早开盘时间，时间间隔为两者时间差秒数与1秒的最大值。（避免差0.*秒到开盘时间，时间差秒数为0的情况）
        print(u"尚未到开始时间，等待：",timelist2[0])
        interval = max((timelist2[0]-nowtime).seconds,1)
    else:
        for i in range(0, int(len(timelist2)/2)):   #以（开始-结束）时间对为索引
            if (timelist2[2*i] <= nowtime) and (nowtime <= timelist2[2*i+1]):   #在交易时间段内时，时间间隔为初始时间间隔
                interval = initinterval
                break
            elif (timelist2[2*i+1] < nowtime) and (nowtime < timelist2[2*i+2]): #在两个交易时间段之间时，时间间隔为当前时间与后一个开盘时间的时间差秒数与1秒的最大值
                interval = max((timelist2[2*i+2]-nowtime).seconds,1)
                break
    return interval

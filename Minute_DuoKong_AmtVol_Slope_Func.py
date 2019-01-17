# conding=utf-8

import numpy as np
import pandas as pd
import os

def get_already_files(already_read_logfile):
    '''读取已读取的文件名称，返回为列表'''
    already_read_files = []
    if (os.path.exists(already_read_logfile)) :
        file = open(already_read_logfile,mode='r')
        lines = file.readlines()
        if len(lines) > 0:
            for item in lines:
                already_read_files.append(item.strip('\n'))
        file.close()
    return already_read_files

def get_treated_files(code, already_statminute_files, treated_path):
    '''获取尚未进行每分钟统计的文件列表，返回文件名列表'''
    allfiles = os.listdir(treated_path)
    codefiles = []
    for item in allfiles:
        if (code in item) and (item not in already_statminute_files):
            codefiles.append(item)
    codefiles = sorted(codefiles)  # 按照文件名排序
    print('#' * 100)  # 分割线
    if len(codefiles) == 0:
        print('所有%s文件均已按每分钟统计。如需重读，请更改已处理文件列表。' % (code))
    else:
        print('需统计%d个%s数据文件: %s' % (len(codefiles), code, ', '.join(codefiles)))
    return codefiles

def read_file(file_path,filename):
    '''读取原始数据文件存放路径下的数据文件。特指处理后的数据文件，各列依次为（时间,价格,价格方向,现手,成交方向,增仓,性质）'''
    dffile = open(file_path + filename)
    df = pd.read_csv(dffile, dtype={'时间':str,'价格':np.float64,'现手':np.float64,'增仓':np.float64,'持仓':np.float64,'多开':np.float64,'空平':np.float64,'空开':np.float64,'多平':np.float64,'双开':np.float64,'多换':np.float64,'双平':np.float64,'空换':np.float64,'未知':np.float64})
    dffile.close()
    return df

def get_next_time(start,interval):
    '''返回下一分钟的时间字符串，格式为00:00'''
    hour = int(start.split(':')[0])
    min = int(start.split(':')[1])
    nexthour = hour
    nextmin = min + interval
    if nextmin >= 60:
        nexthour = hour+1
        nextmin = nextmin-60
    nexttime = ('%02d:%02d' % (nexthour,nextmin))
    return nexttime

def get_minute_index(time_Series):
    '''根据时间获取各时间对应的index'''
    start_end_times = ['21:00','23:30','09:00','10:15','10:30','11:30','13:30','15:00']
    interval = 1 #间隔1分钟
    timelist = time_Series.tolist()
    minutelist = []
    minute_index = []
    for i in range(len(timelist)):
        itime = timelist[i]
        iminute = itime[:-3]
        minutelist.append(iminute)
    times = []
    for i in range(0,len(start_end_times),2):
        start = start_end_times[i]
        end = start_end_times[i+1]
        times.append(start)
        nexttime = get_next_time(start,interval)
        while (nexttime != end):
            times.append(nexttime)
            nexttime = get_next_time(nexttime, interval)
        times.append(end)
    #print(times)
    for i in range(len(times)):
        minute = times[i]
        if (minute in minutelist):
            index = minutelist.index(minute)
            minute_index.append(index)
    #print(minute_index)
    return minute_index

def minute_stat(df,minute_indexs):
    '''根据分钟时间的index，统计每分钟内的做多/做空的次数和总量'''
    for i in range(len(minute_indexs)-1):
        startindex = minute_indexs[i]
        endindex = minute_indexs[i+1]-1
        minute = df.时间[startindex][:-3]
        dfmin = df.loc[startindex:endindex,:]
        Amount_Duo = dfmin.loc[:, '多开'].sum() + dfmin.loc[:, '空平'].sum()
        Amount_Kong = dfmin.loc[:, '空开'].sum() + dfmin.loc[:, '多平'].sum()
        Count_Duo = dfmin.loc[:, '多开'][dfmin['多开'] > 0].count() + dfmin.loc[:, '空平'][dfmin['空平'] > 0].count()
        Count_Kong = dfmin.loc[:, '空开'][dfmin['空开'] > 0].count() + dfmin.loc[:, '多平'][dfmin['多平'] > 0].count()
        delta_Amount = Amount_Duo - Amount_Kong
        delta_Count = Count_Duo - Count_Kong
        #print(minute,Amount_Duo,Amount_Kong,delta_Amount,Count_Duo,Count_Kong,delta_Count)
        return (minute,Amount_Duo,Amount_Kong,delta_Amount,Count_Duo,Count_Kong,delta_Count)

def later_minute_stat(df,minute_indexs,timelength):
    '''根据分钟时间的index，统计每分钟过后几分钟内的每分钟价格变化'''
    for i in range(len(minute_indexs)-1):
        startindex = minute_indexs[i]
        endindex = minute_indexs[i+1]-1
        minute = df.时间[startindex][:-3]
        dfmin = df.loc[startindex:endindex,:]
        price = dfmin.价格.tolist()
        indexlist = range(1,len(price)+1)
        print(np.polyfit(indexlist,price,1))

    print()
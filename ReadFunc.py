# conding=utf-8
from WindPy import w
from datetime import datetime
import pandas as pd
import numpy as np
import os

#class tradedata:
#    def __init__(self,tradecode,rt_date,rt_time,rt_last,rt_last_vol,rt_oi_change,rt_nature):
#        self.name = tradecode
#        self.date = rt_date
#        self.time = rt_time
#        self.price = rt_last
#        self.pos = rt_last_vol
#        self.change = rt_oi_change
#        self.nature = rt_nature

# 获取实时交易数据
#def ReadTradeInfo(codelist):
#    naturedict = {1:'空开',2:'空平',3:'空换',4:'多开',5:'多平',6:'多换',7:'双开',8:'双平'}
#    tradedata = {}
#    code = ','.join(codelist)
#    tradeinfo = w.wsq(code, "rt_date,rt_time,rt_last,rt_last_vol,rt_oi_change,rt_nature").Data
#    for i in range(len(codelist)):
#        tradecode = codelist[i]
#        rt_date = str(tradeinfo[0][i]).split('.')[0]
#        rt_timeorigin = str(tradeinfo[1][i]).split('.')[0]
#        rt_time = ("%s:%s:%s") % (rt_timeorigin[:-4],rt_timeorigin[-4:-2],rt_timeorigin[-2:])
#        rt_last = tradeinfo[2][i]
#        rt_last_vol = tradeinfo[3][i]
#        rt_oi_change = tradeinfo[4][i]
#        rt_nature = naturedict[int(tradeinfo[5][i])]
#        tradedata[i] = [rt_date,rt_time,rt_last,rt_last_vol,rt_oi_change,rt_nature]
#    return tradedata

# 从csv文件读取以往交易数据
def ReadTradeInfo(code):
    #nowmon = datetime.now().strftime('%Y%m')
    #获取各品种以往数据的文件名
    allfiles = os.listdir()
    codefiles = []
    oldtradeinfo = pd.DataFrame
    for item in allfiles:
        if (item.split('.')[-1] == 'csv'):
                if code in item:
                    codefiles.append(item)
    codefiles = sorted(codefiles)
    # 读取各品种以往数据
    datalist = []
    for j in range(len(codefiles)):
        data = pd.read_csv(codefiles[j],encoding='gb2312',dtype={'code':str,'rt_date':str,'rt_time':str,'rt_last':np.int32,'rt_last_vol':np.int32,'rt_oi_change':np.int32,'rt_nature':np.int32})
        datalist.append(data)
    if datalist:
        oldtradeinfo = pd.concat(datalist,ignore_index=True) #合并为一个dataframe
    return (oldtradeinfo)

### 根据code名称获取csv文件列表，并区分以往文件和实时文件
def get_files(code):
    now = datetime.now().strftime('%Y%m%d')
    allfiles = os.listdir()
    codefiles = []
    livefile = ''
    index = -2
    for item in allfiles:
        if (item.split('.')[-1] == 'csv'):
                if code in item:
                    codefiles.append(item)
    oldfiles = sorted(codefiles)
    for i in range(len(oldfiles)):
        if now in oldfiles[i]:
            index = i
    if index == -2:
        index = -1
    livefile = oldfiles[index]
    oldfiles.remove(livefile)
    return (oldfiles,livefile)

def read_old_files(oldfiles):
    dflist = []
    olddf = pd.DataFrame
    if len(oldfiles) > 0:
        for i in range(len(oldfiles)):
            df = pd.read_csv(oldfiles[i], encoding='gb2312',
                               dtype={'code': str, 'rt_date': str, 'rt_time': str, 'rt_last': np.int32,
                                      'rt_last_vol': np.int32, 'rt_oi_change': np.int32, 'rt_nature': np.int32})
            dflist.append(df)
        if len(dflist) > 0:
            olddf = pd.concat(dflist, ignore_index=True)
    return olddf

def read_live_file(livefile,num):
    templine = []
    for i in range(1, num + 1):
        templine.append(i)
    livedf = pd.read_csv(livefile, encoding='gb2312',skiprows=tuple(templine),
                               dtype={'code': str, 'rt_date': str, 'rt_time': str, 'rt_last': np.int32,
                                      'rt_last_vol': np.int32, 'rt_oi_change': np.int32, 'rt_nature': np.int32})
    return livedf
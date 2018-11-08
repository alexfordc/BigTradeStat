# conding=utf-8
import os
from datetime import datetime,timedelta
import pandas as pd
import numpy as np

def get_filelist(code):
    allfiles = os.listdir()
    codefiles = []
    for item in allfiles:
        if (item.split('.')[-1] == 'csv'):
                if code in item:
                    codefiles.append(item)
    codefiles = sorted(codefiles)
    print('文件列表: %s' % (', '.join(codefiles)))
    return codefiles

def get_yesterday(dfdate):
    today = datetime.strptime(dfdate,'%Y%m%d')
    yesterday = (today - timedelta(days=1)).strftime('%Y%m%d')
    return yesterday

def read_file(datafile):
    dfdate = datafile.split('_')[1].split('.')[0]
    yesterday = get_yesterday(dfdate)
    df = pd.read_csv(datafile, encoding='gb2312', usecols=(0, 1, 3, 5, 6),
                     dtype={'时间': str, '价格': np.int32, '现手': np.int32, '增仓': np.int32,
                            '性质': str})
    print('读取文件%r,共%d行' % (datafile, len(df.index)))
    return df

def classify_by_nature(df):
    print()

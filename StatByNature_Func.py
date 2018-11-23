# conding=utf-8
import os,sys
from datetime import datetime,timedelta
import pandas as pd
import numpy as np

def report_progress(progress, total, start, end):
    ratio = progress / float(total)
    percentage = round(ratio * 100)
    length = 80
    percentnums = round(length*ratio)
    sec = (end-start).seconds
    buf = '\r[%s%s] %d%% (%d Seconds)' % (('#'*percentnums),('-'*(length-percentnums)), percentage,sec)
    sys.stdout.write(buf)
    sys.stdout.flush()
def report_progress_done():
    sys.stdout.write('\n')

def read_al_files():
    al_files = 'Already_read_files.txt'
    al_lists = []
    if (os.path.exists(al_files)) :
        file = open(al_files,mode='r')
        lines = file.readlines()
        if len(lines) > 0:
            for item in lines:
                al_lists.append(item.strip('\n'))
        file.close()
    return al_lists

def update(al_lists):
    al_files = 'Already_read_files.txt'
    if len(al_lists) > 0:
        file = open(al_files, mode='w')
        for item in al_lists:
            print('%s' % item,file=file)
        file.close()


def get_filelist(al_lists,code):
    allfiles = os.listdir()
    codefiles = []
    for item in allfiles:
        if (item.split('.')[-1] == 'csv'):
                if (code in item) and (item not in al_lists):
                    codefiles.append(item)
    codefiles = sorted(codefiles)
    if len(codefiles) == 0:
        print('所有文件均早已读取。如需重读，请更改已读文件列表文件。')
        #exit()
    else:
        print('%d个文件: %s' % (len(codefiles),', '.join(codefiles)))
    return codefiles

def get_classify_files(code):
    allfiles = os.listdir('Classify_Data/')
    codefiles = []
    for item in allfiles:
        if (code in item):
            codefiles.append(item)
    codefiles = sorted(codefiles)
    if len(codefiles) == 0:
        print('没有已经按性质分列处理的%s文件' % code)
        exit()
    else:
        print('%d个文件: %s' % (len(codefiles), ', '.join(codefiles)))
    return codefiles

def get_yesterday(dfdate):
    today = datetime.strptime(dfdate,'%Y%m%d')
    yesterday = (today - timedelta(days=1)).strftime('%Y%m%d')
    return yesterday

def read_file(i,al_lists,datafile):
    dfdate = datafile.split('_')[1].split('.')[0]
    yesterday = get_yesterday(dfdate)
    df = pd.read_csv(datafile, encoding='gb2312', usecols=(0, 1, 3, 5, 6),
                 dtype={'时间': str, '价格': np.int32, '现手': np.int32, '增仓': np.int32,
                        '性质': str})#,nrows=5)
    print('读取第%d个文件%r,添加日期，共%d行' % (i+1,datafile, len(df.index)))
    df.insert(0,'天数',i+1)
    start = datetime.now()
    for index, row in df.iterrows():
        if datetime.strptime(row.时间, '%H:%M:%S') > datetime.strptime('20:00:00', '%H:%M:%S'):
            df.iloc[index, 1] = yesterday + '_' + row.时间
        else:
            df.iloc[index, 1] = dfdate + '_' + row.时间
        end = datetime.now()
        report_progress(index, len(df.index), start, end)
    report_progress_done()
    al_lists.append(datafile)
    update(al_lists)
    return df

def getdate(datafile):
    filedate = datafile.split('_')[1].split('.')[0]
    fdate = filedate[:4] + '-' + filedate[4:6] + '-' + filedate[6:]
    return (fdate)

def classify_by_nature(pre_oi,df):
    naturelist = ['多开', '空平', '空开', '多平', '双开', '多换', '双平', '空换']
    classify_df = df.loc[:, ['天数', '时间', '价格', '现手', '增仓']]
    classify_df.insert(4, '总量', 0)
    classify_df.insert(6, '持仓', 0)
    #vol_nature = {}
    #for i in range(len(naturelist)):
    #    vol_nature[naturelist[i]] = 0
    nature_index = {}
    for i in range(len(naturelist)):
        classify_df.insert(i+7,naturelist[i],0)
        nature_index[naturelist[i]] = i+7
    print('按性质分列、求和')
    start = datetime.now()
    for index, row in df.iterrows():
        df_i = df[:index + 1]
        total_vol_i = df_i.iloc[:,3].sum()
        total_oi_i = df_i.iloc[:,4].sum()
        classify_df.iloc[index, 4] = total_vol_i
        classify_df.iloc[index, 6] = total_oi_i + pre_oi
        #vol_nature[row.性质] += row.现手
        #classify_df.iloc[index, nature_index[row.性质]] = vol_nature[row.性质]
        classify_df.iloc[index, nature_index[row.性质]] = row.现手
        end = datetime.now()
        report_progress(index, len(df.index), start, end)
    report_progress_done()
    #pd.set_option('display.max_columns', None)
    #pd.set_option('max_colwidth', 100)
    #print(classify_df)

    return (classify_df)

def saveCSV(datafile,classify_df,classify_path):
    filename = classify_path + datafile.strip('.csv') + '_classified.csv'
    classify_df.to_csv(filename,index=0,encoding='gb2312')
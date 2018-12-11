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
    buf = '\r[%s%s] %d%% (%d Seconds)' % (('>'*percentnums),('-'*(length-percentnums)), percentage,sec)
    sys.stdout.write(buf)
    sys.stdout.flush()
def report_progress_done():
    sys.stdout.write('\n')

def read_al_files():
    al_files = 'Already_Read_duokong_VS_price_files.txt'
    al_lists = []
    if (os.path.exists(al_files)) :
        file = open(al_files,mode='r')
        lines = file.readlines()
        if len(lines) > 0:
            for item in lines:
                al_lists.append(item.strip('\n'))
        file.close()
    return al_lists

def update_al_list(al_lists):
    al_files = 'Already_Read_duokong_VS_price_files.txt'
    al_lists = sorted(al_lists)
    if len(al_lists) > 0:
        file = open(al_files, mode='w')
        for item in al_lists:
            print('%s' % item,file=file)
        file.close()

def update_big_list(code,classify_datafile):
    big_lists = []
    big_file = code + '_Already_big'+'.txt'
    if (os.path.exists(big_file)):
        file = open(big_file, mode='r')
        lines = file.readlines()
        if len(lines) > 0:
            for item in lines:
                big_lists.append(item.strip('\n'))
        file.close()
        if classify_datafile not in big_lists:
            file = open(big_file, mode='a')
            print('%s' % classify_datafile,file=file)
            file.close()
    else:
        file = open(big_file, mode='w')
        print('%s' % classify_datafile, file=file)
        file.close()


def get_filelist(origin_path,al_lists,code):
    allfiles = os.listdir(origin_path)
    codefiles = []
    for item in allfiles:
        if (item.split('.')[-1] == 'csv'):
                if (code in item) and (item not in al_lists):
                    codefiles.append(item)
    codefiles = sorted(codefiles)
    print('#'*50)
    if len(codefiles) == 0:
        print('所有%s文件均已读取。如需重读，请更改已读文件列表文件。' % code)
    else:
        print('需读取%d个%s原始数据文件: %s' % (len(codefiles),code,', '.join(codefiles)))
    return codefiles

def get_classify_files(code,classify_path):
    allfiles = os.listdir(classify_path)
    big_file = code + '_Already_big'+'.txt'
    codefiles = []
    albig_lists = []
    #获取已经大单处理过的文件列表
    if (os.path.exists(big_file)):
        file = open(big_file, mode='r')
        lines = file.readlines()
        if len(lines) > 0:
            for item in lines:
                albig_lists.append(item.strip('\n'))
        file.close()
    # 遍历所有文件，检查code及是否已处理过
    for item in allfiles:
        if (code in item) and (item not in albig_lists):
            codefiles.append(item)
    codefiles = sorted(codefiles)
    if len(codefiles) == 0:
        print('没有需要统计大单数据的%s文件' % code)
        #exit()
    else:
        #print('%d个%s文件需统计大单数据: %s' % (len(codefiles),code,', '.join(codefiles)))
        print('%d个%s文件需统计大单数据' % (len(codefiles),code))
    return codefiles

def get_yesterday(dfdate):
    today = datetime.strptime(dfdate,'%Y%m%d')
    yesterday = (today - timedelta(days=1)).strftime('%Y%m%d')
    return yesterday

def read_file(i,origin_path,al_lists,datafile):
    dfdate = datafile.split('_')[1].split('.')[0]
    yesterday = get_yesterday(dfdate)
    dffile = open(origin_path + datafile)
    df = pd.read_csv(dffile, usecols=(0, 1, 3, 5, 6),
                 dtype={'时间': str, '价格': np.float64, '现手': np.float64, '增仓': np.float64,
                        '性质': str})#,nrows=5)
    #print('读取第%d个文件%r,添加日期，共%d行' % (i+1,datafile, len(df.index)))
    #df.insert(0,'天数',len(al_lists)+i+1)
    #start = datetime.now()
    #for index, row in df.iterrows():
    #    if datetime.strptime(row.时间, '%H:%M:%S') > datetime.strptime('20:00:00', '%H:%M:%S'):
    #        df.iloc[index, 1] = yesterday + '_' + row.时间
    #    else:
    #        df.iloc[index, 1] = dfdate + '_' + row.时间
    #    end = datetime.now()
    #    report_progress(index, len(df.index), start, end)
    #report_progress_done()
    al_lists.append(datafile)
    update_al_list(al_lists)
    return df

def get_open_close_px(df):
    return (df.iloc[1], df.iloc[df.index[-1]])


def getdate(datafile):
    filedate = datafile.split('_')[1].split('.')[0]
    fdate = filedate[:4] + '-' + filedate[4:6] + '-' + filedate[6:]
    return (fdate)

def classify_by_nature(df):
    naturelist = ['多开', '空平', '空开', '多平', '双开', '多换', '双平', '空换']
    classify_df = df.loc[:, ['时间', '价格', '现手', '增仓']]
    nature_index = {}
    for i in range(len(naturelist)):
        classify_df.insert(i+4,naturelist[i],0)
        nature_index[naturelist[i]] = i+4
    start = datetime.now()
    for index, row in df.iterrows():
        classify_df.iloc[index, nature_index[row.性质]] = row.现手
        end = datetime.now()
        report_progress(index, len(df.index), start, end)
    report_progress_done()
    #pd.set_option('display.max_columns', None)
    #pd.set_option('max_colwidth', 100)
    #print(classify_df)

    return (classify_df)

def sum_count_df(df):
    total_duo = int(df.loc[:, '多开'].sum() + df.loc[:, '空平'].sum())
    total_kong = int(df.loc[:, '空开'].sum() + df.loc[:, '多平'].sum())
    count_duo = int(len(df[(df['多开'] > 0) | (df['空平'] > 0)].index))
    count_kong = int(len(df[(df['空开'] > 0) | (df['多平'] > 0)].index))
    return (total_duo,count_duo,total_kong,count_kong)

def add_cols(index,stas_df,total_duo,count_duo,total_kong,count_kong,big_total_duo,big_count_duo,big_total_kong,big_count_kong):
    stas_df.loc[index, '累计做多'] = total_duo
    stas_df.loc[index, '做多次数'] = count_duo
    stas_df.loc[index, '累计大单做多'] = big_total_duo
    stas_df.loc[index, '大单做多次数'] = big_count_duo
    stas_df.loc[index, '累计做空'] = total_kong
    stas_df.loc[index, '做空次数'] = count_kong
    stas_df.loc[index, '累计大单做空'] = big_total_kong
    stas_df.loc[index, '大单做空次数'] = big_count_kong
    return stas_df

def save_classify_CSV(datafile,classify_df,classify_path):
    filename = classify_path + datafile.strip('.csv') + '_classified_noVol.csv'
    classify_df.to_csv(filename,index=0,encoding='gb2312')

def save_big_CSV(classify_datafile, stas_df, big_path,bigline):
    filename = big_path + classify_datafile.strip('.csv') + '_big' + str(bigline) +'.csv'
    stas_df.to_csv(filename,index=0,encoding='gb2312')

def merge_big_files(code,big_path,bigline):
    allfiles = os.listdir(big_path)
    codefiles = []
    dflist = []
    datelist = []
    for item in allfiles:
        if (code in item):
            codefiles.append(item)
    codefiles = sorted(codefiles)
    if len(codefiles) == 0:
        print('没有合并的%s大单文件' % code)
        exit()
    else:
        print('%d个%s大单文件待合并' % (len(codefiles),code))
        for i in range(len(codefiles)):
            datelist.append(codefiles[i].split('_')[1])
            filename = big_path + codefiles[i]
            df = pd.read_csv(filename, encoding='gb2312')
            dflist.append(df)
        if len(dflist) > 0:
            datelist = sorted(datelist)
            alldf = pd.concat(dflist, ignore_index=True)
            #alldfname = code + '_' + datelist[0] + '-' + datelist[-1] + '_big' + str(bigline) + '.txt'
            alldfname = code + '_big' + str(bigline) + '.txt'
            alldf.to_csv(alldfname, index=0, encoding='gb2312')
            print('合并后的文件保存为%s' % alldfname)


def save_Excel(filename,stat_df):
    if (os.path.exists(filename)):
        old_df = pd.read_excel(filename)
        df = pd.concat([old_df,stat_df], ignore_index=True)
        df.to_excel(filename, index=False, encoding='gb2312')
        print('每日大单统计数据写入文件 %s Sheet1子表' % filename)
    else:
        stat_df.to_excel(filename, index=False, encoding='gb2312')
        print('每日大单统计数据写入文件 %s Sheet1子表' % filename)


def calc_correlation(code,biglines,filename):
    df = pd.read_excel(filename)
    corr_df = pd.DataFrame(columns=['多空总量比','价格涨跌','价格涨跌百分比',' ','多空分类比','价格涨跌_','价格涨跌百分比_'])
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer,sheet_name='Sheet1', index=False, encoding='gb2312')
    for i in range(len(biglines)):
        bigline = biglines[i]
        df2 = pd.DataFrame(df,columns=['价格涨跌','价格涨跌百分比',str(bigline)+'多空总量比差',str(bigline)+'多空分类比差'])
        corr_df.loc[i,'多空总量比'] = bigline
        corr_df.loc[i,'价格涨跌'] = df2.corr().loc['价格涨跌',str(bigline)+'多空总量比差']
        corr_df.loc[i,'价格涨跌百分比'] = df2.corr().loc['价格涨跌百分比',str(bigline)+'多空总量比差']
        corr_df.loc[i,'多空分类比'] = bigline
        corr_df.loc[i,'价格涨跌_'] = df2.corr().loc['价格涨跌',str(bigline)+'多空分类比差']
        corr_df.loc[i,'价格涨跌百分比_'] = df2.corr().loc['价格涨跌百分比',str(bigline)+'多空分类比差']
    corr_df.to_excel(writer,sheet_name='相关性分析', index=False, encoding='gb2312')
    writer.save()
    print('相关性分析写入文件 %s 相关性分析子表' % filename)

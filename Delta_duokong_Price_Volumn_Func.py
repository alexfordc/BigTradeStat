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

def get_datafiles(origin_path,already_read_files,code):
    '''获取原始数据文件路径中的所有文件名列表，根据各文件名中是否包含code、文件名是否在已读文件列表中，获取未读取的文件列表'''
    allfiles = os.listdir(origin_path)
    codefiles = []
    for item in allfiles:
        if (code in item) and (item not in already_read_files):
            codefiles.append(item)
    codefiles = sorted(codefiles)   #按照文件名排序
    print('#'*100)   #分割线
    if len(codefiles) == 0:
        print('所有%s文件均已读取。如需重读，请更改已读文件列表%s。' % (code,already_read_files))
    else:
        print('需读取%d个%s原始数据文件: %s' % (len(codefiles),code,', '.join(codefiles)))
    return codefiles

def getdate(datafile):
    '''根据原始数据文件名，获取其对应的日期，返回yyyymmdd形式的字符'''
    filedate = datafile.split('_')[1].split('.')[0]
    fdate = filedate[:4] + '-' + filedate[4:6] + '-' + filedate[6:]
    return (fdate)

def read_datafile(origin_path,datafile):
    '''读取原始数据文件存放路径下的数据文件'''
    dffile = open(origin_path + datafile)
    df = pd.read_csv(dffile,usecols=(0,1,3,5,6),dtype={'时间':str,'价格':np.float64,'现手':np.float64,'增仓':np.float64,'性质':str})
    dffile.close()
    return df

def volumn_classify(pre_oi,df):
    '''增加持仓数据列，持仓量为前一日收盘持仓量+累计增仓量。按性质将现手数据分列，未知表示性质不明或空白时的情况'''
    naturelist = ['多开', '空平', '空开', '多平', '双开', '多换', '双平', '空换','未知']
    keeplist = ['时间', '价格', '现手', '增仓']
    treated_df = df.loc[:, keeplist]
    treated_df.insert(len(keeplist), '持仓', 0)
    nature_index = {}
    for i in range(len(naturelist)):
        treated_df.insert(i+5,naturelist[i],0)
        nature_index[naturelist[i]] = i+5
    start = datetime.now()
    for index, row in df.iterrows():
        df_i = df[:index + 1]
        total_oi_i = df_i.loc[:,'增仓'].sum()
        treated_df.loc[index, '持仓'] = total_oi_i + pre_oi
        treated_df.iloc[index, nature_index[row.性质]] = row.现手
        end = datetime.now()
        report_progress(index, len(df.index), start, end)
    report_progress_done()
    return (treated_df)

def update_listfile(already_read_logfile,datafile):
    '''在已读取文件的文件中加入datafile的文件名。若已存在已读取文件，且datafile不在其中，追加datafile文件名；若不存在，则新建并写入datafile文件名'''
    filelist = []
    if (os.path.exists(already_read_logfile)):
        logfile = open(already_read_logfile, mode='r')
        lines = logfile.readlines()
        if len(lines) > 0:
            for item in lines:
                filelist.append(item.strip('\n'))
        logfile.close()
    if (datafile not in filelist):
        filelist.append(datafile)
    filelist = sorted(filelist)
    logfile = open(already_read_logfile, mode='w')
    for i in range(len(filelist)):
        filename = filelist[i]
        print('%s' % filename, file=logfile)
    logfile.close()







#def update_al_list(al_lists):
#    al_files = 'Already_Read_duokong_VS_price_files.txt'
#    al_lists = sorted(al_lists)
#    if len(al_lists) > 0:
#        file = open(al_files, mode='w')
#        for item in al_lists:
#            print('%s' % item,file=file)
#        file.close()
#
#def update_big_list(code,classify_datafile):
#    big_lists = []
#    big_file = code + '_Already_big'+'.txt'
#    if (os.path.exists(big_file)):
#        file = open(big_file, mode='r')
#        lines = file.readlines()
#        if len(lines) > 0:
#            for item in lines:
#                big_lists.append(item.strip('\n'))
#        file.close()
#        if classify_datafile not in big_lists:
#            file = open(big_file, mode='a')
#            print('%s' % classify_datafile,file=file)
#            file.close()
#    else:
#        file = open(big_file, mode='w')
#        print('%s' % classify_datafile, file=file)
#        file.close()
#
#
#def get_classify_files(code,classify_path):
#    allfiles = os.listdir(classify_path)
#    big_file = code + '_Already_big'+'.txt'
#    codefiles = []
#    albig_lists = []
#    #获取已经大单处理过的文件列表
#    if (os.path.exists(big_file)):
#        file = open(big_file, mode='r')
#        lines = file.readlines()
#        if len(lines) > 0:
#            for item in lines:
#                albig_lists.append(item.strip('\n'))
#        file.close()
#    # 遍历所有文件，检查code及是否已处理过
#    for item in allfiles:
#        if (code in item) and (item not in albig_lists):
#            codefiles.append(item)
#    codefiles = sorted(codefiles)
#    if len(codefiles) == 0:
#        print('没有需要统计大单数据的%s文件' % code)
#        #exit()
#    else:
#        #print('%d个%s文件需统计大单数据: %s' % (len(codefiles),code,', '.join(codefiles)))
#        print('%d个%s文件需统计大单数据' % (len(codefiles),code))
#    return codefiles
#
#def get_yesterday(dfdate):
#    today = datetime.strptime(dfdate,'%Y%m%d')
#    yesterday = (today - timedelta(days=1)).strftime('%Y%m%d')
#    return yesterday
#

#def get_open_close_px(df):
#    return (df.iloc[1], df.iloc[df.index[-1]])
#
#
#def getdate(datafile):
#    filedate = datafile.split('_')[1].split('.')[0]
#    fdate = filedate[:4] + '-' + filedate[4:6] + '-' + filedate[6:]
#    return (fdate)
#
#def classify_by_nature(df):
#    naturelist = ['多开', '空平', '空开', '多平', '双开', '多换', '双平', '空换']
#    treated_df = df.loc[:, ['时间', '价格', '现手', '增仓']]
#    nature_index = {}
#    for i in range(len(naturelist)):
#        treated_df.insert(i+4,naturelist[i],0)
#        nature_index[naturelist[i]] = i+4
#    start = datetime.now()
#    for index, row in df.iterrows():
#        treated_df.iloc[index, nature_index[row.性质]] = row.现手
#        end = datetime.now()
#        report_progress(index, len(df.index), start, end)
#    report_progress_done()
#    #pd.set_option('display.max_columns', None)
#    #pd.set_option('max_colwidth', 100)
#    #print(treated_df)
#
#    return (treated_df)
#
#def sum_count_df(df):
#    total_duo = int(df.loc[:, '多开'].sum() + df.loc[:, '空平'].sum())
#    total_kong = int(df.loc[:, '空开'].sum() + df.loc[:, '多平'].sum())
#    count_duo = int(len(df[(df['多开'] > 0) | (df['空平'] > 0)].index))
#    count_kong = int(len(df[(df['空开'] > 0) | (df['多平'] > 0)].index))
#    return (total_duo,count_duo,total_kong,count_kong)
#
#def add_cols(index,stas_df,total_duo,count_duo,total_kong,count_kong,big_total_duo,big_count_duo,big_total_kong,big_count_kong):
#    stas_df.loc[index, '累计做多'] = total_duo
#    stas_df.loc[index, '做多次数'] = count_duo
#    stas_df.loc[index, '累计大单做多'] = big_total_duo
#    stas_df.loc[index, '大单做多次数'] = big_count_duo
#    stas_df.loc[index, '累计做空'] = total_kong
#    stas_df.loc[index, '做空次数'] = count_kong
#    stas_df.loc[index, '累计大单做空'] = big_total_kong
#    stas_df.loc[index, '大单做空次数'] = big_count_kong
#    return stas_df
#
def save_treated_csv(datafile,treated_df,treated_path):
    filename = treated_path + datafile.strip('.csv') + '_Volumn_Classify.csv'
    treated_df.to_csv(filename,index=0,encoding='gb2312')
#
#def save_big_CSV(classify_datafile, stas_df, big_path,bigline):
#    filename = big_path + classify_datafile.strip('.csv') + '_big' + str(bigline) +'.csv'
#    stas_df.to_csv(filename,index=0,encoding='gb2312')
#
#def merge_big_files(code,big_path,bigline):
#    allfiles = os.listdir(big_path)
#    codefiles = []
#    dflist = []
#    datelist = []
#    for item in allfiles:
#        if (code in item):
#            codefiles.append(item)
#    codefiles = sorted(codefiles)
#    if len(codefiles) == 0:
#        print('没有合并的%s大单文件' % code)
#        exit()
#    else:
#        print('%d个%s大单文件待合并' % (len(codefiles),code))
#        for i in range(len(codefiles)):
#            datelist.append(codefiles[i].split('_')[1])
#            filename = big_path + codefiles[i]
#            df = pd.read_csv(filename, encoding='gb2312')
#            dflist.append(df)
#        if len(dflist) > 0:
#            datelist = sorted(datelist)
#            alldf = pd.concat(dflist, ignore_index=True)
#            #alldfname = code + '_' + datelist[0] + '-' + datelist[-1] + '_big' + str(bigline) + '.txt'
#            alldfname = code + '_big' + str(bigline) + '.txt'
#            alldf.to_csv(alldfname, index=0, encoding='gb2312')
#            print('合并后的文件保存为%s' % alldfname)
#
#
#def save_Excel(filename,stat_df):
#    if (os.path.exists(filename)):
#        old_df = pd.read_excel(filename)
#        df = pd.concat([old_df,stat_df], ignore_index=True)
#        df.to_excel(filename, index=False, encoding='gb2312')
#        print('每日大单统计数据写入文件 %s Sheet1子表' % filename)
#    else:
#        stat_df.to_excel(filename, index=False, encoding='gb2312')
#        print('每日大单统计数据写入文件 %s Sheet1子表' % filename)
#
#
#def calc_correlation(code,biglines,filename):
#    df = pd.read_excel(filename)
#    corr_df = pd.DataFrame(columns=['多空总量比','价格涨跌','价格涨跌百分比',' ','多空分类比','价格涨跌_','价格涨跌百分比_'])
#    writer = pd.ExcelWriter(filename)
#    df.to_excel(writer,sheet_name='Sheet1', index=False, encoding='gb2312')
#    for i in range(len(biglines)):
#        bigline = biglines[i]
#        df2 = pd.DataFrame(df,columns=['价格涨跌','价格涨跌百分比',str(bigline)+'多空总量比差',str(bigline)+'多空分类比差'])
#        corr_df.loc[i,'多空总量比'] = bigline
#        corr_df.loc[i,'价格涨跌'] = df2.corr().loc['价格涨跌',str(bigline)+'多空总量比差']
#        corr_df.loc[i,'价格涨跌百分比'] = df2.corr().loc['价格涨跌百分比',str(bigline)+'多空总量比差']
#        corr_df.loc[i,'多空分类比'] = bigline
#        corr_df.loc[i,'价格涨跌_'] = df2.corr().loc['价格涨跌',str(bigline)+'多空分类比差']
#        corr_df.loc[i,'价格涨跌百分比_'] = df2.corr().loc['价格涨跌百分比',str(bigline)+'多空分类比差']
#    corr_df.to_excel(writer,sheet_name='相关性分析', index=False, encoding='gb2312')
#    writer.save()
#    print('相关性分析写入文件 %s 相关性分析子表' % filename)
#    print('-' * 50)
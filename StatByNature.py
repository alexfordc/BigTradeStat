# conding=utf-8
'''
读取多个数据文件（由Wind直接导出的成交明细）
红: {2:'空平',4:'多开',6:'多换',7:'双开'}
绿: {1:'空开',3:'空换',5:'多平',8:'双平'}
'''
from WindPy import w
from StatByNature_Func import *
import time
import numpy as np
import matplotlib.pyplot as plt

#####################
#codelist = ['RB.SHF','I.DCE','J.DCE']
code = 'RB.SHF'
bigline = 1000     #手动指定大单标准线
#biglines = [1000]
#bigline = [x for x in range(0,500,100)]    #等差列表产生一系列大单标准线

al_lists = read_al_files()
al_lists = []

### 处理原始数据 ###
datafiles = get_filelist(al_lists,code)
if len(datafiles) > 0:
    w.start()
    for i in range(len(datafiles)):
        datafile = datafiles[i]
        df = read_file(i,al_lists,datafile)
        pre_oi = w.wsd(code,'oi',"ED-1TD",getdate(datafile),'').Data[0][0]
        classify_df = classify_by_nature(pre_oi,df)
        saveCSV(datafile,classify_df)

### 根据大单线整理数据 ###
#classify_datafiles = get_classify_files(code)
#for i in range(len(classify_datafiles)):
#    classify_datafile = classify_datafiles[i]
#    df = pd.read_csv(classify_datafile, encoding='gb2312', usecols=(0,1,2,3,5,6,7,8,9,10),dtype={'天数': int,'时间': str,'价格': np.int32,'现手': np.int32,'增仓': np.int32,'持仓': np.int32,'多开': np.int32,'空平': np.int32,'空开': np.int32,'多平': np.int32})  # ,nrows=5)


#today = datetime.now().strftime('%Y%m%d')
#filename = 'test_' + today + '.csv'

#outfile = open(filename, mode='w')
#output_title(outfile)
#
#start = datetime.now()
#print('开始：',start.strftime('%Y-%m-%d %H:%M:%S'))
#dfs = read_files(datafiles)
#stat_file = stat_data(dfs,bigline)
stat_file = 'Stated_Records_20181108_1000.csv'
#plot_data(stat_file)

#for i in range(len(biglines)):
#    bigline = biglines[i]

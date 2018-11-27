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

pd.set_option('display.max_columns', None)

#####################
#codelist = ['RB.SHF','I.DCE','J.DCE']
code = 'RB.SHF'
bigline = 1000     #手动指定大单标准线
classify_path = 'Classify_Data/'    #保存按性质分类的每天数据的路径
big_path = 'BigTrade/'      #保存按性质分类、大单线累积统计的数据的路径
#biglines = [1000]
#bigline = [x for x in range(0,500,100)]    #等差列表产生一系列大单标准线

al_lists = read_al_files()      #读取“已经读取过”的文件清单
#al_lists = []

### 处理原始数据 ###
datafiles = get_filelist(al_lists,code) #根据code名称获取没有读取过的文件清单
if len(datafiles) > 0:
    w.start()
    for i in range(len(datafiles)):
        datafile = datafiles[i]
        df = read_file(i,al_lists,datafile) #读取文件，同时更新“已读取文件清单”
        pre_oi = w.wsd(code,'oi',"ED-1TD",getdate(datafile),'').Data[0][0]  #获取数据前一天的持仓量
        classify_df = classify_by_nature(pre_oi,df)     #按性质分类数据。主要加入实时总交易量、持仓量，将现手按性质分列输出
        save_classify_CSV(datafile,classify_df,classify_path)     #保存性质分列数据到指定路径
    #w.stop()

### 根据大单线整理数据 ###
classify_datafiles = get_classify_files(code,classify_path)     #从指定路径获取分类数据的文件清单
for i in range(len(classify_datafiles)):
    classify_datafile = classify_datafiles[i]
    df = pd.read_csv(classify_path+classify_datafile, encoding='gb2312', usecols=(0,1,2,3,5,6,7,8,9,10),dtype={'天数': int,'时间': str,'价格': np.int32,'现手': np.int32,'增仓': np.int32,'持仓': np.int32,'多开': np.int32,'空平': np.int32,'空开': np.int32,'多平': np.int32})  # ,nrows=5)  # 仅读取按性质分列数据中的天数、时间、价格、现手、增仓、持仓、多开、空平、空开、多平10列的数据
    dfbig = df[df['现手'] >= bigline]     #根据大单线读取大单数据
    stas_df = df.loc[:,'天数':'持仓']
    start = datetime.now()
    print('%s统计大单,大单线%d:' % (classify_datafile,bigline))
    for index, row in df.iterrows():
        df_i = df.loc[:index]
        dfbig_i = dfbig.loc[:index]
        total_duo, count_duo, total_kong, count_kong = sum_count_df(df_i)
        big_total_duo, big_count_duo, big_total_kong, big_count_kong = sum_count_df(dfbig_i)
        stas_df = add_cols(index,stas_df,total_duo,count_duo,total_kong,count_kong,big_total_duo,big_count_duo,big_total_kong,big_count_kong)
        end = datetime.now()
        report_progress(index, len(df.index), start, end)
    report_progress_done()
    save_big_CSV(classify_datafile, stas_df, big_path,bigline)

merge_big_files(code,big_path)



#    df = pd.read_csv(classify_path+classify_datafile, encoding='gb2312', usecols=(1,5),dtype={'天数': int,'增仓':np.int32})  # ,nrows=5)
#    datetimelist = df['时间'].tolist()
#    x1ticks = list(range(0, len(datetimelist), int(len(datetimelist) / 20)))
#    x1labels = [datetimelist[x] for x in x1ticks]
#    plt.xticks(x1ticks,x1labels,rotation=45)
#    plt.plot(df['增仓'])
#    plt.show()
    #dfbig = df.loc[df['现手'] >= bigline]
    #print(dfbig)

#today = datetime.now().strftime('%Y%m%d')
#filename = 'test_' + today + '.csv'

#outfile = open(filename, mode='w')
#output_title(outfile)
#
#start = datetime.now()
#print('开始：',start.strftime('%Y-%m-%d %H:%M:%S'))
#dfs = read_files(datafiles)
#stat_file = stat_data(dfs,bigline)
#stat_file = 'Stated_Records_20181108_1000.csv'
#plot_data(stat_file)

#for i in range(len(biglines)):
#    bigline = biglines[i]

# conding=utf-8
'''
读取多个数据文件（由Wind直接导出的成交明细）
红: {2:'空平',4:'多开',6:'多换',7:'双开'}
绿: {1:'空开',3:'空换',5:'多平',8:'双平'}
'''
from WindPy import w
from Delta_duokong_vs_Delta_Price_Func import *
import numpy as np

pd.set_option('display.max_columns', None)

#####################
codelist = ['HC.SHF','RB.SHF','I.DCE','J.DCE','JM.DCE']
#code = 'J.DCE'
#biglines = [1000,1500]
biglines = [x for x in range(100,5050,100)]    #等差列表产生一系列大单标准线
#bigline = 1000     #手动指定大单标准线
classify_path = 'Classify_Data_noVol/'    #保存按性质分类的每天数据的路径

al_lists = read_al_files()      #读取“已经读取过”的文件清单
#al_lists = []
for a in range(len(codelist)):
    code = codelist[a]
    ### 处理原始数据（按性质分列） ###
    datafiles = get_filelist(al_lists,code) #根据code名称获取没有读取过的文件清单
    if len(datafiles) > 0:
        for i in range(len(datafiles)):
            datafile = datafiles[i]
            print('现手数据按性质分列,第%d个文件: %s' % (i+1,datafile))
            df = read_file(i, al_lists, datafile)  # 读取文件，同时更新“已读取文件清单”
            classify_df = classify_by_nature(df)     #按性质分类数据。主要加入实时总交易量、持仓量，将现手按性质分列输出
            save_classify_CSV(datafile,classify_df,classify_path)     #保存性质分列数据到指定路径
        print('所有文件中的现手数据均已按性质分列')

    ### 根据大单线统计数据 ###
    stat_df = pd.DataFrame(columns=['日期','开盘价','收盘价','价格涨跌','价格涨跌百分比'])
    colnum = len(stat_df.columns)
    for i in range(len(biglines)):
        stat_df.insert(colnum*(i+1)+0,'%d多单' % biglines[i],value=None)
        stat_df.insert(colnum*(i+1)+1,'%d空单' % biglines[i],value=None)
        stat_df.insert(colnum*(i+1)+2,'%d多空差' % biglines[i],value=None)
        stat_df.insert(colnum*(i+1)+3,'%d多空总量比差' % biglines[i],value=None)
        stat_df.insert(colnum*(i+1)+4,'%d多空分类比差' % biglines[i],value=None)
    classify_datafiles = get_classify_files(code,classify_path)     #从指定路径获取分类数据的文件清单
    if len(classify_datafiles) > 0:
        for i in range(len(classify_datafiles)):
            classify_datafile = classify_datafiles[i]
            print('根据大单线列表统计%s文件' % classify_datafile)
            day = classify_datafile.strip('.csv').split('_')[1]
            file = classify_path + classify_datafile
            df = pd.read_csv(file, encoding='gb2312')  # 读取文件
            openpx = df['价格'].iloc[1]   #当天开盘价
            closepx = df['价格'].iloc[df.index[-1]]   #当天收盘价
            change_px1 = closepx-openpx    #当天收盘价格涨跌数
            change_px2 = 100*(closepx-openpx)/openpx     #当天收盘价格涨跌百分比
            #print(day, ':', openpx, closepx,change_px1,change_px2)
            stat_df.loc[i, '日期'] = day
            stat_df.loc[i,'开盘价'] = openpx
            stat_df.loc[i,'收盘价'] = closepx
            stat_df.loc[i,'价格涨跌'] = change_px1
            stat_df.loc[i,'价格涨跌百分比'] = change_px2
            total = (df.loc[:, '现手'].sum())
            total_duo = (df.loc[:, '多开'].sum() + df.loc[:, '空平'].sum())
            total_kong = (df.loc[:, '空开'].sum() + df.loc[:, '多平'].sum())
            for j in range(len(biglines)):
                bigline = biglines[j]
                big_duo = (df.loc[:, '多开'][df['多开'] >= bigline].sum() + df.loc[:, '空平'][df['空平'] >= bigline].sum())
                big_kong = (df.loc[:, '空开'][df['空开'] >= bigline].sum() + df.loc[:, '多平'][df['多平'] >= bigline].sum())
                delta_duo_kong = big_duo - big_kong
                deltaratio_total = delta_duo_kong*100/total
                deltaratio_duo_kong = 100*(big_duo/total_duo) - 100*(big_kong/total_kong)
                stat_df.loc[i, '%d多单' % bigline] = big_duo
                stat_df.loc[i, '%d空单' % bigline] = big_kong
                stat_df.loc[i, '%d多空差' % bigline] = delta_duo_kong
                stat_df.loc[i, '%d多空总量比差' % bigline] = 100*delta_duo_kong/total
                stat_df.loc[i, '%d多空分类比差' % bigline] = deltaratio_duo_kong
            update_big_list(code,classify_datafile)
        filename = code + '_BigDuoKong_vs_Price.xlsx'
        save_Excel(filename,stat_df)
        calc_correlation(code,biglines,filename)
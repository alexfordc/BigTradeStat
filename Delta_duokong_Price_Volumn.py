# conding=utf-8
'''
读取多个数据文件（由Wind直接导出的成交明细）
红: {2:'空平',4:'多开',6:'多换',7:'双开'}
绿: {1:'空开',3:'空换',5:'多平',8:'双平'}
'''
from WindPy import w
from Delta_duokong_Price_Volumn_Func import *
import numpy as np

pd.set_option('display.max_columns', None)

#######################################################
codelist = ['HC.SHF','RB.SHF','I.DCE','J.DCE','JM.DCE']     #要处理的品种的名称列表。品种数据文件名中需包含此名称
biglines = [x for x in range(100,5050,100)]    #等差列表产生一系列大单标准线

origin_path = '../Wind直接导出数据/'      #从Wind导出的原始数据的存放路径
treated_path = 'Treated_Data/'          #保存增加持仓量、按性质分类后的数据的路径

already_read_logfile = 'Already_Read_Files.log'     #记录哪些原始数据文件已经读取

#######################################################

already_read_files = get_already_files(already_read_logfile)      #读取“已经读取过”的文件清单
w.start()
for a in range(len(codelist)):      #按照code列表中的顺序依次处理
    code = codelist[a]
    ### 处理原始数据（增加持仓数据，现手按性质分列） ###
    datafiles = get_datafiles(origin_path,already_read_files,code)   #根据code名称、已读取文件列表，获取没有读取过的文件清单
    if len(datafiles) > 0:
        for i in range(len(datafiles)):
            datafile = datafiles[i]
            print('处理第%d个文件(%s), 增加持仓数据, 现手数据按性质分列' % (i+1,datafile))
            pre_oi = w.wsd(code, 'oi', "ED-1TD", getdate(datafile), '').Data[0][0]  # 获取数据文件日期前一天收盘后的持仓量
            df = read_datafile(origin_path,datafile)  # 读取文件，同时更新“已读取文件清单”
            treated_df = volumn_classify(pre_oi,df)     #加入实时总交易量、持仓量，将现手按性质分列输出
            save_treated_csv(datafile,treated_df,treated_path)     #保存增加持仓、性质分列后的数据到指定路径
            update_listfile(already_read_logfile,datafile)   #更新已读文件列表
        print('所有%s原始数据文件已增加持仓数据、按性质分列' % code)

    ### 根据大单线统计 ###
    fixed_list = ['日期','时间段','开始价','结束价','价格涨跌','价格涨跌百分比','开始持仓','结束持仓','持仓变化','持仓变化百分比']   #定义固定的列标题
    scale_list = ['多单','空单','多空差','多空总量比差']#,'多空分类比差']      #根据不同大单线的固定标题
    stat_df = init_stat_df(fixed_list,scale_list,biglines)
    already_statbig_logfile = '%s_Already_StatBig_Files.log' % code     #记录哪些Volumn_Classify数据文件已根据大单线统计数据
    statbig_files = get_statbig_files(code,already_statbig_logfile,treated_path)     #从指定路径获取需要根据大单线统计数据的文件清单
    if len(statbig_files) > 0:
        for i in range(len(statbig_files)):
            statbig_file = statbig_files[i]
            print('根据大单线统计%s文件' % statbig_file)
            day = statbig_file.split('_')[1]
            file = treated_path + statbig_file
            df = pd.read_csv(file,encoding='gb2312')  # 读取文件
            indexlists = get_timeinterval_indexs(code,df)
            stat_df = stat_by_biglines(biglines,df,stat_df,indexlists,day)
            update_listfile(already_statbig_logfile, statbig_file)
        save_statbig_excel(code,stat_df)
#        calc_correlation(code,biglines,filename)
# conding=utf-8
'''
根据文件夹内文件清单和已读文件清单，处理原始数据：
（1）增加持仓量
（2）按照交易性质分列显示
'''

from WindPy import w
from Treat_Original_Data_Func import *
import numpy as np

pd.set_option('display.max_columns', None)

#######################################################
codelist = ['HC.SHF','RB.SHF','I.DCE','J.DCE','JM.DCE']     #要处理的品种的名称列表。品种数据文件名中需包含此名称
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

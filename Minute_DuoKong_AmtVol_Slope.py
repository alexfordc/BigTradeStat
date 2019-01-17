# conding=utf-8
'''
（1）统计1分钟内，做多与做空的次数、交易量、及两者各自差值
（2）统计上述1分钟后的n分钟内，每分钟交易价格的线性拟合斜率
分析（1）与（2）之前有无关联
'''

import numpy as np
from Minute_DuoKong_AmtVol_Slope_Func import *

#######################################################
codelist = ['HC.SHF','RB.SHF','I.DCE','J.DCE','JM.DCE']     #要处理的品种的名称列表。品种数据文件名中需包含此名称
origin_path = '../Wind直接导出数据/'      #从Wind导出的原始数据的存放路径
treated_path = 'Treated_Data/'          #保存增加持仓量、按性质分类后的数据的路径
already_StatMinute_logfile = 'Already_StatMinute_Files.log'     #记录哪些数据文件已经统计了每分钟内的多空次量，价格变化
#######################################################
already_statminute_files = get_already_files(already_StatMinute_logfile)
for i in range(len(codelist)):      #按照code列表中的顺序依次处理
    code = codelist[i]
    treated_files = get_treated_files(code, already_statminute_files, treated_path)
    treated_files = treated_files[0:1]
    if len(treated_files) > 0:
        for j in range(len(treated_files)):
            treated_file = treated_files[j]
            print(treated_file)
            df = read_file(treated_path,treated_file)
            minute_indexs = get_minute_index(df.时间)
            minute,Amount_Duo,Amount_Kong,delta_Amount,Count_Duo,Count_Kong,delta_Count = minute_stat(df,minute_indexs)
            test = later_minute_stat(df,minute_indexs,10)

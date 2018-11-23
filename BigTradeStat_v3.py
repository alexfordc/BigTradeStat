# conding=utf-8
'''
读取多个数据文件（由Wind直接导出的成交明细）
红: {2:'空平',4:'多开',6:'多换',7:'双开'}
绿: {1:'空开',3:'空换',5:'多平',8:'双平'}
'''
from WindPy import w
from OperFunc import *
from ReadFunc import *
from WriteFunc import *
import time
import numpy as np
import matplotlib.pyplot as plt

#####################
#codelist = ['RB.SHF','I.DCE','J.DCE']
code = 'RB.SHF'
bigline = 1000     #手动指定大单标准线
#biglines = [1000]
#bigline = [x for x in range(0,500,100)]    #等差列表产生一系列大单标准线
#total = []
#total_nature = []
#today = datetime.now().strftime('%Y%m%d')
#filename = 'test_' + today + '.csv'

#outfile = open(filename, mode='w')
#output_title(outfile)
#
#start = datetime.now()
#print('开始：',start.strftime('%Y-%m-%d %H:%M:%S'))
datafiles = get_filelist(code)
dfs = read_files(datafiles)
stat_file = stat_data(dfs,bigline)
#stat_file = 'Stated_Records_20181108_1000.csv'
#plot_data(stat_file)

#for i in range(len(biglines)):
#    bigline = biglines[i]




#oldfiles, livefile = get_files(code)        #默认当前日期或最后一个文件为正在更新的数据文件
#
#if len(oldfiles) > 0:
#    olddf = read_old_files(oldfiles)
#    #print(olddf)
#    end1 = datetime.now()
#    print('读取以往文件结束：',end1.strftime('%Y-%m-%d %H:%M:%S'))
#    print('读取以往文件用时：',(end1-start).seconds,'秒')
#
#    ### 读取以往数据，逐行计算各参量 ###
#    for index, row in olddf.iterrows():
#        rowdate = row.rt_date
#        rowtime = row.rt_time
#        rowlastpx = row.rt_last
#        df = olddf[:index+1]        #切片获取到index为止的所有数据
#        dfbig = olddf[:index+1].loc[df['rt_last_vol'] >= bigline]       #切片获取到index为止的大单数据
#        total = sum_big_vol(df, dfbig)      #累积的总交易量、总增仓量、大单交易量、大单增仓量
#        total_nature = split_big_group(df, dfbig)       #按性质分组的，累积总交易量、总增仓量、大单交易量、大单增仓量
#        print(rowdate,rowtime,rowlastpx,total)
#        output(outfile,rowdate,rowtime,rowlastpx,total,total_nature)
#    end2 = datetime.now()
#    print('统计以往数据结束：',end2.strftime('%Y-%m-%d %H:%M:%S'))
#    print('统计以往数据用时：',(end2-end1).seconds,'秒')
#else:
#    print('无以往数据 或 仅有一个数据文件')
#
##livefile = '../GetDayTradeInfo/RB.SHF_20181029.csv'
#
##print(total,total_nature)
#
#num = 0
#iii = 0
#while iii < 5:
#    start2 = datetime.now()
#    livedf = read_live_file(livefile,num)
#    #num += 5
#    iii += 1
#    print('-'*20)
#    num += len(livedf)
#    if len(livedf) > 0:
#        for index, row in livedf.iterrows():
#            rowdate = row.rt_date
#            rowtime = row.rt_time
#            rowlastpx = row.rt_last
#            df = livedf[:index+1]        #切片获取到index为止的所有数据
#            dfbig = livedf[:index+1].loc[df['rt_last_vol'] >= bigline]       #切片获取到index为止的大单数据
#            live_total = live_sum_big_vol(df, dfbig,total)      #累积的总交易量、总增仓量、大单交易量、大单增仓量
#            live_total_nature = live_split_big_group(df, dfbig,total_nature)       #按性质分组的，累积总交易量、总增仓量、大单交易量、大单增仓量
#            print(rowdate,rowtime,rowlastpx,live_total)
#            output(outfile,rowdate,rowtime,rowlastpx,live_total,live_total_nature)
#        total = live_total
#        total_nature = live_total_nature
#        #print(total, total_nature)
#
#    end3 = datetime.now()
#    print('统计实时数据结束：', end3.strftime('%Y-%m-%d %H:%M:%S'))
#    print('统计实时数据用时：', (end3 - start2).seconds, '秒')
#    time.sleep(1)
#outfile.close()
#print('总结束：',end3.strftime('%Y-%m-%d %H:%M:%S'))
#print('总用时：',(end3-start).seconds,'秒')


#rtdatetime = np.loadtxt(filename, delimiter=',', dtype=str, usecols=(1), unpack=False, skiprows=1)
#last_px,total_vol,total_oi,big_vol = np.loadtxt(filename, delimiter=',', dtype=int, usecols=(2,3,4,5), unpack=True, skiprows=1)
#total_vol_2,total_vol_4 = np.loadtxt(filename, delimiter=',', dtype=int, usecols=(11,19), unpack=True, skiprows=1)
#total_vol_1,total_vol_5 = np.loadtxt(filename, delimiter=',', dtype=int, usecols=(7,23), unpack=True, skiprows=1)
#total_vol_duo = total_vol_2 + total_vol_4
#total_vol_kong = total_vol_1 + total_vol_5

#plt.rcParams['figure.figsize'] = (20.0, 16.0)
#plt.rcParams['lines.linewidth'] = 1
##plt.plot(rtdatetime,last_px)
#plt.xticks(rotation=90)
#plt.plot(rtdatetime,last_px, color='black', label='Live Price')
#plt.plot(rtdatetime,total_vol, color='black', label='Total Volumn')
#plt.plot(rtdatetime,total_oi, color='black', label='Total OI Change')
#plt.plot(rtdatetime,big_vol, color='black', label='Big Trade Volumn')
#plt.plot(rtdatetime,total_vol_duo, color='red', label='Duo Trade Volumn')
#plt.plot(rtdatetime,total_vol_kong, color='green', label='Kong Trade Volumn')
#plt.legend()
#plt.show()
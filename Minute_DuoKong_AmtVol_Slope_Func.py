# conding=utf-8

import numpy as np
import pandas as pd
import os

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

def get_treated_files(code, already_statminute_files, treated_path):
    '''获取尚未进行每分钟统计的文件列表，返回文件名列表'''
    allfiles = os.listdir(treated_path)
    codefiles = []
    for item in allfiles:
        if (code in item) and (item not in already_statminute_files):
            codefiles.append(item)
    codefiles = sorted(codefiles)  # 按照文件名排序
    print('#' * 100)  # 分割线
    if len(codefiles) == 0:
        print('所有%s文件均已按每分钟统计。如需重读，请更改已处理文件列表。' % (code))
    else:
        print('需统计%d个%s数据文件: %s' % (len(codefiles), code, ', '.join(codefiles)))
    return codefiles
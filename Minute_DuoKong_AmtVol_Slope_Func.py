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

def get_treated_files(code, already_StatMinute_logfile, treated_path):
    '''获取尚未进行每分钟统计的文件列表，返回文件名列表'''
    allfiles = os.listdir(treated_path)
    already_statminute_files = get_already_files(already_StatMinute_logfile)

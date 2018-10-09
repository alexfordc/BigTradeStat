# conding=utf-8
import csv,os
from datetime import datetime

def strlist(list):
    for i in range(len(list)):
        list[i] = str(list[i])
    return  list

def WriteTickMergeData(codelist,tradedata,olddata):
    today = datetime.now().strftime('%Y%m%d')
    for i in range(len(codelist)):
        codename = codelist[i]
        filename = codename+'_'+today+'.csv'
        if os.path.isfile(filename):
            tempfile = open(filename, 'r')
            reader = csv.reader(tempfile)
            lastline = list(reader)[-1]
            tempfile.close()
            if (lastline != strlist(tradedata[i])):
                csvfile = open(filename, 'a', newline='')
                writeCSV = csv.writer(csvfile)
                writeCSV.writerow(strlist(tradedata[i]))
                print(codelist[i],':',strlist(tradedata[i]))
                csvfile.close()
            else:
                print('重复数据,',codelist[i], ':', strlist(tradedata[i]))
        else:
            csvfile = open(filename, 'w', newline='')
            writeCSV = csv.writer(csvfile)
            writeCSV.writerow(["Date","Time","LastPX","Last_Vol","OI_Change","Nature"])
            writeCSV.writerow(strlist(tradedata[i]))
            print(codelist[i], ':', strlist(tradedata[i]))
            csvfile.close()
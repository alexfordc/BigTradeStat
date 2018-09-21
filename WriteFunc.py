# conding=utf-8
import csv
from datetime import datetime

def WriteTick(codelist,tradedata):
    today = datetime.now().strftime('%Y%m%d')
    for i in range(len(codelist)):
        codename = codelist[i]
        filename = codename+'_'+today+'.csv'
        csvfile = open(filename,'a',newline='')
        writeCSV = csv.writer(csvfile)
        writeCSV.writerow(tradedata[i])
        #print(codelist[i],end=':')
        print(tradedata[i])


# conding=utf-8
import csv,os
from datetime import datetime

def output_title(outfile):
    print('date', 'time', 'total_vol', 'total_oi', 'big_vol', 'big_oi', sep=',', end=',',file=outfile)
    for i in range(1, 8):
        print(('total_vol_%d,total_oi_%d,big_vol_%d,big_oi_%d') % (i, i, i, i), end=',',file=outfile)
    print(('total_vol_%d,total_oi_%d,big_vol_%d,big_oi_%d') % (8, 8, 8, 8),file=outfile)
    outfile.flush()

def output1(rowdate,rowtime,total_vol,total_oi,big_vol,big_oi,vol_nature, oi_nature, big_vol_nature, big_oi_nature):
    now = datetime.now().strftime('%Y%m%d')
    outfile = open('test_' + now + '.csv', mode='a')
    print(rowdate,rowtime,total_vol,total_oi,big_vol,big_oi,sep=',',end=',')#,file=outfile)
    for i in range(1,9):
        if i != 8:
            print(vol_nature[i],oi_nature[i],big_vol_nature[i],big_oi_nature[i],sep=',',end=',')#,file=outfile)
        elif i == 8:
            print(vol_nature[i], oi_nature[i], big_vol_nature[i], big_oi_nature[i], sep=',')#,file=outfile)
            outfile.flush()

def output(outfile,rowdate,rowtime,total,total_nature):
    print(rowdate,rowtime,sep=',',end=',',file=outfile)
    for i in range(len(total)):
        print(total[i],end=',',file=outfile)
    for i in range(1,8):
        for j in range(len(total_nature)):
            print(total_nature[j][i],end=',',file=outfile)
    for j in range(len(total_nature)):
            if j != 3:
                print(total_nature[j][8],end=',',file=outfile)
            elif j == 3:
                print(total_nature[j][8],file=outfile)
    outfile.flush()





#def strlist(list):
#    for i in range(len(list)):
#        list[i] = str(list[i])
#    return  list
#
#def WriteTickMergeData(codelist,tradedata,olddata):
#    today = datetime.now().strftime('%Y%m%d')
#    for i in range(len(codelist)):
#        codename = codelist[i]
#        filename = codename+'_'+today+'.csv'
#        if os.path.isfile(filename):
#            tempfile = open(filename, 'r')
#            reader = csv.reader(tempfile)
#            lastline = list(reader)[-1]
#            tempfile.close()
#            if (lastline != strlist(tradedata[i])):
#                csvfile = open(filename, 'a', newline='')
#                writeCSV = csv.writer(csvfile)
#                writeCSV.writerow(strlist(tradedata[i]))
#                print(codelist[i],':',strlist(tradedata[i]))
#                csvfile.close()
#            else:
#                print('重复数据,',codelist[i], ':', strlist(tradedata[i]))
#        else:
#            csvfile = open(filename, 'w', newline='')
#            writeCSV = csv.writer(csvfile)
#            writeCSV.writerow(["Date","Time","LastPX","Last_Vol","OI_Change","Nature"])
#            writeCSV.writerow(strlist(tradedata[i]))
#            print(codelist[i], ':', strlist(tradedata[i]))
#            csvfile.close()
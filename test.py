# conding=utf-8

from WindPy import w
from functions import *
import time


w.start()

timelist = ["22:43","23:00"]
timeinterval = 1
timelist2 = TransTimeList(timelist)
while CheckTime(timelist2):
    interval = CheckInterval(timeinterval, timelist2)
    time.sleep(interval)
    data = w.wsq("RB.SHF", "rt_date,rt_time,rt_last,rt_latest,rt_last_vol,rt_oi_change,rt_nature")
    print(data.Data)

w.stop()
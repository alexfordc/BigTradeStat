# conding=utf-8
import time
import pandas as pd




while True:
    f1 = pd.read_table('test.txt')
    num = len(f1)
    print(num)
    time.sleep(1)
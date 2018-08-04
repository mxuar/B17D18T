import numpy as np
import pandas as pd
from itertools import islice
import re

with open("temperature_daily.csv") as f:
        array = f.readlines()[1:]

data = []
for line in array:
    line = line.strip()        #delete return
    linelist = re.split("[,-]",line)
    data.append(linelist[0:5])

for i in range(len(data)):
    if i == 0:
        mintemp = []
        maxtemp = []
        year = [data[i][0]]
        month = [data[i][1]]
        a = data[i][3]
        b = data[i][4]
    elif data[i-1][0:2] != data[i][0:2]:
        mintemp.append(a)
        maxtemp.append(b)
        year.append(data[i][0])
        month.append(data[i][1])
        a = data[i][3]
        b = data[i][4]
    else: 
        a = min(int(float(a)),int(float(data[i][3])))
        b = max(int(float(b)),int(float(data[i][4])))
    if i == len(data)-1:
        mintemp.append(a)
        maxtemp.append(b)
mindata = [[a,b,c,d] for a,b,c,d in zip(year,month,mintemp,maxtemp)]
maxdata = [[a,b,c,d] for a,b,c,d in zip(year,month,maxtemp,mintemp)]

column = ['year','month','three','four']
minDF = pd.DataFrame(columns = column, data = mindata)
maxDF = pd.DataFrame(columns = column, data = maxdata)
minDF.to_csv("/Users/xumin/Desktop/codingtest/minimum.csv")
maxDF.to_csv("/Users/xumin/Desktop/codingtest/maximum.csv")
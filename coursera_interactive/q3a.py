"""
Created on Oct 28, 2013

@author: Nathan S.
"""
import re
from datetime import date, timedelta
import sys

mydate = date.today()
td = timedelta(days=1)
dateformat = "%B %d, %Y"

mfp_doc = "C:\\Users\\Administrator\\Documents\\Programming\\mfp_test.txt"
re.DOTALL = True

with open(mfp_doc, 'r') as myfile:
    text = myfile.read()
    


    
# for i in range(500):
# mydate -= td
# ds = mydate.strftime(dateformat)
    
find_date_ptrn = re.compile(r'(?<=id="date">)(.*)</h2>')
find_cal_ptrn = re.compile(r'(?<=TOTAL:</td>)\s+<td>(\d*),*(\d*)</td>')

dates = re.findall(find_date_ptrn, text)
cals = [int(''.join(x)) for x in re.findall(find_cal_ptrn, text)]

print(len(dates))
print(dates)
print(len(cals))
print(cals)

for i in range(17):
    mydate -= td

print(dates[-1])
print(mydate.strftime(dateformat))

i = len(dates)-1
while i > 0:
    mydate -= td
    ds = mydate.strftime(dateformat)
    if dates[i] != ds:
        i += 1
        dates.insert(i, ds)
        cals.insert(i, cals[i+1])
    if cals[i] < 1200:
        cals[i] = 2000
        print("derp", ds)
#         cals[i] = cals[i+1]
    i -= 1
        
print(len(cals))
totalcals = sum(cals)
calperday = totalcals/len(dates)
     
caldict = {k:v for k,v in zip(dates,cals)}

for day in range(20, 30):
    print(caldict["April %d, 2013" % day])

print(calperday)
    
    

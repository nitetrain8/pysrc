"""
Created on Oct 28, 2013

@author: Nathan S.
"""
import re
from datetime import date, timedelta
import sys


def main():
    mydate = date.today()
    td = timedelta(days=1)
    dateformat = "%B %d, %Y"

    mfp_doc = "C:\\Users\\Administrator\\Documents\\Programming\\mfp_test.txt"
    mfp_doc = "C:\\Users\\PBS Biotech\Documents\\Personal\\test files\\mfp.txt"

    with open(mfp_doc, 'r') as myfile:
        text = myfile.read()




    # for i in range(500):
    # mydate -= td
    # ds = mydate.strftime(dateformat)

    find_date_ptrn = re.compile(r'(?<=id="date">)(.*)</h2>')
    find_cal_ptrn = re.compile(r'(?<=TOTAL:</td>)\s+<td>(\d*)(?:,*)(\d*)</td>')

    dates = re.findall(find_date_ptrn, text)
    cals = [int(''.join(x)) for x in re.findall(find_cal_ptrn, text)]

    if len(dates) != len(cals):
        raise ValueError("oh no!")

    ave_daily = sum(cals) / len(cals)
    return ave_daily, dates, cals

if __name__ == '__main__':
    main()





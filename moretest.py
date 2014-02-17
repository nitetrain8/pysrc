mfp_doc = "C:\\Users\\Administrator\\Documents\\Programming\\docs\\output\\mfp_test2.txt"

import re
import io
ptrn = r"(?<=TOTAL:</td>)\s+?<td>(.*?)</td>"
with open(mfp_doc, 'r') as f:
    text = f.read()

a = [int(i.replace(",", "")) for i in re.findall(ptrn, text, re.DOTALL)]
# print(a)
a = a[-120:]
total = sum(a)
days = len(a)
ave = total/days
possible = []
for weight_end in range(175, 178):
    for weight_start in range(171, 174):

        weight_diff = weight_end-weight_start

        total_surplus = weight_diff * 3500
        info = (weight_start, weight_end, ave-total_surplus/days)
        print(*info)
        possible.append(info)

possible.sort(key=lambda x:x[2])
print("\n Max and Min:")
print(*possible[-1])
print(*possible[0])





mfp_doc = "C:\\Users\\Administrator\\Documents\\Programming\\docs\\output\\mfp_test2.txt"


import re

ptrn = r".*TOTAL:\<\/td\>.*<td>(.*)</td>"
ptrn = r"(?<=TOTAL:</td>\n  \t\t<td>)(.*?)</td>"
ptrn = r"(?<=TOTAL:</td>)\s+?<td>(.*?)</td>"
with open(mfp_doc, 'r') as f:
    text = f.read()
    
a = [int(i.replace(",", "")) for i in re.findall(ptrn, text, re.DOTALL)]
print(a)

total = sum(a)
days = len(a)

ave = total / days

for weight_end in range(176, 178):
    weight_start = 173

    weight_diff = weight_end-weight_start
    
    total_surplus = weight_diff * 3500
    
    print(weight_end, ave - total_surplus / days)
    




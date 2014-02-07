
import os.path
uifile = 'C:\\python33\\lib\\site-packages\\pyqt5\\myprojects\\ui\\myIDE.ui'

import xml.etree.ElementTree as etree
tree = etree.parse(uifile)
connections = tree.find('connections')

# from office import pbsdbg

for w in tree.findall('./widget/widget'):
    try:
        print(w.attrib['name'])
    except:
        print(w)

for times in tree.iter():
    print(times)

print(connections)
connections = connections.findall('connection')
print(connections)
funcs = []
for con in connections:
    receiver = con.find('receiver').text
    if receiver != "MyCompiler":
        continue
    sender = con.find('sender').text
    signal = con.find('signal').text
    slot = con.find('slot').text
    print(sender.text, signal.text, receiver.text, slot.text)
    print("Send signal %s from %s to slot %s of %s" % \
            (signal, sender, slot, receiver))
    funcs.append(slot)

uifile = open(r'C:\Python33\Lib\site-packages\PyQt5\myprojects\ui\MyIDE.ui', 'r')
outfile = open(r'C:\Python33\Lib\site-packages\PyQt5\myprojects\python\MyCompiler.py', 'w')

uifile.close()
outfile.close()


import os


datadir = "C:\\Users\\Administrator\\Documents\\Programming\\Coursera\\Data Analysis\\"

dirs = os.listdir(datadir)
# print(datadir +dirs[0])
    
def getmonitor(id, directory, summarize=False):
    id_str = str(id)
    for i in range(3-len(id_str)):
        id_str = "0" + id_str
    id_str += ".csv"
    
    if directory[-1] != "\\":
        directory += "\\"
    
    with open(datadir + directory + id_str) as myfile:
        input = [[x.strip("\"") for x in s.split(',')] for s in myfile.read().split('\n')]
#         print(input)
        
    if not summarize:
        return input    
    
    
       
data = getmonitor(1, "specdata" )
[print(d) for d in data]
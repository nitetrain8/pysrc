import html
from html.parser import HTMLParser
import urllib
import urllib.request as request
import bs4 as soup
import calendar
import datetime

mfp_doc = "C:\\Users\\Administrator\\Documents\\Programming\\mfp_test.txt"
# 


class weblogin():
    '''class for web logins
    import modules in case they haven't been already,
    so that namespace isn't cluttered unless necessary
    '''
    global urllib
    global request 
    global cookielib
    
    
    import urllib
    import urllib.request as request
    import http.cookiejar as cookielib
    
    def __init__(self, login, password):
        
#         import urllib
#         import urllib.request as request
#         import http.cookiejar as cookielib
#         
        self.login = login#.encode('utf-8')
        self.password = password#.encode('utf-8')
        self.cal_list = []
        
        self.cj = cookielib.CookieJar()
        self.opener = request.build_opener(
                    request.HTTPRedirectHandler(),                       
                    request.HTTPHandler(debuglevel=0),
                    request.HTTPSHandler(debuglevel=0),
                    request.HTTPCookieProcessor(self.cj)
        )
        
        self.logintomfp()
        self.logintomfp()
        
    def logintomfp(self):
        
        user_id = 'username'#.encode()
        pass_id = 'password'#.encode()
        
        #print("login%s\npassword%s\nuser_id%s\npass_id%s\n" % (self.login.__class__, self.password.__class__, user_id.__class__, pass_id.__class__))
        
        self.login_data = urllib.parse.urlencode(
                                    {user_id : self.login,
                                    pass_id : self.password}
        ).encode('utf-8')
        print(self.login_data)
        self.response = self.opener.open("https://www.myfitnesspal.com/account/login", self.login_data)
#         print(dir(self.cj))
#         print(self.cj)
        
    def open(self, url, data=None):
#         if data is None:
#             data = self.login_data
        return self.opener.open(url, data)
    
    def source_from_url(self, url, data=None, encode='utf-8'):
        
        return self.open(url,data).read().decode('utf-8')
    
    def get_cal_from_date(self, date):
        
        source = self.source_from_url("https://www.myfitnesspal.com/food/diary/nitetrain8?date=%s" % date)
        text=source.split("\n")
        
        try:
            totalsindex = text.index('Totals')
        except:
            print(date)
            global cal_list
            print(cal_list)
            raise
        day_cals = text[totalsindex+1]
        
        return self.fudge_cal(int(''.join(day_cals.split(','))))
    
    def fudge_cal(self, cal):
        if cal < 1200:
            global cal_list
            cal = cal_list[-1][1]
        return cal
        

        
        
        
        

login = weblogin('nitetrain8', '081089')



mfp_calendar = calendar.Calendar()



months = 3
year = 2012
month = 9
day = 1
cal_list = []
for i in range(months):
    
    for day in range(1, calendar.monthrange(year, month)[1]+1):

        date = "{}-{}-{}".format(year, month, day)
        cals = login.get_cal_from_date("%d-%d-%d" % (year, month, day))
        cal_list.append([date, cals])
        print(date)

    month += 1
    if month > 12:
        year += 1
        month = 1


with open(mfp_doc, 'w') as doc:
    for line in cal_list:
        doc.write("%s\n" % line)
        
        
import excelcon

excel = excelcon.Excel()
wb = excel.Workbooks.Add(1)
sheet = wb.Worksheets(1)
cells = sheet.Cells

cells(1,1).Value = "Date"
cells(1,2).Value = "Calories"
cells(1,3).Value = "Est +/-"
cells(1,4).Value = "Total"
cells(1,5).Value = "Ave Daily"
cells(1,6).Value = "Est Maintenance"



total_cal = sum([i[1] for i in cal_list])
ave_daily_cal = total_cal/len(cal_list)

cells(2,4).Value = total_cal
cells(2,5).Value = ave_daily_cal

for i in range(len(cal_list)):
    cells(i+2,1).Value = cal_list[i][0]
    cells(i+2,2).Value = cal_list[i][1]
    cells(i+2,3).Value = cal_list[i][1]-ave_daily_cal
    








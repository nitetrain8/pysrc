import urllib
import calendar
import datetime
import requests
import urllib.parse
import pyquery
import json
from collections import OrderedDict
from http.client import HTTPException


def fudge_cal(cal):
    if cal < 400:
        global cal_list
        cal = cal_list[-1][1]
    return cal


class MFPApi():
    """class for web logins
    import modules in case they haven't been already,
    so that namespace isn't cluttered unless necessary
    """

    # URLs
    _weight_progress_url = "http://www.myfitnesspal.com/reports/results/progress/1/%d.json"
    _login_url = "https://www.myfitnesspal.com/account/login"
    _food_diary_url = "https://www.myfitnesspal.com/food/diary?date=%s"
    _copy_meal_url = "https://www.myfitnesspal.com/food/copy_meal?date=%s&from_date=%s&from_meal=%d&username=%s"

    # Enums for copy meal
    BREAKFAST = 0
    LUNCH = 1
    DINNER = 2
    SNACKS = 3
    SNACK = 3

    _meal2name = {
        BREAKFAST: 'breakfast',
        LUNCH: 'lunch',
        DINNER: 'dinner',
        SNACK: 'snack',
        SNACKS: 'snacks'
    }

    _meal2num = {
        'breakfast': BREAKFAST,
        'lunch': LUNCH,
        'dinner': DINNER,
        'snack': SNACK,
        'snacks': SNACKS,
        BREAKFAST: BREAKFAST,
        LUNCH: LUNCH,
        DINNER: DINNER,
        SNACK: SNACK
    }

    def __init__(self, user='nitetrain8', password='081089'):

        self.user = user
        self.password = password

        self.session = requests.Session()
        self.login()

    def login(self):
        self._login(self.session)

    def _login(self, session):

        login_data = urllib.parse.urlencode(
            {'username': self.user,
             'password': self.password}
        ).encode('utf-8')

        response = session.post(self._login_url, data=login_data)
        
        # this is kind of hacky but the easiest way to to tell if the POST was
        # actually successful or returned a "200 wrong usr/pw try again lol"

        if 'form class="form login LoginForm"' in response.content.decode():
            raise HTTPException("401 bad auth")
        
        #print("Login Successful", flush=True)

    def load_cals(self, date):
        return self._load_cals(date, self.session)

    def _download_cals(self, date, session):
        ds = _dt2ds(date)
        date_url = self._food_diary_url % ds
        rsp = session.get(date_url)
        if rsp.status_code != 200:
            raise HTTPException(rsp.status_code)
        return rsp.content

    def _load_cals(self, date, session):
        source = self._download_cals(date, session)
        return self._parse_cals(source)

    def _parse_cals(self, source):
        p = pyquery.PyQuery(source.decode())
        totals = p("#diary-table > tbody > .total")
        cals = 0
        if not totals:
            raise HTTPException("401 bad auth?")
        for t in totals:
            if t.attrib['class'] != 'total':
                continue
            else:
                assert t[0].text == 'Totals'
                sc = t[1].text
                cals = int(sc.replace(",", ""))
                break
        return cals

    def _extract_weights(self, days):
        url = self._weight_progress_url % days
        data = self.session.get(url).content.decode()
        return json.loads(data, object_hook=OrderedDict)

    def load_weights(self, days):
        js = self._extract_weights(days)
        data = js['data']
        data.reverse()
        cd = datetime.date.today()
        day = datetime.timedelta(days=1)
        for i, entry in enumerate(data):
            date = entry['date']
            total = entry['total']
            assert date == "%d/%02d" % (cd.month, cd.day), (date, "%d/%02d" % (cd.month, cd.day))
            data[i] = cd, float(total)
            cd -= day
        data.reverse()
        return data

    def load_weights_range(self, start_date, end_date):

        today = datetime.date.today()
        if end_date > today:
            end_date = today

        # Number of days to return. Today -> Today = 1 result
        days = (today - start_date).days + 1
        data = self.load_weights(days)
        back = (today - end_date).days
        if back:
            data = data[:-back]
        assert data[-1][0] == end_date
        return data

    def load_cals_range_async(self, start_date, end_date, nthreads=48):
        import threading, queue, time
        day = datetime.timedelta(days=1)
        current = start_date
        days = queue.Queue()
        results = queue.Queue()
        ndays = (end_date - start_date).days + 1
        
        # yes, making this number very high really does
        # make it go WAY faster... [edit: moved to param list]
        # nthreads = 48

        while current <= end_date:
            days.put(current)
            current += day
        
        for _ in range(nthreads):
            days.put(None)  # sentinel
        
        def worker(iq, oq, s):
            while True:
                day = iq.get()
                if day is None:
                    break  # all done
                iq.task_done()
                while True:
                    try:
                        html = self._download_cals(day, s)
                    except HTTPException:
                        pass  # retry
                    else:
                        break
                oq.put((day, html))
            #print("thread exiting")

        threads = set()
        for i in range(nthreads):
            s = requests.Session()
            s.cookies = self.session.cookies  # assumes we logged in already
            thread = threading.Thread(None, target=worker, args=(days, results, s), daemon=True)
            thread.start()
            threads.add(thread)
        
        while threads:
            active = threads.copy()
            for a in active:
                if not a.is_alive():
                    threads.remove(a)
            print("\rDownloaded %d of %d (%d active threads)...       " % (results.qsize(), ndays, len(threads)), end="")
            time.sleep(0.200)
        print()

        data = []
        while True:
            try:
                day, html = results.get_nowait()
            except queue.Empty:
                break
            cals = self._parse_cals(html)
            data.append((day, cals))
            print("\rParsing %d of %d                "%(len(data), ndays), end="")
        print()
        return data

    def load_cals_range(self, start_date, end_date):
        one_day = datetime.timedelta(days=1)
        current = start_date
        data = []
        days = (end_date - start_date).days
        i = 1
        while True:
            if current > end_date:
                break
            self.print("\rLoading calories from %s (%d/%d)                          ",
                                 _dt2ds(current), i, days + 1, end="")
            cals = self.load_cals(current)
            data.append((current, cals))
            current += one_day
            i += 1
        self.print()
        return data

    def print(self, msg="", *args, **kw):
        if args:
            msg = msg%args
        kw.setdefault('flush', True)
        print(msg, **kw)

    def copy_meal(self, from_date, to_date, meal=0):
        """ Copy a meal from date to date.
        :param to_date: copy to this date
        :type to_date: datetime.datetime | datetime.date
        :param from_date: copy meal from this date
        :type from_date: datetime.datetime | datetime.date
        :param meal: 0 = breakfast, 1 = lunch, 2 = dinner, 3 = snack
        """
        meal = self._meal2num[meal]
        self.print("Copying %s from %s to %s...", self._meal2name[meal], _dt2ds(from_date), _dt2ds(to_date), end=" ")
        url = self._copy_meal_url % (to_date, from_date, meal, self.user)
        r = self.session.get(url)
        r.raise_for_status()
        self.print("Complete", end="\n")


def _dt2ds(dt):
    """ Datetime to String
    convert datetime.datetime or datetime.date object
    to a string of the form YYYY-MM-DD, suitable for use
    in the food diary url query string.

    :param dt: datetime object
    :type dt: datetime.datetime | datetime.date """
    return dt.strftime("%Y-%m-%d")


def extract_calories(user='nitetrain8', pw='081089', months=10, year=2015, start_month=1):
    mfp = MFPApi(user, pw)
    mp_calendar = calendar.Calendar()

    month = start_month
    days = months * 30
    cal_list = []
    cd = 1
    for m in range(months):
        cm = m + month
        for day in mp_calendar.itermonthdays(year, cm):
                if day == 0:
                    continue
                ds = "%d-%d-%d" % (year, cm, day)
                print("\rParsing: %s (%d/%d)...          " % (ds, cd, days), end="")
                date = datetime.date(year, cm, day)
                cals = mfp.load_cals(date)
                cal_list.append((date, cals))
                cd += 1
        if cm >= 12:
            year += 1
            month -= 12
    mfp_doc = "mfp_test.txt"
    with open(mfp_doc, 'w') as doc:
        for line in cal_list:
            doc.write("%s\t%s\n" % line)

MFP = MFPApi


def to_excel():
    from python.officelib.xllib.xlcom import Excel

    excel = Excel()
    wb = excel.Workbooks.Add(1)
    sheet = wb.Worksheets(1)
    cells = sheet.Cells

    cells(1, 1).Value = "Date"
    cells(1, 2).Value = "Calories"
    cells(1, 3).Value = "Est +/-"
    cells(1, 4).Value = "Total"
    cells(1, 5).Value = "Ave Daily"
    cells(1, 6).Value = "Est Maintenance"

    total_cal = sum([i[1] for i in cal_list])
    ave_daily_cal = total_cal / len(cal_list)

    cells(2, 4).Value = total_cal
    cells(2, 5).Value = ave_daily_cal

    for i in range(len(cal_list)):
       cells(i + 2, 1).Value = cal_list[i][0]
       cells(i + 2, 2).Value = cal_list[i][1]
       cells(i + 2, 3).Value = cal_list[i][1] - ave_daily_cal

if __name__ == '__main__':
    mfp = MFPApi()
    # data = extract_weight_json(mfp, 30)

    def dump_l(l, level=0):
        for v in l:
            space = level * " "
            if isinstance(v, dict):
                print(space, "[", sep="")
                dump_d(v, level+1)
                print(space, "]", sep="")
            elif isinstance(v, list):
                print(space, "[", sep="")
                dump_l(v, level + 1)
                print(space, "]", sep="")
            else:
                print(space, v)

    def dump_d(d, level=0):
        for k in d:
            v = d[k]
            if isinstance(v, dict):
                print(k,":", sep="")
                dump_d(v, level+1)
            elif isinstance(v, list):
                print(k, ":", sep="")
                dump_l(v, level + 1)
            else:
                print("%s%s=%s" % (level*" ", k,v))
    data = mfp.load_cals_range(datetime.date(2015, 2, 7), datetime.date(2015, 8, 1))
    with open('mfp_test3.csv', 'w') as f:
        for a, b in data:
            print(a, b)
            f.write("%s,%s\n"%(a,b))

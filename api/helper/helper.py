import random
import math
import hashlib
import json
import socket
from turtle import st
from django.core.validators import validate_email
from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta
from django.db import connection 
import requests
from api.config import webconfig

class Helper:
    def getRandom(self):
        return math.ceil(random.random() * 1000000)

    def passwordEncrypt(self, password):
        return hashlib.sha256(str(password).encode("utf-8")).hexdigest()
    
    def generateCodeName(self, word):
        return word.lower().replace(" ", "_")

    def executeQuery(self, sql, params=[]):
        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                params
            )

    def getFutureDate(self, months):
        current_date_time = timezone.datetime.now()
        future_date = current_date_time + relativedelta(months=months)
        return future_date
    ###########################
    def getPageList(self, counter):
        page_list = []
        for x in range(1,counter+1):
            page_list.append(x)
        return page_list

    def CovertListToSQLTuple(self, list):
        list = ",".join(str(x) for x in list)
        return  f"({list})"


    def getDefaultCurrency(self, request):
        vistor_ip = self.vistor_ip_address(request)
        ip = '41.75.186.63' if webconfig.IS_LOCAL_HOST or  (vistor_ip == "127.0.0.1") or (vistor_ip == "localhost") else vistor_ip
        #ip = '77.68.40.42' if webconfig.IS_LOCAL_HOST or  (vistor_ip == "127.0.0.1") or (vistor_ip == "localhost") else vistor_ip
        try:
            url = f"http://www.geoplugin.net/json.gp?ip={ip}"
            payload={}
            headers = {}
            response = requests.get(url,timeout=3)
            response.raise_for_status()
            return json.loads(response.text)
        except requests.exceptions.HTTPError as errh:
            return None
        except requests.exceptions.ConnectionError as errc:
            return None
        except requests.exceptions.Timeout as errt:
            return None
        except requests.exceptions.RequestException as err:
            return None
        return None

    def readStatic(self, staticpath):
        linesstring = ""
        with open(staticpath, "r") as f:
            lines = f.readlines()
            for line in lines:
                linesstring += f"{line}\n"
        return linesstring

    def convertSeconds(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return {
            "hours": hour  if  (hour < 1) else math.ceil(hour),
            "minutes": math.ceil(minutes),
            "seconds": math.ceil(seconds)
        }

    def convertToDate(self, dateString):
        splited_date = dateString.strip().split("-")
        year = int(splited_date[0])
        month = int(splited_date[1])
        days = int(splited_date[2])
        return datetime.date(year, month, days)

    def is_number(self, s):
        try:
            float(s) # for int, long and float
        except ValueError:
            try:
                complex(s) # for complex
            except ValueError:
                return False
        return True

    def isEqual(self, f1, f2):
        f1 = float(f1)
        f2 = float(f2)
        ans1 = f1-f2
        ans2 = f2-f1
        return (ans1 == ans2)


    def compareDates(self, startdate, enddate):
        # 2022-04-28
        now = self.getCurrentDate()
        delta = enddate[0] - now
        hours_left = delta.days if delta.days else 0
        minutes = hours_left * 60
        # months = self.months_between(now, enddate[0]) if self.months_between(now, enddate[0]) else 0
        return {
             "is_expired": now > enddate[0],
             "is_equal": (startdate == enddate),
             "is_greater_than": startdate > enddate,
             "is_less_than": startdate < enddate,
             "minutes_left": minutes,
             "days_left": hours_left,
             "months_left": 0,
             "years_left": 0,
        }
    
    def getDuration(self, startdate, enddate):
        now = timezone.now()
        delta = (enddate - now)
        hours_left = delta.days if delta.days else 0
        minutes = hours_left * 60
        return {
             "is_expired": startdate > enddate,
             "is_equal": (startdate == enddate),
             "is_greater_than": startdate > enddate,
             "is_less_than": startdate < enddate,
             "minutes_left": minutes,
             "days_left": hours_left,
             "months_left": 0,
             "years_left": 0,
        }  
    
    def getCurrentPageName(self, request):
        path = request.path.split("/")
        if len(path) == 0:
            return "home"
        elif len(path) == 2:
            return path[0]
        elif len(path) >= 3:
            return path[1]
        else:
            return path[0]

    def getDurationBetween(self, startdate, enddate):
            delta = (enddate - startdate)
            hours_left = delta.days if delta.days else 0
            minutes = hours_left * 60
            return {
                "is_expired": startdate > enddate,
                "is_equal": (startdate == enddate),
                "is_greater_than": startdate > enddate,
                "is_less_than": startdate < enddate,
                "minutes_left": minutes,
                "days_left": hours_left,
                "months_left": 0,
                "years_left": 0,
            }
        
    def months_between(self, date1,date2):
        if date1>date2:
            date1,date2=date2,date1
        m1=date1.year*12+date1.month
        m2=date2.year*12+date2.month
        months=m2-m1
        if date1.day>date2.day:
            months-=1
        elif date1.day==date2.day:
            seconds1=date1.hour*3600+date1.minute+date1.second
            seconds2=date2.hour*3600+date2.minute+date2.second
            if seconds1>seconds2:
                months-=1
        return months

    def getNextYear(self):
        today = self.getCurrentDate()
        return datetime.date(today.year + 1, today.month, today.day)

    def isEmailValid(self, email):
        valid_email = False
        try:
            validate_email(email)
            valid_email = True
        except:
            valid_email = False
        return valid_email

    def parseJson(self, request):
        return json.loads(request.decode("utf-8"))

    def getCurrentDate(self):
        return datetime.date.today()

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def get_ip_address(request):
        user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip_address:
            ip = user_ip_address.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def getCurrentDateString(self):
        return str(datetime.date.today())

    def getDateTime(self):
        return timezone.datetime.now()

    def empty(self, text):
        return not str(text)

    def vistor_ip_address(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

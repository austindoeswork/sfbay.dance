import subprocess
import pprint
import hashlib
from datetime import datetime
from dateutil import parser as dateParser

# EVENT

class Event:
    def __init__(self, location):
        self.location = location
        self.id       = "INVALID"
        self.logo     = None
        self.img      = None
        self.date     = None
        self.duration = None
        self.title    = None
        self.teacher  = None
        self.link     = None
        self.price    = None
        self.notes    = []

    @classmethod
    def fromDict(cls, d):
        if d["date"] and type(d["date"]) != type(datetime.today()):
            d["date"] = dateParser.parse(d["date"])
        e = cls(d["location"])
        e.id       = d["id"]
        e.logo     = d["logo"]
        e.img      = d["img"]
        e.date     = d["date"]
        e.duration = d["duration"]
        e.title    = d["title"]
        e.teacher  = d["teacher"]
        e.link     = d["link"]
        e.price    = d["price"]
        e.notes    = d["notes"]
        return e

    def hash(self):
        s = self.location + self.teacher + self.date.strftime('%m%d%y%H%M')
        hash_object = hashlib.md5(bytes(s, encoding='utf8'))
        id = hash_object.hexdigest()[:10]
        self.id = id # NOTE this is kinda unsafe/weird, but whatever
        return id

    def is_valid(self):
        if self.location \
        and self.date    \
        and self.title   \
        and self.teacher \
        and self.link    \
        and self.price:
            return True
        return False

    def pprint_oneline(self):
        fmt_s = '''%6.6s | %-30.30s | %-20.20s [%s - %s]'''
        print(fmt_s % (self.location,
         self.title,
         self.teacher,
         self.date.strftime("%m/%d"),
         self.date.strftime("%H:%M")
         ))

    def pprint_safe(self):
        fmt_s = '''loc:      %s
name:     %s
teacher:  %s
date:     %s
time:     %s
duration: %s
link:     %s
price:    %s
valid:    %s'''
        print(fmt_s % (
            self.location,
            self.title,
            self.teacher,
            self.date,
            self.date,
            self.duration,
            self.link,
            self.price,
            self.is_valid()))
        print("notes:")
        print("NONE" if len(self.notes) == 0 else "\n".join(self.notes))

    def pprint(self):
        fmt_s = '''loc:      %s
name:     %s
teacher:  %s
date:     %s
time:     %s
duration: %s
link:     %s
price:    %s
valid:    %s'''
        print(fmt_s % (
            self.location,
            self.title,
            self.teacher,
            self.date.strftime("%m/%d"),
            self.date.strftime("%H:%M"),
            self.duration,
            self.link,
            self.price,
            self.is_valid()))
        print("notes:")
        print("NONE" if len(self.notes) == 0 else "\n".join(self.notes))

# MISC

def shell(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, text=True)
    return process.communicate()[0]

def rollover(num, limit):
    if num >= limit:
        return num - limit
    return num

def duration(start, end):
    delta = end - start
    hours  = int(delta.total_seconds() // 3600)
    minutes = int((delta.total_seconds() % 3600) // 60)
    return str(hours) + ":" + str(minutes)

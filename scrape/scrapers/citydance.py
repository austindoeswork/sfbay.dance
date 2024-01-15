import re
import urllib.parse
import demoji
import pprint
from pyquery import PyQuery as pq
from datetime import datetime
from dateutil import parser as dateParser

import utils

# TODO add more time than 1 week, annoying
STUDIO_NAME  = "City Dance Studios"
STUDIO_LOGO  = "https://images.squarespace-cdn.com/content/v1/5738b9abab48de6e3b53189b/6193f76e-ce5e-4310-9ddb-80513a176733/city+dance+logo+for+mind+body+app.jpg?format=1500w"
NUM_EVENTS = 140

def scrape():
    events = []

    while len(events) < NUM_EVENTS:
        cmd_str = curl_str(len(events),10)
        output = utils.shell(cmd_str)
        new_events = parse(output)
        events += new_events

    return events

def parse(html):
    events = []
    parsed = pq(html)

    for session in parsed(".class-class-row"):
        try:
            event = parse_session(pq(session))
            if event.is_valid():
                events.append(event)
        except:
            pass

    return events

def parse_session(session):
    event = utils.Event(STUDIO_NAME)
    event.logo = STUDIO_LOGO

    # title
    title = session(".class-name").text()
    title, teacher = parse_title(title)
    event.title = title
    event.teacher = teacher

    # check for PW
    if "PERFORMANCE WORKSHOP" in event.title:
        return event

    # link
    btn = session(".btn-class-signup")
    session_id = btn.attr('data-type')
    link = "https://app.acuityscheduling.com/schedule.php?appointmentType=%s&owner=22968233" % session_id
    event.link = link

    # date
    date = dateParser.parse(btn.attr('data-time'))
    event.date = date

    # duration
    duration_str = session(".class-duration").text()
    nums = re.findall('(\d+)', duration_str, re.DOTALL)
    if len(nums) > 1:
        event.duration = "%s:%s" % (nums[0], nums[1])
    else:
        event.duration = "%s:00" % (nums[0])

    # price
    price_str = session(".class-price-column").text()
    price = float(price_str[1:])
    event.price = price

    return event

def parse_title(title):
    split_re = '''(W\/)|(w\/)|(with)|(With)|( w )|( W )'''
    words = re.split(split_re, title)

    # TODO what if split fails
    class_title = words[0]
    teacher = words[-1].strip()

    return [class_title, teacher]

def curl_str(offset, numdays):
    base = '''curl 'https://app.squarespacescheduling.com/schedule.php?action=showCalendar&fulldate=1&owner=22968233&template=class' \
  -H 'x-requested-with: XMLHttpRequest' \
  --data-raw 'type=&calendar=&month=&timezone=America%2FLos_Angeles&skip=true&options%5Boffset%5D=OFFSET&options%5BnumDays%5D=NUMDAYS&ignoreAppointment=&appointmentType=&calendarID=' \
  --compressed
'''

    cmd = base.replace("OFFSET", str(offset))
    cmd = cmd.replace("NUMDAYS", str(numdays))
    return cmd


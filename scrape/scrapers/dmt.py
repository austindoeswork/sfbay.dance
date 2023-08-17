import utils

import re
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from datetime import timedelta
from dateutil import parser as dateParser
from pyquery import PyQuery as pq

STUDIO_NAME  = "DMT"
STUDIO_PRICE = 21.00
STUDIO_LOGO  = "/imgs/dmt.png"

def scrape(scrape_date):
    events = []

    today     = utils.today()
    today_str = today.strftime("%-m%%2f%e%%2f%Y")
    nextweek     = today + timedelta(days=7)
    nextweek_str = nextweek.strftime("%-m%%2f%e%%2f%Y")

    url = "https://clients.mindbodyonline.com/classic/mainclass?studioid=15734&loc=1&date="
    today_url    = url + today_str
    nextweek_url = url + nextweek_str

    firefox_options = Options()
    firefox_options.add_argument('--headless')  # Run Firefox in headless mode
    driver = webdriver.Firefox(options=firefox_options)

    driver.get(today_url)
    time.sleep(4)
    today_html = driver.page_source

    driver.get(nextweek_url)
    time.sleep(4)
    nextweek_html = driver.page_source

    driver.quit()

    #  FOR TESTING
    #  html = ""
    #  with open('tmp_dmt_full.html', 'r') as file:
        #  html = file.read()

    events = parse(today_html)
    events += parse(nextweek_html)

    return events

def parse(html):
    events = []

    parsed = pq(html)
    main = parsed("table#classSchedule-mainTable")

    date_re   = '''class="headText">'''
    event_re  = '''"(oddRow|evenRow)">'''

    current_date_str = None
    for r in main("tbody>tr"):
        row = pq(r)

        # date row
        date_match = re.search(date_re, row.html())
        if date_match != None:
            current_date_str = row.text()
            continue

        # event row
        event_match = re.search(event_re, row.outer_html())
        if event_match != None:
            event = parse_event(row, current_date_str)
            if event.is_valid(): events.append(event)

    return events

def parse_event(row, date_str):
    event = utils.Event(STUDIO_NAME)

    if date_str == None: return event

    button_re = '''"button"'''
    dur1_re = '''(\d{1,2}).{4,}?(\d{1,2})'''
    dur2_re = '''(\d{1,2})'''

    details = row("td")
    time_td     = details.eq(0)
    button_td   = details.eq(1)
    title_td    = details.eq(2)
    teacher_td  = details.eq(3)
    duration_td = details.eq(4)

    # time
    time_str = " ".join(time_td.text().split()[:2])
    start_date = dateParser.parse(date_str + " " + time_str)
    event.date = start_date

    # link
    button_match = re.search(button_re, button_td.outer_html())
    if button_match != None:
        link = button_td("input").attr("onclick")
        if link == None: return event

        # ex:  https://clients.mindbodyonline.com/ASP/res_a.asp?tg=34&classId=2472&classDate=7/22/2023&clsLoc=1
        studio_id_param = "&studioid=15734"
        url = "https://clients.mindbodyonline.com"
        link = link.split(",")[-1][2:-4]
        url += link
        url += studio_id_param
        event.link = url

    # title
    title = title_td.text()
    event.title = title

    # teacher
    teacher = teacher_td.text()
    event.teacher = teacher

    # duration
    duration_text = duration_td.text()
    dur1_match = re.match(dur1_re, duration_text)
    dur2_match = re.match(dur2_re, duration_text)
    if dur1_match != None:
        hours   = dur1_match.group(1)
        minutes = dur1_match.group(2)
    elif dur2_match != None:
        hours = dur2_match.group(1)
        minutes = "00"
    else:
        return event

    duration = hours + ":" + minutes
    event.duration = duration

    # misc
    event.price = STUDIO_PRICE
    event.logo  = STUDIO_LOGO

    return event


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

def scrape():
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
    main = parsed("#classSchedule-mainTable")

    date_re   = '''class="headText">'''
    event_re  = '''"(oddRow|evenRow) row">'''

    current_date_str = None
    for r in main('div').items():
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
    """
    Args:
        row: A div containing the event data. This should look like:
            <div class="evenRow row">
            <div class="col-1">
                <div class="col col-first" style="width: 172px;">6:45 pm  PST</div>
                <div class="col" style="width: 177px;"><input type="button" name="but2491" class="SignupButton" onclick="_gaq.push(['_trackEvent', 'Class_Schedule', 'click', 'Sign_Up_Now_button']);promptLogin('', ' Hip Hop (all levels)  at 6:45 pm  on Monday, 1/8/2024 with Kyle Limin', '/ASP/res_a.asp?tg=34&amp;classId=2491&amp;classDate=1/8/2024&amp;clsLoc=1'); " value="Sign Up Now"/></div>
            </div>
            <div class="col-2">
                <div class="col" style="width: 177px;"><a href="javascript:;" name="cid501" class="modalClassDesc"> Hip Hop (all levels) </a></div>
                <div class="col" style="width: 177px;">Kyle Limin</div>
                <div class="col" style="width: 177px;">1 hour &amp;15 minutes</div>
            </div>
            </div>
        date_str: the date of the event. This should look like `'Mon January 8, 2024'`.


    """
    event = utils.Event(STUDIO_NAME)

    if date_str == None: return event

    button_re = '''"button"'''
    dur1_re = '''(\d{1,2}).{4,}?(\d{1,2})'''
    dur2_re = '''(\d{1,2})'''

    time_td = row.find('.col-1 .col-first')
    title_td = row.find('.col-2 .col:nth-child(1)')
    teacher_td = row.find('.col-2 .col:nth-child(2)')
    duration_td = row.find('.col-2 .col:nth-child(3)')
    button_td = row(".SignupButton").parent()

    time_str = " ".join(time_td.text().split()[:2])
    start_date = dateParser.parse(date_str + " " + time_str)
    event.date = start_date

    # link
    if not button_td:
        return event
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


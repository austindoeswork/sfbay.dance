import re
import urllib.parse
import demoji
import pprint
from pyquery import PyQuery
from datetime import datetime
from dateutil import parser as dateParser

import utils

# TODO add more time than 1 week, annoying
STUDIO_NAME  = "City Dance Studios"
STUDIO_PRICE = 23.0
STUDIO_LOGO  = "https://images.squarespace-cdn.com/content/v1/5738b9abab48de6e3b53189b/6193f76e-ce5e-4310-9ddb-80513a176733/city+dance+logo+for+mind+body+app.jpg?format=1500w"

NUM_DAYS = 6

def scrape():
    events = []
    curl = '''curl 'https://www.citydancesf.com/%s' '''
    days = ['mondays', 'tuesdays', 'wednesdays', 'thursdays', 'fridays', 'saturdays', 'sundays']

    today = utils.today().weekday()
    for i in range(NUM_DAYS):
        weekday = days[utils.rollover(today + i, len(days))]
        cmd = curl % (weekday)

        output = utils.shell(cmd)
        new_events = parse(output)
        events += new_events

    return events

def parse(html):
    events = []

    date_re    = '''<h1>(.*?\d{1,2})<\/h1>'''
    time_re    = '''^.*?(\d{1,2}:\d{2})-(\d{1,2}:\d{2})'''
    section_re = '<section(.*)<\/section>'
    line_re    = '<p(.*?)<\/p>'
    break_re   = '-{6,}|={6,}|_{6,}|\|{6,}' # TODO improve this regex
    event_re   = '''(.*?)\|(.*?)\|(.*?)'''
    link_re    = '''CLICK HERE TO'''
    url_re     = '''<a href="(.*?)">'''
    empty_re   = '''^\s*$'''

    # TODO error handling
    # find date
    date = re.search(date_re, html)
    today = utils.today().date()
    if date is not None:
        date = date.group(1)
        dtime = dateParser.parse(date).date()
        if dtime < today:
             return events
    else:
        return events

    # find section with classes
    section = re.search(section_re, html).group()
    section = demoji.replace(section, "!")
    lines = [x.group() for x in re.finditer(line_re, section)]

    current_event = utils.Event(STUDIO_NAME)
    current_event.price = STUDIO_PRICE
    current_event.logo  = STUDIO_LOGO
    for line in lines:
        is_event = False
        is_link  = False
        is_break = False
        is_else  = False
        is_empty = False

        parsed = PyQuery(line)
        text = parsed.text()

        is_break = re.search(break_re, text) is not None
        is_event = re.search(event_re, text) is not None
        is_link  = re.search(link_re,  text) is not None
        is_empty = re.search(empty_re, text) is not None

        if is_empty: continue
        if is_break:
            if current_event.is_valid():
                events.append(current_event)
            current_event = utils.Event(STUDIO_NAME)
            current_event.price = STUDIO_PRICE
            current_event.logo  = STUDIO_LOGO
            continue

        if is_link:
            url_match = re.search(url_re, line)

            # TODO err handling
            if url_match != None:
                url = url_match.group(1)
                current_event.link = url.replace("amp;","") # NOTE is this enough?
            continue

        if is_event:
            # TODO NOTE some events are split into two lines. This is annoying so
            #           i'm ignoring it for now
            # ex: "5. ! New Time! 7:45-8:45pm | All Levels GROOVES | Jeric Per"
            words = text.split("|")
            if len(words) == 3:
                time_match = re.search(time_re, words[0])
                if time_match != None and len(time_match.groups()) == 2:
                    start_t, end_t = time_match.groups()
                    # assumes PM
                    start_date = dateParser.parse(date + " " + start_t + "pm")
                    end_date   = dateParser.parse(date + " " + end_t   + "pm")
                    current_event.teacher  = words[2].strip()
                    current_event.date     = start_date
                    current_event.duration = utils.duration(start_date, end_date)
                    current_event.title    = words[1].strip()
                    continue
                #  else:
                    # TODO err handling

        # last case is a "note"
        if len(text) > 1:
            current_event.notes.append(text)

    # may not end on a "break"

    if current_event.is_valid():
        events.append(current_event)

    return events

import utils

import re
from datetime import datetime
from dateutil import parser as dateParser
from pyquery import PyQuery as pq

STUDIO_NAME  = "ODC"
STUDIO_PRICE = 21.00
STUDIO_LOGO  = "https://odc.dance/sites/all/themes/odc/images/odc-dance-logo.png"

def scrape(scrape_date):
    events = []

    date_str = scrape_date.strftime("%Y-%m-%d")
    # TODO images
    # TODO make scrape_date actually select the date, but this is ok for now I think
    #  curl = '''curl 'https://widgets.mindbodyonline.com/widgets/schedules/52115/load_markup?callback=jQuery36405655120515382499_1689698523814&options%5Bstart_date%5D=2023-07-18' '''

    curl = '''curl 'https://widgets.mindbodyonline.com/widgets/schedules/52115/load_markup?callback=jQuery36405655120515382499_1689698523814&options%5Bstart_date%5D='''
    curl += date_str + "'"
    res = utils.shell(curl)
    decoded = bytes(res, "utf-8").decode("unicode_escape")

    xml_re = '''class_sessions":"([\s\S]*)","filters'''
    xml_match = re.search(xml_re, decoded)
    xml = ""

    # TODO err handling
    if xml_match != None:
        xml = xml_match.group(1)
    else:
        print("ERR")
        return []

    events = parse(xml)
    return events

def parse(html):
    events = []
    parsed = pq(html)

    for session in parsed(".bw-session"):
        event = parse_session(pq(session))
        if event.is_valid(): events.append(event)

    return events

def parse_session(session):
    event = utils.Event(STUDIO_NAME)

    # TIME / DURATION
    start_t = session("span.hc_time > time.hc_starttime").attr('datetime')
    end_t   = session("span.hc_time > time.hc_endtime").attr('datetime')

    if start_t == None: return event
    start_date = dateParser.parse(start_t)
    end_date   = dateParser.parse(end_t)
    duration = utils.duration(start_date, end_date)

    event.date     = start_date
    event.duration = duration

    # INFO
    title = session(".bw-session__name").text()
    level = session(".bw-session__level").text()
    title += " - " + level
    teacher = session(".bw-session__staff").text()

    event.title    = title
    event.teacher  = teacher

    link = session(".bw-widget__signup-now").attr('data-url')
    event.link     = link

    event.price    = STUDIO_PRICE
    event.logo     = STUDIO_LOGO

    # TODO some weird encoding stuff going on, too lazy to fix rn
    #      also remove empty lines n shit
    note = session(".bw-session__description").text()
    event.notes.append(note)

    return event


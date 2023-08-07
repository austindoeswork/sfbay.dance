# local
from db import db
from scrapers import odc
from scrapers import citydance
from scrapers import dmt
import utils
# packages
from datetime import datetime
import pprint
import json

# TODO config
# TODO date stuff, not an index
# TODO ? instagrams for teachers?
ODC_DAYS        = 1
CITY_DANCE_DAYS = 6
DMT_DAYS        = 1
CONFIG_FILE = "./scrape_config.json"

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)


def main():
    c = load_config()
    event_db = db.EventDB(c["db_path"], c["teacher_path"])

    events = []
    dmt_events = []
    odc_events = []
    cd_events = []

    # DMT
    print("dmt: start")
    try:
        dmt_events = dmt.scrape(DMT_DAYS)
        events += dmt_events
    except Exception as error:
        print("dmt:", error)

    # ODC
    print("odc: start")
    try:
        odc_events = odc.scrape(ODC_DAYS)
        events += odc_events
    except Exception as error:
        print("odc:", error)

    #  CITY DANCE
    print("cds: start")
    try:
        cd_events = citydance.scrape(CITY_DANCE_DAYS)
        events += cd_events
    except Exception as error:
        print("cds:", error)

    # TODO archive old events instead of reseting the whole db
    event_db.reset()

    event_db.add_bulk(events)
    print("dmt: ", len(dmt_events))
    print("odc: ", len(odc_events))
    print("cds: ", len(cd_events))

    all_events = event_db.all()

    linkless_teachers = [];
    for e in all_events:
        ev = utils.Event.fromDict(e)
        if ev.teacher_link is None:
            clean_teacher = utils.clean_teacher(ev.teacher)
            linkless_teachers.append(clean_teacher)

    uniq = list(set(linkless_teachers))
    uniq.sort()
    print("LINKLESS TEACHERS:")
    for t in uniq: print(t)



    # TODO rae
    # TODO mood and moves
    # TODO fix dmt

if __name__== "__main__":
    main()


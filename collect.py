# local
from db import db
from scrapers import odc
from scrapers import citydance
from scrapers import dmt
import utils
# packages
from datetime import datetime
import pprint

# TODO config
# TODO date stuff, not an index
# TODO ? instagrams for teachers?
ODC_DAYS        = 1
CITY_DANCE_DAYS = 6
DMT_DAYS        = 1

def main():
    event_db = db.EventDB("./db/events.json")
    event_db.reset()

    events = []

    # DMT
    dmt_events = dmt.scrape(DMT_DAYS)
    event_db.add_bulk(dmt_events)


    # ODC
    odc_events = odc.scrape(ODC_DAYS)
    event_db.add_bulk(odc_events)

    #  CITY DANCE
    cd_events = citydance.scrape(CITY_DANCE_DAYS)
    event_db.add_bulk(cd_events)

    all_events = event_db.all()
    for e in all_events:
        ev = utils.Event.fromDict(e)
        ev.pprint_oneline()

    # TODO rae
    # TODO check for duplicates

if __name__== "__main__":
    main()


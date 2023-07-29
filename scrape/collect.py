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
    event_db = db.EventDB(c["db_path"])

    # TODO archive old events instead of reseting the whole db
    event_db.reset()

    events = []

    # ODC
    odc_events = odc.scrape(ODC_DAYS)
    events += odc_events
    #  return

    # DMT
    dmt_events = dmt.scrape(DMT_DAYS)
    events += dmt_events


    #  CITY DANCE
    cd_events = citydance.scrape(CITY_DANCE_DAYS)
    events += cd_events

    event_db.add_bulk(events)
    print("dmt: ", len(dmt_events))
    print("odc: ", len(odc_events))
    print("cds: ", len(cd_events))

    #  all_events = event_db.all()
    #  for e in all_events:
        #  ev = utils.Event.fromDict(e)
        #  ev.pprint_oneline()

    # TODO rae
    # TODO mood and moves
    # TODO fix dmt

if __name__== "__main__":
    main()


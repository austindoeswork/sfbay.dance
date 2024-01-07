# local
from db import db
from scrapers import odc
from scrapers import lines
from scrapers import citydance
from scrapers import dmt
from scrapers import rae
import utils
# packages
from datetime import datetime
from datetime import timedelta
import pprint
import json

CONFIG_FILE = "./scrape_config.json"

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)


def main():
    c = load_config()
    event_db = db.EventDB(c["db_path"], c["teacher_path"])


    modules = [    \
        odc,       \
        lines,     \
        citydance, \
        dmt,       \
        rae,       \
    ]

    events = []
    event_count = {}

    for module in modules:
        name = module.__name__.split(".")[1]
        print("%s: start" % (name))
        try:
            module_events = module.scrape()
            events += module_events
            event_count[name] = len(module_events)
        except Exception as error:
            print(name, error)

    print(event_count)
    for studio in event_count.keys():
        print("%s: %d" % (studio, event_count[studio]))


    # TODO archive old events instead of reseting the whole db
    event_db.reset()
    event_db.add_bulk(events)
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

    # TODO mood and moves

if __name__== "__main__":
    main()


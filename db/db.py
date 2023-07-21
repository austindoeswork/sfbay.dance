# NOTE is this worth building? should I set up a "real" db?
import os, json, uuid
from dateutil import parser as dateParser

class EventDB:
    def __init__(self, path):
        self.file_path = path
        self.events = {}
        self.load_from_file(path)

    def add(self, event):
        if not event.is_valid():
            # TODO err logging
            print("ERR invalid event")
            event.pprint_safe()
            return

        e_hash = event.hash()
        e_dict = event.__dict__

        self.events[e_hash] = e_dict
        self.persist()
        return

    def add_bulk(self, events):
        for e in events:
            if not e.is_valid():
                # TODO err logging
                print("ERR invalid event")
                event.pprint_safe()
            else:
                e_hash = e.hash()
                e_dict = e.__dict__
                self.events[e_hash] = e_dict
        self.persist()
        return

    def persist(self):
        tempfile = os.path.join(os.path.dirname("/tmp/"), str(uuid.uuid4()))
        with open(tempfile, 'w') as f:
            json.dump(self.events, f, indent=4, sort_keys=True, default=str)

        # rename temporary file replacing old file
        os.rename(tempfile, self.file_path)

    def reset(self):
        self.events = {}
        self.persist()

    def all(self):
        def by_date(x):
            return x["date"]
        all_events = list(self.events.values())
        print(len(all_events))

        return sorted(all_events, key=by_date)

    def filter_date(self, date):
        return

    def filter_location(self, location):
        return

    def load_from_file(self, path):
        print("loading from:", path)
        with open(path, 'r') as f:
            self.events = json.load(f)
        print("events: ", len(self.events))

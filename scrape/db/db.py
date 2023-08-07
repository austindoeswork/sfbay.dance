# NOTE is this worth building? should I set up a "real" db?
import os, json, uuid, csv
from dateutil import parser as dateParser
import utils

class EventDB:
    def __init__(self, path, teacher_path):
        self.file_path = path
        self.events = {}
        self.teachers = {}
        self.load_from_file(path, teacher_path)

    def prep(self, event):
        if event.teacher_link: return

        clean_teacher = utils.clean_teacher(event.teacher)
        if clean_teacher in self.teachers:
            event.teacher_link = self.teachers[clean_teacher]
        return


    def add(self, event):
        if not event.is_valid():
            # TODO err logging
            print("ERR invalid event")
            event.pprint_safe()
            return

        self.prep(event)
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
                self.prep(e)
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

        return sorted(all_events, key=by_date)

    def filter_date(self, date):
        return

    def filter_location(self, location):
        return

    def load_from_file(self, path, teacher_path):
        print("loading from:", path)
        with open(path, 'r') as f:
            self.events = json.load(f)
        with open(teacher_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                name, link = row
                name = name.strip()
                link = link.strip()
                if len(link) <= 0: continue
                self.teachers[name] = link

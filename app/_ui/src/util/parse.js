import strftime from './strftime.js'

function newEventList(title) {
  return {
    title: title,
    events: [],
  }
}

function cleanTitle(title) {
  const delimiterRe = /[^\w-\/\$]/;

  const replacements = [
    [ /IN PERSON/ , "" ],
    [ /Beginner/ , "Beg." ],
    [ /beginner/ , "Beg." ],
    [ /Beginning/ , "Beg." ],
    [ /beginning/ , "Beg." ],
    [ /Intermediate/ , "Int." ],
    [ /intermediate/ , "Int." ],
    [ /Advanced/ , "Adv." ],
    [ /advanced/ , "Adv." ],
  ]

  let newTitle = "";
  let wordMap = {};
  let words = title.split(delimiterRe);

  for (let i = 0; i < words.length; i++) {
    let w = words[i];
    let wLower = w.toLowerCase();
    if (wordMap[wLower]) {
      //
    } else {
      wordMap[wLower] = true;
      newTitle += w;
      if (i < words.length - 1) { newTitle += " " }
    }
  }

  for (let [re, repl] of replacements) {
    newTitle = newTitle.replace(re, repl);
  }

  return newTitle;
}

function parseEvents(data) {
  let events = []; // [ {event}... ]
  let eventsByDate = []; // [ {title: str, events: [ {event}...] }...]
  // TODO sort / classify into days?
  for (let [, value] of Object.entries(data)) {
    // parse date string
    const d = new Date(value["date"]);
    value["date"] = d;
    value["dateStr"] = strftime("%a, %b %e", d)
    value["timeStr"] = strftime("%l:%M %p", d)
    events.push(value);
  }


  // sort events by date
  events.sort((a,b) => {
      return a["date"] - b["date"]
    }
  );

  for (let e of events) {
    e["title"] = cleanTitle(e["title"]);
  }

  let foundDates = {};
  let eventList;
  for (const e of events) {
    const dStr = e["dateStr"]

    if (foundDates[dStr] === undefined) {
      foundDates[dStr] = true;

      if (eventList) {
        eventsByDate.push(eventList)
      }
      eventList = newEventList(dStr);
      eventList.events.push(e);
    } else {
      eventList.events.push(e);
    }
  }
  if (eventList) {
    eventsByDate.push(eventList)
  }

  return { events: events, eventsByDate: eventsByDate };
}

function filterEvents(events, filter) {
  if (filter.length <= 2) { return events; }

  let newEvents = [];
  let f = filter.toLowerCase();

  for (let e of events) {
    const title = e["title"].toLowerCase();
    const teacher = e["teacher"].toLowerCase();
    const location = e["location"].toLowerCase();
    if (title.includes(f) ||
      teacher.includes(f) ||
      location.includes(f)
    ) {
      newEvents.push(e);
    }
  }
  return newEvents;
}

function filterEventsByDate(evsByDate, filter) {
  let ret = [];

  for (let list of evsByDate) {
    let newList = newEventList(list.title);
    let filteredEvents = filterEvents(list.events, filter);

    if (filteredEvents.length === 0) { continue }
    newList.events = filteredEvents;

    ret.push(newList);
  }

  return ret;
}

export { parseEvents, filterEvents, filterEventsByDate };

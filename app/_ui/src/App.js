import React, { Component } from 'react';
import EventBlock from './components/EventBlock.js'

import './App.css';
import './components/EventRow.css'
import './components/EventBlock.css'

import strftime from './util/strftime.js'

class Main extends Component {
  constructor(props) {
    super(props);
    this.state = {
      srcData: {},
      events: [],
      eventsByDate: [],
    }
  }

  newEventList = (title) => {
    return {
      title: title,
      events: [],
    }
  }

  parseData = (data) => {
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

    let foundDates = {};
    let eventList;
    for (const e of events) {
      const dStr = e["dateStr"]

      if (foundDates[dStr] === undefined) {
        foundDates[dStr] = true;

        if (eventList) {
          eventsByDate.push(eventList)
        }
        eventList = this.newEventList(dStr);
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

  componentDidMount() {
    // TODO this should prob be a config var
    // This is the all events object
    fetch('/assets/events.json')
      .then(response => response.json())
      .then(json => {
        const {events, eventsByDate} = this.parseData(json);

        this.setState({
          srcData: json,
          events: events,
          eventsByDate: eventsByDate,
        });
      });
  }

  render() {
    const { eventsByDate } = this.state;
    return (
      <div id="main">
        <div id="events">
          { eventsByDate.map( e => (
              <EventBlock eventList={e} />
          ))}
        </div>
      </div>
    );
  }
}

function App() {
  return (
    <>
      <Main />
    </>
  );
}

export default App;

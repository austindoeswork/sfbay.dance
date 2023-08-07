import React, { Component } from 'react';
import EventBlock from './components/EventBlock.js'
import EventList from './components/EventList.js'
import './App.css';
import parseEvents from './util/parse.js'

import {BrowserView, MobileView} from 'react-device-detect';
// import Carousel from 'react-elastic-carousel';

class Header extends Component {
  constructor(props) {
    super(props);

    this.state = {
    }
  }

  render() {
    return (
      <div id="header">
        IM THE HEADER
      </div>
    )
  }
}

class Main extends Component {
  constructor(props) {
    super(props);
    this.state = {
      srcData: {},
      events: [],
      eventsByDate: [],
    }
  }

  // MAIN API REQUEST
  componentDidMount() {
    // This is the all events object
    fetch('/assets/events.json')
      .then(response => response.json())
      .then(json => {
        const {events, eventsByDate} = parseEvents(json);

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
        <MobileView>
          <div id="mobile">
            { eventsByDate.map( e => (
                <EventBlock eventList={e} />
            ))}
          </div>
        </MobileView>
        <BrowserView>
          <div id="web">
            { eventsByDate.map( e => (
                <EventList eventList={e} />
            ))}
          </div>
        </BrowserView>
      </div>
    );
  }
}

function App() {
  return (
    <div id="body">
      <Header />
      <Main />
    </div>
  );
}

export default App;

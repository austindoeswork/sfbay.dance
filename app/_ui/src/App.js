import React, { Component } from 'react';
import EventBlock from './components/EventBlock.js'
import EventList from './components/EventList.js'
import './App.css';
import parseEvents from './util/parse.js'

import {BrowserView, MobileView} from 'react-device-detect';

import {
  BiSearchAlt2
} from "react-icons/bi"
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
        <div class="header-block">
          <div id="header-logo">
            <img src="/breaker.png"/>
          </div>
          <div id="header-title">
            SFBAY.DANCE
          </div>
        </div>
        <div class="header-block search-wrapper">
          < BiSearchAlt2 />
          <input
             class="search"
             type="search"
             placeholder="search classes"
          />
        </div>
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

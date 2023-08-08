import React, { Component } from 'react';
import EventBlock from './components/EventBlock.js'
import EventList from './components/EventList.js'
import './App.css';
import { parseEvents, filterEventsByDate } from './util/parse.js'

import {BrowserView, MobileView} from 'react-device-detect';

import {
  BiSearchAlt2
} from "react-icons/bi"

class Header extends Component {
  constructor(props) {
    super(props);

    this.state = {
    }
  }

  updateQuery = (e) => {
    const value = e.target.value;
    this.props.updateQuery(value);
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
             value={this.props.query}
             onChange={this.updateQuery}
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
      loaded: false,
      srcData: {},
      events: [],
      eventsByDate: [],
      srcEventsByDate: [],
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
          loaded: true,
          srcData: json,
          events: events,
          eventsByDate: eventsByDate,
          srcEventsByDate: eventsByDate,
        });
      });
  }

  renderEmpty = () => {
    const { loaded } = this.state;
    return (
      <>
        { loaded ?
          (
            <div id="empty">
              <div class="empty-message">
                {"No events found for: " + this.state.query}
              </div>
              <div class="action-btn main-action-btn"
                onClick={() => this.updateQuery("")}
              >
                Clear search
              </div>
            </div>
          ) :
          (
            <div id="empty">
              <div class="empty-message">
                loading...
              </div>
            </div>
          )
        }
      </>
    )
  }

  updateQuery = (query) => {
    const newEvsByDate = filterEventsByDate(
      this.state.srcEventsByDate, query);

    this.setState({
      eventsByDate: newEvsByDate,
      query: query,
    });
  }

  renderMobile(eventsByDate) {
    return (
        <MobileView>
          <div id="mobile">
            { eventsByDate.map( e => (
                <EventBlock title={e.title} events={e.events} />
            ))}
          </div>
        </MobileView>
    );
  }

  renderWeb(eventsByDate) {
    return (
        <BrowserView>
          <div id="web">
            { eventsByDate.map( e => (
                <EventList title={e.title} events={e.events} />
            ))}
          </div>
        </BrowserView>
    );
  }

  render() {
    const { eventsByDate } = this.state;

    let r;
    if (eventsByDate.length === 0) {
      r = this.renderEmpty();
    } else {
      r = <>
        {this.renderMobile(eventsByDate)}
        {this.renderWeb(eventsByDate)}
      </>;
    }

    return (
      <>
        <Header
          query={this.state.query}
          updateQuery={this.updateQuery}
        />
        <div id="main">
          {r}
        </div>
      </>
    );
  }
}

function App() {
  return (
    <div id="body">
      <Main />
    </div>
  );
}

export default App;

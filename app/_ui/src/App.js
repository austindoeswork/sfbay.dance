import React, { Component } from 'react';
import Header from './components/Header.js'
import Filter from './components/Filter.js'
import EventBlock from './components/EventBlock.js'
import EventList from './components/EventList.js'
import './App.css';
import { parseEvents, queryEventsByDate, filterEventsByDate } from './util/parse.js'
import {BrowserView, MobileView} from 'react-device-detect';

import {
  BiX,
  BiStore,
} from "react-icons/bi"


class Main extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loaded: false,
      srcData: {},
      studios: [],
      events: [],
      eventsByDate: [],
      srcEventsByDate: [],
      defaultFilter: {
        studios: [],
      },
      currentFilter: {
        studios: [],
      },
    }
  }

  // MAIN API REQUEST
  componentDidMount() {
    // This is the all events object
    fetch('/assets/events.json')
      .then(response => response.json())
      .then(json => {
        const {events, eventsByDate, studios} = parseEvents(json);

        this.setState({
          loaded: true,
          srcData: json,
          events: events,
          studios: studios,
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
    const newEvsByDate = queryEventsByDate(
      this.state.srcEventsByDate, query);

    this.setState({
      eventsByDate: newEvsByDate,
      query: query,
    });
  }

  updateFilter = (filter) => {
    const newEvsByDate = filterEventsByDate(
      this.state.srcEventsByDate, filter);

    console.log(newEvsByDate);

    this.setState({
      eventsByDate: newEvsByDate,
      currentFilter: filter,
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

    let body;
    if (eventsByDate.length === 0) {
      body = this.renderEmpty();
    } else {
      body = <>
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
        <Filter
          studios={this.state.studios}
          defaultFilter={this.state.defaultFilter}
          currentFilter={this.state.currentFilter}
          updateFilter={this.updateFilter}
        />
        <div id="main">
          {body}
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

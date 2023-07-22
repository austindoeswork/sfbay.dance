import React, { Component } from 'react';
import EventRow from './components/EventRow.js'

import './App.css';
import './components/EventRow.css'

class Main extends Component {
  constructor(props) {
    super(props);
    this.state = {
      srcData: {},
      events: [],
    }
  }

  parseData = (data) => {
    let events = [];
    // TODO sort / classify into days?
    for (const [key, value] of Object.entries(data)) {
      events.push(value);
    }
    return events;
  }

  componentDidMount() {
    // TODO this should prob be a config var
    // This is the all events object
    fetch('/assets/events.json')
      .then(response => response.json())
      .then(json => {
        this.setState({
          srcData: json,
          events: this.parseData(json),
        });
      });
  }

  render() {
    const events = this.state.events

    return (
      <div id="main">
        { events.map( e => (
            <EventRow event={e} />
        ))}
      </div>
    );
  }
}

function App() {
  return (
    <Main />
  );
}

export default App;

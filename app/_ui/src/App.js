import React, { Component } from 'react';
import './App.css';
import EventRow from './components/EventRow.js'

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
    for (const [key, value] of Object.entries(data)) {
      console.log(key, value);
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
    console.log(this.state)
    return (
      <div id="main">
        yo dawgg
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

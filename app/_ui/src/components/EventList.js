import React, { Component } from 'react';
import EventRow from './EventRow.js'
import './EventList.css'

export default class EventList extends Component {

  constructor(props) {
    super(props);
    this.state = {
    }
  }

  componentDidMount() {
  }

  render() {
    const { title, events } = this.props;
    return (
      <div class="list">
        <div class="list-header">
          { title }
        </div>
        <div class="list-body">
          { events.map( e => (
              <EventRow event={e} />
          ))}
        </div>
      </div>
    );
  }
}

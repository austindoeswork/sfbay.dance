import React, { Component } from 'react';
import EventRow from './EventRow.js'
import './EventBlock.css'

import {
  FaCalendarAlt,
} from "react-icons/fa"

export default class EventBlock extends Component {

  constructor(props) {
    super(props);
    this.state = {
      title: props.eventList.title,
      events: props.eventList.events,
    }
  }

  componentDidMount() {
  }

  render() {
    const { title, events } = this.state;
    return (
      <div class="block">
        <div class="block-header">
          <div class="block-date-wrapper">
            <div class="block-date">
              { title }
            </div>
          </div>
        </div>
        <div class="event-list">
          { events.map( e => (
              <EventRow event={e} />
          ))}
        </div>
      </div>
    );
  }
}

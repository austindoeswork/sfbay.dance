import React, { Component } from 'react';
import strftime from '../util/strftime.js'

import {
  FaShareAlt,
  FaInstagram,
} from "react-icons/fa"

export default class EventRow extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      event: props.event,
    }
  }

  componentDidMount() {
  }

  render() {
    const event = this.state.event;
    const timeStr = strftime("%l:%M %P", event["date"])
    return (
      <div class="event">
        <div class="event-logo">
          <img class="event-logo-img" src={event["logo"]}/>
        </div>
        <div class="event-body">
          <div class="event-row">

            <div class="event-item event-teacher"> {event["teacher"]} </div>

            <div class="event-info-block">
              <div class="event-icons">
                <FaInstagram class="event-icon"/>
                <FaShareAlt class="event-icon"/>
              </div>
              <div class="event-item event-date">
                <div class="event-date-item"> { timeStr } </div>
              </div>
              <div class="event-item event-link-wrapper">
                <a class="event-link" href={ event["link"] }> sign up </a>
              </div>
            </div>

          </div>
          <div class="event-row">
            <div class="event-item event-title"> { event["title"] } </div>
          </div>
        </div>
      </div>
    );
  }
}

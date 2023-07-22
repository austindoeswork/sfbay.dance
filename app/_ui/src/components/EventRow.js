import React, { Component } from 'react';
export default class EventRow extends React.Component {
  constructor(props) {
    super(props);
    console.log(props);
    this.state = {
      event: props.event,
    }
  }

  componentDidMount() {
  }

  render() {
    const event = this.state.event;
    return (
      <div class="event">
        <div class="event-row">
          <div class="event-item event-location"> {event["location"]} </div>
          <div class="event-item event-teacher"> {event["teacher"]} </div>
          <div class="event-item event-date"> {event["date"]} </div>
        </div>
        <div class="event-row">
          <div class="event-item event-title"><a href={event["link"]}>{event["title"]}</a></div>
        </div>
      </div>
    );
  }
}

import React, { Component } from 'react';
import strftime from '../util/strftime.js'
import './EventRow.css'

import toast, { toastConfig } from 'react-simple-toasts';
import 'react-simple-toasts/dist/theme/dark.css';
import {
  FaShareAlt,
  FaInstagram,
} from "react-icons/fa"

toastConfig({
  theme: 'dark',
});

export default class EventRow extends Component {
  constructor(props) {
    super(props);
    this.state = {
      event: props.event,
      selected: false,
    }
  }

  toggleSelect = (e) => {
    this.setState({
      selected: !this.state.selected,
    });
  }

  componentDidMount() {
  }

  linkAction = (url) => {
    return (e) => {
      e.stopPropagation();
      window.open(url, "_blank", "noreferrer");
    }
  }

  copyAction = (text) => {
    return (e) => {
      e.stopPropagation();
      console.log("copy text");
      navigator.clipboard.writeText(text)
      toast('link copied!');
    }
  }

  renderActions = (event) => {
    return (
      <div class="actions">
        <div
          class="action-btn main-action-btn"
          onClick={this.linkAction(event["link"])}
        >
          Sign up
        </div>
        <div class="action-block">
          <div
            class="action-btn"
            onClick={this.linkAction("instagram.com")}
          >
            < FaInstagram />
          </div>
          <div
            class="action-btn"
            onClick={this.copyAction(event["link"])}
          >
            < FaShareAlt />
          </div>
        </div>
      </div>

    );
  }

  render() {
    const { event, selected } = this.state;
    const timeStr = strftime("%l:%M %P", event["date"])
    // const actions = selected ? this.renderActions(event) : null;
    const actions = this.renderActions(event);
      // selected ? this.renderActions(event) : null;
    return (
      <div
        className={
          "event" +
          ( selected ? " selected" : "")
        }
        onClick={this.toggleSelect}>
        <div class="event-logo">
          <img class="event-logo-img" alt={event["location"]} src={event["logo"]}/>
        </div>
        <div class="event-body">
            <div class="event-item event-title"> { event["title"] } </div>
            <div class="event-item event-teacher"> {event["teacher"]} </div>
            <div class="event-item event-location"> {event["location"]} </div>
        </div>
        <div class="event-item event-date">
          <div class="event-date-item"> { timeStr } </div>
        </div>
        { actions }
      </div>
    );
  }
}

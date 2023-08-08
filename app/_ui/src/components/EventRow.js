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

  copyText = (id) => {
    console.log("copying:", id);
    var input = document.querySelector("#" + id);

    if (navigator.userAgent.match(/ipad|ipod|iphone/i)) {
      // handle iOS devices
      input.contenteditable = true;
      input.readonly = false;

      var range = document.createRange();
      range.selectNodeContents(input);

      var selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      input.setSelectionRange(0, 999999);
    } else {
      // other devices are easy
      console.log(input);
      input.select()
    }
    let res = document.execCommand('copy');
    console.log(res);
  }

  copyAction = (id) => {
    return (e) => {
      e.stopPropagation();
      console.log("copy text");
      this.copyText(id);
      toast('link copied!');
    }
  }

  renderActions = (event) => {
    const inputId = "link_"+event["id"]
    return (
      <div class="actions">
        <div
          class="action-btn main-action-btn"
          onClick={this.linkAction(event["link"])}
        >
          Sign up
        </div>
        <div class="action-block">
          { event["teacher_link"] ? (
            <div
              class="action-btn"
              onClick={this.linkAction(event["teacher_link"])} >
              < FaInstagram />
            </div>
          ) : null
          }
          <div
            class="action-btn"
            onClick={this.copyAction(inputId)}
          >
            < FaShareAlt />
            <input
              id={inputId}
              class="hidden"
              value={event["link"]}
            />
          </div>
        </div>
      </div>

    );
  }

  render() {
    const { event, selected } = this.state;
    const timeStr = strftime("%l:%M %P", event["date"])
    const actions = this.renderActions(event);
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

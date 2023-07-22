import React, { Component } from 'react';
export default class EventRow extends React.Component {
  constructor(props) {
    super(props);
    console.log(props);
    // this.state = {
      // data: {},
    // }
  }

  componentDidMount() {
  }

  render() {
    return (
      <div class="eventRow">
        event row
      </div>
    );
  }
}

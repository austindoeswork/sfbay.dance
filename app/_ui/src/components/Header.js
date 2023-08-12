import React, { Component } from 'react';
import './Header.css';

import {
  BiSearchAlt2
} from "react-icons/bi"

export default class Header extends Component {
  constructor(props) {
    super(props);

    this.state = {
    }
  }

  updateQuery = (e) => {
    const value = e.target.value;
    this.props.updateQuery(value);
  }

  render() {
    return (
      <div id="header">
        <div class="header-block">
          <div id="header-logo">
            <img src="/breaker.png"/>
          </div>
          <div id="header-title">
            SFBAY.DANCE
          </div>
        </div>
        <div class="header-block search-wrapper">
          < BiSearchAlt2 />
          <input
             class="search"
             type="search"
             placeholder="search classes"
             value={this.props.query}
             onChange={this.updateQuery}
          />
        </div>
      </div>
    )
  }
}

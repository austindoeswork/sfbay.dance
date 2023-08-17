import React, { Component } from 'react';
import './Header.css';
import checkMobile from '../util/misc.js'

import {
  BiSearchAlt2,
  BiX
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
          { checkMobile() ? null :
            <div id="header-title">
              SFBAY.DANCE
            </div>
          }
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
          { !this.props.query || this.props.query.length <= 0 ? null :
            <BiX class="x-clear" onClick={()=>this.props.updateQuery("")} />
          }
        </div>
      </div>
    )
  }
}

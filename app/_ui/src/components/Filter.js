import React, { Component } from 'react';
import './Filter.css';

import {
  BiX,
  BiStore,
} from "react-icons/bi"

export default class Filter extends Component {
  constructor(props) {
    super(props);
    this.state = {
      currentModal: null,
    };
  }

  componentDidMount() {
  }

  toggleModal = (modal) => {
    const current = this.state.currentModal;

    if (current === modal) {
      this.setState({
        currentModal: null,
      });
      return;
    }

    this.setState({
      currentModal: modal,
    });
  }

  clearStudios = (filter, updateFilter) => {
    let newFilter = filter;
    newFilter.studios = [];
    updateFilter(newFilter);
  }

  toggleStudio = (studio, filter, updateFilter) => {
    let newFilter = filter;
    let newStudios = filter.studios;
    if (newStudios.includes(studio)) {
      newStudios = newStudios.filter(s => s !== studio);
    } else {
      newStudios.push(studio);
    }
    newFilter.studios = newStudios;
    updateFilter(newFilter);
  }

  renderStudio = (studio, currentFilter, updateFilter) => {
    const selected = currentFilter.studios.includes(studio.name);
    const classes = "studio-row " + (selected ? "selected" : "");

    return (
      <div
           class={classes}
           onClick={()=>this.toggleStudio(studio.name, currentFilter, updateFilter)}
      >
        <div class="studio-logo">
          <img class="studio-logo-img" alt={studio.name} src={studio.logo}/>
        </div>
        <div class="studio-name">
          {studio.name}
        </div>
      </div>
    )

  }

  renderStudioModal(studios, currentFilter, updateFilter) {
    const len = currentFilter.studios.length;
    let modalTitle;
    if (len <= 0) {
      modalTitle = "Filter by studio";
    } else {
      modalTitle = (
        <>
          <div> {len} selected </div>
          <div
            class="clear-selection-btn"
            onClick={ () => this.clearStudios(currentFilter, updateFilter) }
          >
            Clear All
          </div>
        </>
      );
    }


    return (
      <div id="studio-modal" class="modal">
        <div class="modal-header">
          <div class="modal-title">{modalTitle}</div>
          <div class="x-clear modal-exit" onClick={() => this.toggleModal(null)}>
            <BiX />
          </div>
        </div>
        <div class="modal-content">
          {studios.map(s =>
            this.renderStudio(s, currentFilter, updateFilter)
          )}
        </div>
      </div>
    );
  }


  render() {
    const { studios, defaultFilter, currentFilter, updateFilter } = this.props;
    const { currentModal } = this.state;
    let newFilter = currentFilter;
    const btnClass = "filter-btn" +
      (currentFilter.studios.length > 0 ?
      " selected" : "");

    return (
      <div id="filter">
        <div class={btnClass}
             onClick={() => this.toggleModal("studios")}>
          <BiStore />
          studios
        </div>
        { currentModal !== null ?
          <div id="modal-backdrop"
               onClick={() => this.toggleModal(null)}>
          </div> : null
        }
        { currentModal === "studios" ?
          this.renderStudioModal(studios, currentFilter, updateFilter)
          : null
        }
      </div>
    );
  }
}

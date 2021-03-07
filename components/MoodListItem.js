import React from "react";
import styles from "../styles/ListItem.module.css";

/**
 * @typedef MoodListItemProps
 * @memberof MoodListItem
 * @property {String} name - mood name
 * @property {Number} id - mood id
 * @property {Number} key - mood id
 * @property {Function} setOpen - function to set OpenMood
 * @property {Boolean} selected - true if if is equivalent to openMood value
 */

/**
 * Component representing a list of moods
 * @class MoodListItem
 * @param {MoodListItemProps} props
 */
const MoodListItem = (props) => {
  let displayName =
    props.name.length > 35
      ? props.name.substring(0, 36).concat("...")
      : props.name;

  return (
    <div className={styles.item} onClick={props.setOpen}>
      <div
        className={`${styles.name} ${
          props.selected ? "font-weight-bold" : styles.link
        }`}
      >
        {displayName}
      </div>
    </div>
  );
};

export default MoodListItem;

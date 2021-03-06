import React from "react";
import styles from "../styles/ListItem.module.css";

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

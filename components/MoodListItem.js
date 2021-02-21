import React from "react";
import styles from "../styles/ListItem.module.css";

const MoodListItem = (props) => {
  return (
    <div className={styles.item} onClick={props.setOpen}>
        <div className={`${styles.name} ${props.selected ? "font-weight-bold" : styles.link}`}>{props.name}</div>
    </div>
  );
};

export default MoodListItem;

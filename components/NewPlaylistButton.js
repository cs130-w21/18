import React from "react";
import Link from 'next/link'
import styles from "../styles/ListItem.module.css";

const NewPlaylistButton = (props) => {
  return (
    <div className={styles.item} onClick={props.getNewPlaylist}>
        <div className={`${styles.name} ${styles.link}`}>+ Create a new playlist from this mood</div>
    </div>
  );
};

export default NewPlaylistButton;

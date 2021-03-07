import React from "react";
import Link from "next/link";
import styles from "../styles/ListItem.module.css";

/**
 * @typedef NewPlaylistButtonProps
 * @memberof NewPlaylistButton
 * @property {String} mood - indicates a user is logged in and a mood is selected
 * @property {Function} getNewPlaylist - function to get a new playlist
 */

/**
 * Button component to create a new playlist
 * @class NewPlaylistButton
 * @param {NewPlaylistButtonProps} props
 */
const NewPlaylistButton = (props) => {
  return (
    <div className={styles.item} onClick={props.getNewPlaylist}>
      <div className={`${styles.name} ${styles.link}`}>
        + Create a new playlist from this mood
      </div>
    </div>
  );
};

export default NewPlaylistButton;

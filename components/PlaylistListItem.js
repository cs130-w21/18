import React from "react";
import Link from "next/link";
import styles from "../styles/ListItem.module.css";

/**
 * @typedef PlaylistListItemProps
 * @memberof PlaylistListItem
 * @property {Number} key - index referencing each playlist
 * @property {String} name - playlist name
 * @property {Number} id - playlist id
 */

/**
 * Component representing a list of playlists
 * @class PlaylistListItem
 * @param {PlaylistListItemProps} props
 */
const PlaylistListItem = (props) => {
  return (
    <Link href={`/playlist/${props.id}`}>
      <div className={styles.item}>
        <div className={`${styles.name} ${styles.link}`}>{props.name}</div>
      </div>
    </Link>
  );
};

export default PlaylistListItem;

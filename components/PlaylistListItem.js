import React from "react";
import Link from 'next/link'
import styles from "../styles/ListItem.module.css";

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

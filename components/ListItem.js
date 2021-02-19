import React from "react";
import Link from 'next/link'
import styles from "../styles/ListItem.module.css";

const ListItem = (props) => {
  return (<>
    <Link href={`/${props.type}/${props.id}`}>
      <div key={props.id} className={styles.item}>
          <div className={styles.name}>{props.name}</div>
      </div>
    </Link>
  </>);
};

export default ListItem;
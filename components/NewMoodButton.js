import React from "react";
import Link from "next/link";
import styles from "../styles/ListItem.module.css";

/**
 * @typedef NewMoodButtonProps
 * @memberof NewMoodButton
 * @property {String} questionnaireUrl - URL to the questionnaire page
 */

/**
 * Button component to create a new mood
 * @class NewMoodButton
 * @param {NewMoodButtonProps} props
 */
const NewMoodButton = (props) => {
  return (
    <Link href={props.questionnaireUrl}>
      <div className={styles.item}>
        <div className={`${styles.name} ${styles.link}`}>
          + Create a new mood
        </div>
      </div>
    </Link>
  );
};

export default NewMoodButton;

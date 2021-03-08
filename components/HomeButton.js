import React from "react";
import styles from "../styles/HomeButton.module.css";
import { Button } from "react-bootstrap";

/**
 * @typedef HometButtonProps
 * @memberof HomeButton
 */

/**
 * Component representing a navigate-to-home button
 * @class HomeButton
 */
const LoginLogoutButton = (props) => {
  return (
    <Button
      className={styles.homebutton}
      variant="outline-primary"
      onClick={props.homeFunction}
    >
      Home
    </Button>
  );
};

export default HomeButton;

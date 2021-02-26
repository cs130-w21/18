import React from "react";
import styles from "../styles/LoginLogoutButton.module.css";
import { Button } from "react-bootstrap";

const LoginLogoutButton = (props) => {
  if (props.loggedIn) {
    return (
      <Button
        className={styles.loginlogoutbutton}
        variant="outline-dark"
        onClick={props.logoutFunction}
      >
        Log Out
      </Button>
    );
  }
  return (
    <Button
      className={styles.loginlogoutbutton}
      variant="outline-primary"
      onClick={props.loginFunction}
    >
      Log In With Spotify
    </Button>
  );
};

export default LoginLogoutButton;

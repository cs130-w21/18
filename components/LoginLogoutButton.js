import React from "react";
import styles from "../styles/MusaicHeader.module.css";
import { Button } from "react-bootstrap";

/**
 * @typedef LoginLogoutButtonProps
 * @memberof LoginLogoutButton
 * @property {Boolean} loggedIn - indicates whether a user is logged in
 * @property {Function} loginFunction - function to process user login
 * @property {Function} logoutFunction - function to process user logout
 */

/**
 * Component representing a login/logout button
 * @class LoginLogoutButton
 * @param {LoginLogoutButtonProps} props
 */
const LoginLogoutButton = (props) => {
  if (props.loggedIn) {
    return (
      <Button
        className={styles.headerbutton}
        variant="outline-dark"
        onClick={props.logoutFunction}
      >
        Log Out
      </Button>
    );
  }
  return (
    <Button
      className={styles.headerbutton}
      variant="outline-primary"
      onClick={props.loginFunction}
    >
      Log In With Spotify
    </Button>
  );
};

export default LoginLogoutButton;

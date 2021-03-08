import React from "react";
import styles from "../styles/MusaicHeader.module.css";
import LoginLogoutButton from "./LoginLogoutButton";
import Button from "react-bootstrap/Button";
import Link from "next/link";

/**
 * @typedef MusaicHeaderProps
 * @memberof MusaicHeader
 * @property {Boolean} loggedIn - indicates whether a user is logged in
 * @property {Function} loginFunction - function to process user login
 * @property {Function} logoutFunction - function to process user logout
 */

/**
 * Component to standardize overall application header
 * @class MusaicHeader
 * @param {MusaicHeaderProps} props
 */
const MusaicHeader = (props) => (
  <header className={styles.musaicheader}>
    <div className={styles.headerdiv}>
      <div className={styles.musaic}>Musaic</div>
      {props.loggedIn && props.switchViewLink && props.switchViewText ? (
        <Link href={props.switchViewLink}>
          <Button
            variant="outline-primary"
            className={`${styles.headerbutton} mr-1`}
          >
            {props.switchViewText}
          </Button>
        </Link>
      ) : (
        ""
      )}
      <LoginLogoutButton
        loggedIn={props.loggedIn}
        loginFunction={props.loginFunction}
        logoutFunction={props.logoutFunction}
      />
    </div>
  </header>
);

export default MusaicHeader;

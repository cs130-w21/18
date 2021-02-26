import React from "react";
import styles from "../styles/MusaicHeader.module.css";
import LoginLogoutButton from "./LoginLogoutButton";

const MusaicHeader = (props) => (
  <header className={styles.musaicheader}>
    <div className={styles.headerdiv}>
      <div className={styles.musaic}>Musaic</div>
      <LoginLogoutButton
        loggedIn={props.loggedIn}
        loginFunction={props.loginFunction}
        logoutFunction={props.logoutFunction}
      />
    </div>
  </header>
);

export default MusaicHeader;

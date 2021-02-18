import React from "react";
import Link from "next/link";
import { Button } from "react-bootstrap";
import { Container, Row, Col } from "react-bootstrap";
import PageHead from "../components/head";
import MusaicHeader from "../components/MusaicHeader";
import styles from "../styles/Home.module.css";

const Home = (props) => {
  return (
    <>
      <PageHead/>
      <div className="page_container">
        <MusaicHeader/>
        <div className={styles.big_flex_container}>
          <div className={`${styles.row} ${styles.row_1}`}>
            <div className={`${styles.intro_box} ${styles.box}`}>
              Welcome!
            </div>
            <div className={`${styles.instructions_box} ${styles.box}`}>
              Here's how this works!
            </div>
          </div>
          <div className={`${styles.row} ${styles.row_2}`}>
            <div className={`${styles.playlists_box} ${styles.box}`}>
              Here are your cool playlists!
            </div>
            <div className={`${styles.moods_box} ${styles.box}`}>
              Here are your moods!
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;

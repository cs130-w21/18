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
              Welcome, {props.username}!
            </div>
            <div className={`${styles.instructions_box} ${styles.box}`}>
              <p><b>Here's how this works:</b> Answer a few questions, and we'll make you a brand new Spotify playlist
              based on your mood and your favorite music. You can also create a relatable mood and associate it with your playlist,
              then share your musical moods with friends!</p>
            </div>
          </div>
          <div className={`${styles.row} ${styles.row_2}`}>
            <div className={`${styles.playlists_box} ${styles.box} ${styles.bottom_box}`}>
              <div className={styles.lower_box_text}>
                Your Playlists
              </div>
              <div className={styles.list}>
                {props.playlistList}
              </div>
            </div>
            <div className={`${styles.bottom_box} ${styles.box}`}>
              <div className={styles.lower_box_text}>
                Your Moods
              </div>
              <div className={styles.list}>
                {props.moodList}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;

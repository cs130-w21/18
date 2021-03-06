import React, { useState } from "react";
import { cloneDeep } from "lodash";
import Alert from "react-bootstrap/Alert";
import PageHead from "../components/head";
import MusaicHeader from "../components/MusaicHeader";
import PlaylistListItem from "../components/PlaylistListItem";
import MoodListItem from "../components/MoodListItem";
import NewMoodButton from "../components/NewMoodButton";
import NewPlaylistButton from "../components/NewPlaylistButton";
import styles from "../styles/Home.module.css";

/* Render the home page. */

const Home = (props) => {
  const [openMood, setOpenMood] = useState(
    props.moods.size > 0 ? props.moods.keys().next().value : null
  );
  const [moods, setMoods] = useState(props.moods);

  const moodListItems = [];
  moods.forEach((mood, id) => {
    moodListItems.push(
      <MoodListItem
        name={mood.name}
        id={id}
        key={id}
        setOpen={() => setOpenMood(id)}
        selected={id === openMood}
      />
    );
  });

  const makeNewPlaylist = async (moodId) => {
    let moodName = moods.get(moodId).name;
    let newPlaylist = await props.getNewPlaylist(moodId, moodName);
    if (newPlaylist.id === null) {
      return;
    }
    setMoods((oldState) => {
      let playlists = cloneDeep(moods.get(moodId).playlists);
      playlists.push(newPlaylist);
      return new Map(oldState).set(moodId, {
        name: moodName,
        playlists: playlists,
      });
    });
  };

  const playlistBoxContents = () => {
    if (props.loggedIn) {
      if (openMood !== null) {
        // User is logged in and a mood is selected
        return (
          <>
            <NewPlaylistButton
              mood={openMood}
              getNewPlaylist={() => makeNewPlaylist(openMood)}
            />
            <div className={styles.list}>
              {moods.get(openMood).playlists.map((playlist) => (
                <PlaylistListItem
                  key={playlist.idx}
                  name={playlist.name}
                  id={playlist.id}
                />
              ))}
            </div>
          </>
        );
      } else {
        // Logged in, but user has no moods
        return (
          <div className={styles.list}>
            Create a mood to get your first custom playlist!
          </div>
        );
      }
    } else {
      // Box is empty if user is not logged in.
      return "";
    }
  };

  return (
    <>
      <PageHead />
      <div className="page_container">
        <MusaicHeader
          loggedIn={props.loggedIn}
          loginFunction={props.loginFunction}
          logoutFunction={props.logoutFunction}
        />
        {props.error !== "" ? (
          <Alert
            variant="primary"
            className="justify-content-md-center w-50 mx-auto mb-0"
          >
            {props.error}
          </Alert>
        ) : (
          ""
        )}
        <div className={styles.big_flex_container}>
          <div className={`${styles.row} ${styles.row_1}`}>
            <div className={`${styles.intro_box} ${styles.box}`}>
              {props.username ? `Welcome, ${props.username}!` : "Welcome!"}
            </div>
            <div className={`${styles.instructions_box} ${styles.box}`}>
              <p>
                <b>Here's how this works:</b> Answer a few questions, and we'll
                make you a brand new Spotify playlist based on your mood and
                musical taste! You'll also get a mood, which you can reuse to
                create more playlists from your responses. Or, share your moods
                with friends so they can create their own playlists from your
                musical mood!
              </p>
            </div>
          </div>
          <div className={`${styles.row} ${styles.row_2}`}>
            <div
              className={`${styles.playlists_box} ${styles.box} ${styles.bottom_box}`}
            >
              <div className={styles.lower_box_text}>Your Moods</div>
              {props.loggedIn ? (
                <>
                  <NewMoodButton questionnaireUrl={props.questionnaireUrl} />
                  <div className={styles.list}>{moodListItems}</div>
                </>
              ) : (
                "Log in with Spotify to create your first mood!"
              )}
            </div>
            <div className={`${styles.bottom_box} ${styles.box}`}>
              <div className={styles.lower_box_text}>Your Playlists</div>
              {playlistBoxContents()}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;

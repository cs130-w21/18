import React, { useState } from "react";
import { cloneDeep } from "lodash";
import Alert from "react-bootstrap/Alert";
import PageHead from "../components/head";
import MoodListItem from "../components/MoodListItem";
import NewPlaylistButton from "../components/NewPlaylistButton";
import HomeButton from "../components/HomeButton";
import styles from "../styles/Home.module.css";

/* render the explore page. */

/**
 * @typedef ExploreProps
 * @memberof Explore
 * @property {String} homeUrl - url for questionnaire page
 * @property {Function} getNewPlaylist - function to get a new playlist
 * @property {Object} moods - a user's moods to explore
 * @property {String} error - error message
 */

/**
 * component to display and handle explore page functionality
 * @class Explore
 * @param {ExploreProps} props
 */
const Explore = (props) => {
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

  /**
   * Method to create a new playlist
   * @memberof Explore
   * @param {String} moodId
   */
  const makeNewPlaylist = async (moodId) => {
    let moodName = moods.get(moodId).name;
    let newPlaylist = await props.getNewPlaylist(moodId, moodName);
    if (newPlaylist.id === null) {
      return;
    }
  };

  /**
   * Method to display playlists in a box
   * @memberof Home
   */
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

  const saveMoodContents = () => {
    if (props.loggedIn) {
      if (openMood !== null) {
        // User is logged in and a mood is selected
        return (
          <>
            <SaveMoodButton
              mood={openMood}
              saveMood={() => saveMood(openMood)}
            />
          </>
        );
      } else {
        // Logged in, but user has no moods
        return (
          <div className={styles.list}>
            No moods to explore right now!
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
      </div>
    </>
  );
};

export default Explore;

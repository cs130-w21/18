import React from "react";
import PageHead from "../components/head";
import styles from "../styles/playlist.module.css";
import { useRouter } from "next/router";

/**
 * Component to display playlist
 * @class Playlist
 */
const Playlist = () => {
  const router = useRouter();
  const { playlist } = router.query;

  return (
    <>
      <PageHead />
      <div className={`${styles.playlistContainer}`}>
        <div className={`${styles.embed} ${styles.playlistText}`}>
          <p>Here's your custom playlist!</p>
        </div>
        <div className={`${styles.embed}`}>
          <iframe
            src={`https://open.spotify.com/embed/playlist/${playlist}`}
            width="300"
            height="380"
            frameBorder="0"
            allowtransparency="true"
            allow="encrypted-media"
          ></iframe>
        </div>
      </div>
    </>
  );
};

export default Playlist;

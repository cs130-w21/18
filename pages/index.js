import React, { useState } from "react";
import { useRouter } from "next/router";
import { parseCookies, setCookie, destroyCookie } from "nookies";
import Home from "../views/home";
import {
  fetchPlaylistsFromMood,
  fetchUserMoods,
  requestNewPlaylist,
} from "../lib/fetch";

/**
 * This function handles the login for the home page.
 * It passes information to the home page view and returns that
 * React component with the parameters filled in.
 * @class Index
 * @param {Object} context - React context
 */
export async function getServerSideProps(context) {
  const cookies = parseCookies(context);

  return (
    <div>
      {/* Todo: Pull this out into its own component so we can reuse it */}
      <Head>
        <title>Custom Mood-Based Playlists</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Todo: automatically redirect user if they're not logged in. */}
      <Link href='/login'>
        <Button>Log in</Button>
      </Link>

      <p>Hello!</p>
      <Link href="/questionnaire">
        <Button>
          Generate your playlist!
        </Button>
      </Link>

      <Link href="/explore">
        <Button>
          Explore
        </Button>
      </Link>
    </div>
  );
};

  // Otherwise, try to load username & jwt from cookies.
  username = cookies.username ?? null;
  jwt = cookies.jwt ?? null;

  // Load user data if user is logged in.
  let data = {},
    error = "";
  if (username && jwt) {
    // Request moods from the backend.
    try {
      const moodsResponse = await fetchUserMoods(jwt);
      if (moodsResponse.error !== "") {
        throw moodsResponse.error;
      }
      // Extract the information we want to use from the response.
      data.moods = moodsResponse.moods.map((mood) => ({
        mood_name: mood.mood_name,
        mood_id: mood.mood_id,
        playlists: [],
      }));
      // Request playlists that go with each mood.
      // Make all the requests in parallel.
      await Promise.all(
        data.moods.map(async (mood) => {
          const playlistsResponse = await fetchPlaylistsFromMood(
            jwt,
            mood.mood_id
          );
          if (playlistsResponse.error !== "") {
            throw playlistsResponse.error;
          }
          // Extract the information we want and associate the playlists with the mood.
          mood.playlists = playlistsResponse.playlists.map((playlist) => ({
            id: playlist.uri.replace("spotify:playlist:", ""),
            idx: playlist.idx,
            name: `${mood.mood_name} ${playlist.idx}`,
          }));
        })
      );
    } catch (err) {
      if (err === "Access Token expired") {
        error = "Your session has expired. Please log in again.";
      } else {
        error =
          "Sorry, we're having trouble accessing your playlists right now. Please try again later.";
      }
    }
  }

  // Pass data to the page via props
  return {
    props: {
      data,
      username,
      jwt,
      error,
    },
  };
}

export default function HomeController(props) {
  const router = useRouter();
  const [error, setError] = useState(props.error);

  const moods = new Map();
  // Convert moods and playlists into a map.
  if (!error && props.username && props.jwt) {
    try {
      props.data.moods.forEach((mood) => {
        moods.set(mood.mood_id, {
          name: mood.mood_name,
          playlists: mood.playlists,
        });
      });
    } catch {
      setError(
        "Sorry, we're having trouble accessing your playlists right now. Please try again later."
      );
    }
  }

  const getNewPlaylist = async (moodID, moodName) => {
    const { jwt } = parseCookies();

    const newPlaylist = {
      name: "",
      id: null,
      idx: null,
    };
    try {
      const playlistResponse = await requestNewPlaylist(jwt, moodID, moodName);
      if (playlistResponse.error !== "") {
        throw playlistResponse.error;
      }
      newPlaylist.id = playlistResponse.playlist.uri.replace(
        "spotify:playlist:",
        ""
      );
      newPlaylist.idx = playlistResponse.playlist.idx;
      newPlaylist.name = `${moodName} ${playlistResponse.playlist.idx}`;
    } catch {
      setError(
        "Sorry, we couldn't make you a new playlist. Please try again later."
      );
    }

    return newPlaylist;
  };

  /**
   * Component logs the user in via Spotify and stores user information
   * @memberof Index
   */
  const loginFunction = async () => {
    fetch("https://musaic-13018.herokuapp.com/login/appdetails")
      .then((response) => response.json())
      .then(
        (data) => {
          const redurl = new URL("https://accounts.spotify.com/authorize");
          redurl.searchParams.append("client_id", data.client_id);
          redurl.searchParams.append("response_type", "code");
          redurl.searchParams.append("redirect_uri", data.redirect_uri);
          redurl.searchParams.append("scope", data.scopes);
          window.location.href = redurl.href;
        },
        (err) => {}
      );
  };

  /**
   * Component logs the user out and destroys cookies
   * @memberof Index
   */
  const logoutFunction = () => {
    // Remove cookies
    destroyCookie(null, "jwt");
    destroyCookie(null, "username");
    // Reload so all previous user data goes away.
    router.reload();
  };

  return (
    <Home
      loggedIn={props.username && props.jwt}
      username={props.username}
      loginFunction={loginFunction}
      logoutFunction={logoutFunction}
      questionnaireUrl={"/questionnaire"}
      getNewPlaylist={getNewPlaylist}
      moods={moods}
      error={error}
    />
  );
}

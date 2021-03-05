import React from "react";
import { useRouter } from "next/router";
import { parseCookies, setCookie, destroyCookie } from "nookies";
import Home from "../views/home";
import { fetchHomePageData, requestNewPlaylist } from "../lib/fetch";

/* This function handles the login for the home page. It passes information to the home page view and returns that
 * React component with the parameters filled in.
 */
export async function getServerSideProps(context) {
  const cookies = parseCookies(context);

  let username = null,
    jwt = null;
  // If the user is coming from Spotify (username & jwt are in params), store their username and jwt in cookies.
  if (context.query.username && context.query.jwt) {
    // Don't update user if there's already one logged in.
    if (
      typeof cookies.username === "undefined" &&
      typeof cookies.jwt === "undefined"
    ) {
      setCookie(context, "jwt", context.query.jwt);
      setCookie(context, "username", context.query.username);
    }
    // This removes the parameters from the URL, because leaving them in causes issues.
    return {
      redirect: {
        destination: "/",
        permanent: true,
      },
    };
  }

  // Otherwise, try to load username & jwt from cookies.
  username = cookies.username ?? null;
  jwt = cookies.jwt ?? null;

  // Load user data if user is logged in.
  let data = {},
    error = "";
  if (username && jwt) {
    // Request moods and playlists from the backend.
    try {
      const response = await fetchHomePageData(jwt);
      console.log(JSON.stringify(response));
      if (response.error !== "") {
        throw response.error;
      }
      data = response.data;
    } catch {
      error =
        "Sorry, we're having trouble accessing your playlists right now. Please try again later.";
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

  let error = "";
  const moods = new Map();
  // Convert moods and playlists into a map.
  if (!props.error && props.username && props.jwt) {
    try {
      props.data.created_moods.forEach((mood) => {
        moods.set(mood.mood_id, {
          name: mood.mood_name,
          playlists: [],
        });
      });

      // TODO: Map playlists to moods.
      // testData.playlists.forEach((playlist) => {
      //   if (!moods.has(playlist.mood_id)) {
      //     // If this playlist's mood doesn't exist for whatever reason, skip it.
      //     return;
      //   }
      //   moods.get(playlist.mood_id).playlists.push(playlist);
      // });
    } catch {
      error =
        "Sorry, we're having trouble accessing your playlists right now. Please try again later.";
    }
  }

  const getNewPlaylist = async (moodId) => {
    // Will get user ID, then provide mood ID and user ID in this function call
    // TODO: Implement this function.
    const newPlaylist = await requestNewPlaylist();
    newPlaylist.mood_id = moodId;
    return newPlaylist;
  };

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
        (error) => {}
      );
  };

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
      error={props.error || error}
    />
  );
}

import React, { useEffect } from "react";
import { useRouter } from "next/router";
import { parseCookies, setCookie, destroyCookie } from "nookies";
import Home from "../views/home";
import { fetchHomePageData, requestNewPlaylist } from "../lib/fetch";
// import LoginPageController from "./login.js"

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

  // TODO: Make back-end requests.
  const data = await fetchHomePageData();

  // Pass data to the page via props
  return {
    props: {
      data,
      username,
      jwt,
    },
  };
}

export default function HomeController(props) {
  const router = useRouter();

  // TEST DATA
  const testData = {
    playlists: [
      { name: "Heavy metal for studying", id: 123456, mood_id: 333333 },
      { name: "Elevator music", id: 111111, mood_id: 444444 },
      { name: "Pump-up operas", id: 654321, mood_id: 111111 },
      { name: "People talking slowly", id: 444444, mood_id: 222222 },
      { name: "Just bad music", id: 555555, mood_id: 222222 },
      { name: "My Friday Playlist", id: 777777, mood_id: 111111 },
    ],
    moods: [
      { name: "It's a beautiful day!", id: 111111 },
      { name: "Studying", id: 333333 },
      { name: "Graduating over Zoom", id: 444444 },
      { name: "(Thinking about) Working Out", id: 555555 },
      { name: "Post-130 Midterm", id: 666666 },
      { name: "Lounging", id: 222222 },
    ],
  };

  // TODO: Replace this when API calls are implemented.
  // Associate playlists with moods and index moods by id.
  const moods = new Map();
  testData.moods.forEach((mood) => {
    moods.set(mood.id, {
      name: mood.name,
      playlists: [],
    });
  });
  testData.playlists.forEach((playlist) => {
    if (!moods.has(playlist.mood_id)) {
      // Shouldn't happen.
      return;
    }
    moods.get(playlist.mood_id).playlists.push(playlist);
  });

  const getNewPlaylist = async (moodId) => {
    // Will get user ID, then provide mood ID and user ID in this function call
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
    />
  );
}

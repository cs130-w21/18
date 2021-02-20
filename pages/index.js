import React from "react";
import Home from "../views/home";
import { fetchHomePageData, requestNewPlaylist } from "../lib/fetch";

/* This function handles the login for the home page. It passes information to the home page view and returns that
 * React component with the parameters filled in.
 */

export default function HomeController(props) {

  // TEST DATA
  const testData = {
    username: "User",
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
    ]
  }

  // TODO: Replace this when API calls are implemented.
  // Associate playlists with moods and index moods by id.
  const moods = new Map();
  testData.moods.forEach((mood) => {
    moods.set(mood.id, {
      name: mood.name,
      playlists: []
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

  return (
    <Home
      username={testData.username}
      questionnaireUrl={'/questionnaire'}
      getNewPlaylist={getNewPlaylist}
      moods={moods}
    />
  );
};

export async function getServerSideProps(context) {
  // TODO: Make back-end requests.
  const data = await fetchHomePageData();
  // Pass data to the page via props
  return { props: { data } }
}

import React from "react";
import Home from "../views/home";
import ListItem from "../components/ListItem";
import { fetchHomePageData } from "../lib/fetch";

export default function HomeController(props) {

  // Test code
  const testData = {
    username: "Will",
    playlists: [
      { name: "Elevator music", id: 111111 },
      { name: "Heavy metal for studying", id: 123456 },
      { name: "People talking slowly", id: 444444 },
      { name: "Pump-up operas", id: 654321 },
      { name: "Just bad music", id: 555555},
      { name: "Will's Friday Playlist", id: 777777 },
    ],
    moods: [
      { name: "Wallowing", id: 222222 },
      { name: "Mad at the World", id: 333333 },
      { name: "It's a beautiful day!", id: 111111 },
    ]
  }

  let playlistList = testData.playlists.map(playlist => <ListItem type="playlist" name={playlist.name} id={playlist.id}/>);
  let moodList = testData.moods.map(mood => <ListItem type="mood" name={mood.name} id={mood.id}/>);;

  return (
    <Home
      username={testData.username}
      questionnaireUrl={'/questionnaire'}
      playlistList={playlistList}
      moodList={moodList}
    />
  );
};

export async function getServerSideProps(context) {
  const data = await fetchHomePageData();
  // Pass data to the page via props
  return { props: { data } }
}

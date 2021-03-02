import React from "react";
import PageHead from "../components/head";

const Playlist = (props) => {
  return (<>
    <PageHead/>
    <div>
      <p>Here's your custom playlist!</p>
      <iframe src="https://open.spotify.com/embed/album/1DFixLWuPkv3KT3TnV35m3"></iframe>
    </div>
  </>);
};
  
export default Playlist;
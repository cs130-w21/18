import { parseCookies } from "nookies";

const axios = require("axios");

// This file handles all API calls and exports simple functions for accessing backend data.

export async function requestNewPlaylist() {
  // TODO: Request a new playlist for this user and a given mood.
  return { name: "Brand new playlist!", id: 505050 };
}

export async function fetchHomePageData(jwt) {
  // Fetch any moods and playlists from the backend.
  const data = {
    error: "",
    data: null,
  };
  try {
    const response = await axios.get(
      "https://musaic-13018.herokuapp.com/api/v1/user/moods",
      { headers: { Authorization: `Bearer ${jwt}` } }
    );
    // console.log(response.status)
    // console.log(response.data)
    if (response.data.error) {
      throw response.data.error;
    } else if (response.status != 200) {
      throw response.statusText;
    }
    data.data = response.data;
  } catch (error) {
    data.error = error;
    return data;
  }

  // TODO: Fetch playlists and add to result.
  return data;
}

export async function submitQuestionnaire(moodName, responses) {
  // Make PUT request to send questionnaire responses to the backend
  const cookies = parseCookies();
  // console.log("cookies: " + JSON.stringify(cookies))
  // console.log("submitting these responses: " + JSON.stringify(responses))

  const data = {
    error: "",
    data: null,
  };
  try {
    const response = await axios.put(
      `https://musaic-13018.herokuapp.com/api/v1/mood/mood?name=${moodName}`,
      responses,
      { headers: { Authorization: `Bearer ${cookies.jwt}` } }
    );
    // console.log(response.status)
    // console.log(response.data)
    if (response.data.error) {
      throw response.data.error;
    } else if (response.status != 200) {
      throw response.statusText;
    }
    data.data = response.data;
  } catch (error) {
    data.error = error;
  }

  return data;
}

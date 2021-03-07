import { parseCookies } from "nookies";

const axios = require("axios");

// This file handles all API calls and exports simple functions for accessing backend data.

var baseURL = "https://musaic-13018.herokuapp.com/api/v1";
/**
 * @module Queries
 */

/**
 * This function requests a new playlist from the backend
 * @param {String} jwt - JSON Web Token
 * @param {String} moodID - mood identifier
 * @param {String} moodName - a mood's name
 */
export async function requestNewPlaylist(jwt, moodID, moodName) {
  // Request a new playlist for this user and a given mood.
  const data = {
    error: "",
    playlist: null,
  };
  try {
    let response = await axios.get(
      `${baseURL}/playlist/playlist-from-mood?mood_id=${moodID}&mood_name=${moodName}`,
      { headers: { Authorization: `Bearer ${jwt}` } }
    );
    // console.log(response);
    if (response.data.error) {
      throw response.data.error;
    } else if (response.status != 200) {
      throw response.statusText;
    } else if (response.data.mood_id && response.data.mood_id != moodID) {
      throw "Wrong mood id returned";
    }
    data.playlist = response.data;
  } catch (error) {
    // console.log(error);
    data.error = error;
  }
  return data;
}

/**
 * This function fetches playlists associated with a given mood
 * @memberof Fetch
 * @param {String} jwt - JSON Web Token
 * @param {String} moodID - mood identifier
 */
export async function fetchPlaylistsFromMood(jwt, moodID) {
  const data = {
    error: "",
    playlists: null,
  };
  try {
    let response = await axios.get(
      `${baseURL}/playlist/playlists?mood_id=${moodID}`,
      { headers: { Authorization: `Bearer ${jwt}` } }
    );
    if (response.data.error) {
      throw response.data.error;
    } else if (response.status != 200) {
      throw response.statusText;
    } else if (response.data.mood_id && response.data.mood_id != moodID) {
      throw "Wrong mood ID returned";
    }
    data.playlists = response.data;
  } catch (error) {
    data.error = error;
  }
  return data;
}

/**
 * This function fetches any moods belonging to this user from the backend
 * @param {String} jwt - JSON Web Token
 */
export async function fetchUserMoods(jwt) {
  const data = {
    error: "",
    moods: null,
  };
  // Request all moods belonging to this user.
  try {
    const response = await axios.get(`${baseURL}/user/moods`, {
      headers: { Authorization: `Bearer ${jwt}` },
    });
    // console.log("response.data" + JSON.stringify(response.data))
    if (response.data.error) {
      throw response.data.error;
    } else if (response.status != 200) {
      throw response.statusText;
    }

    data.moods = response.data.created_moods;
    // Combine created_moods and external_moods, avoiding duplicates.
    response.data.external_moods.forEach((e_mood) => {
      if (
        !response.data.created_moods.some(
          (c_mood) => c_mood.mood_id === e_mood.mood_id
        )
      ) {
        data.moods.push(e_mood);
      }
    });
  } catch (error) {
    // console.log(error)
    data.error = error;
  }
  return data;
}

/**
 * This function puts user information from the questionnaire to the backend
 * @param {String} moodName - a mood's name
 * @param {Object} responses - user's responses from the questionnaire excluding moodName
 */
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
      `${baseURL}/mood/mood?name=${moodName}`,
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

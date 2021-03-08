import axios from "axios";
import * as fetch from "../lib/fetch.js";

// A suite of tests to check server response processing in fetch.js

jest.mock("axios");

// TEST CASE 1: fetchUserMoods processes returned data correctly
test("fetchUserMoods convert mood response correctly", () => {
  // Mock backend response
  const axiosResponse = {
    status: 200,
    statusText: "OK",
    data: {
      created_moods: [
        {
          mood_id: 32,
          mood_name: "Test Mood 1",
          params: {
            danceability: [0.0, 1.0, 0.6],
            energy: [0.0, 1.0, 0.6],
            instrumentalness: [0.0, 1.0, 0.7],
            speechiness: [0.0, 1.0, 0.2],
            valence: [0.0, 1.0, 0.5],
          },
        },
        {
          mood_id: 39,
          mood_name: "Test! Test!",
          params: {
            danceability: [0.0, 1.0, 0.6],
            energy: [0.0, 1.0, 0.6],
            instrumentalness: [0.0, 1.0, 0.7],
            speechiness: [0.0, 1.0, 0.2],
            valence: [0.0, 1.0, 0.5],
          },
        },
        {
          mood_id: 40,
          mood_name: "1234",
          params: {
            danceability: [0.0, 1.0, 0.1],
            energy: [0.0, 1.0, 0.2],
            instrumentalness: [0.0, 1.0, 0.3],
            speechiness: [0.0, 1.0, 0.4],
            valence: [0.0, 1.0, 0.5],
          },
        },
      ],
      external_moods: [
        {
          mood_id: 30,
          mood_name: "External mood",
          params: {
            danceability: [0.0, 1.0, 0.6],
            energy: [0.0, 1.0, 0.6],
            instrumentalness: [0.0, 1.0, 0.7],
            speechiness: [0.0, 1.0, 0.2],
            valence: [0.0, 1.0, 0.5],
          },
        },
      ],
    },
  };
  axios.get.mockResolvedValue(axiosResponse);

  const correctOutput = {
    error: "",
    moods: [
      {
        mood_id: 32,
        mood_name: "Test Mood 1",
        params: {
          danceability: [0.0, 1.0, 0.6],
          energy: [0.0, 1.0, 0.6],
          instrumentalness: [0.0, 1.0, 0.7],
          speechiness: [0.0, 1.0, 0.2],
          valence: [0.0, 1.0, 0.5],
        },
      },
      {
        mood_id: 39,
        mood_name: "Test! Test!",
        params: {
          danceability: [0.0, 1.0, 0.6],
          energy: [0.0, 1.0, 0.6],
          instrumentalness: [0.0, 1.0, 0.7],
          speechiness: [0.0, 1.0, 0.2],
          valence: [0.0, 1.0, 0.5],
        },
      },
      {
        mood_id: 40,
        mood_name: "1234",
        params: {
          danceability: [0.0, 1.0, 0.1],
          energy: [0.0, 1.0, 0.2],
          instrumentalness: [0.0, 1.0, 0.3],
          speechiness: [0.0, 1.0, 0.4],
          valence: [0.0, 1.0, 0.5],
        },
      },
      {
        mood_id: 30,
        mood_name: "External mood",
        params: {
          danceability: [0.0, 1.0, 0.6],
          energy: [0.0, 1.0, 0.6],
          instrumentalness: [0.0, 1.0, 0.7],
          speechiness: [0.0, 1.0, 0.2],
          valence: [0.0, 1.0, 0.5],
        },
      },
    ],
  };

  return fetch
    .fetchUserMoods(123)
    .then((data) => expect(data).toEqual(correctOutput));
});

// TEST CASE 2: fetchUserMoods reports error received
test("fetchUserMoods should report error in API response", () => {
  // Mock backend response
  const axiosResponse = {
    status: 500,
    statusText: "INTERNAL SERVER ERROR",
    data: {
      created_moods: [],
      external_moods: [],
      error: "An error occurred",
    },
  };
  axios.get.mockResolvedValue(axiosResponse);

  const correctOutput = {
    error: "An error occurred",
    moods: null,
  };

  return fetch
    .fetchUserMoods(123)
    .then((data) => expect(data).toEqual(correctOutput));
});

// TEST CASE 3: fetchPlaylistsFromMood processes playlists correctly
test("fetchPlaylistsFromMood should process playlist response correctly", () => {
  // Mock backend response
  const axiosResponse = {
    status: 200,
    statusText: "OK",
    data: [
      {
        idx: 1,
        mood_id: 15,
        uri: "spotify:playlist:0z3fVofHoQKNeqZulMexbg",
      },
      {
        idx: 2,
        mood_id: 15,
        uri: "spotify:playlist:5Eij6nP76TtSt10Lwluaob",
      },
      {
        idx: 3,
        mood_id: 15,
        uri: "spotify:playlist:1FnGmN4kA2ueEwCqaosVDf",
      },
    ],
  };
  axios.get.mockResolvedValue(axiosResponse);

  const correctOutput = {
    error: "",
    playlists: [
      {
        idx: 1,
        mood_id: 15,
        uri: "spotify:playlist:0z3fVofHoQKNeqZulMexbg",
      },
      {
        idx: 2,
        mood_id: 15,
        uri: "spotify:playlist:5Eij6nP76TtSt10Lwluaob",
      },
      {
        idx: 3,
        mood_id: 15,
        uri: "spotify:playlist:1FnGmN4kA2ueEwCqaosVDf",
      },
    ],
  };

  return fetch
    .fetchPlaylistsFromMood(123, 15)
    .then((data) => expect(data).toEqual(correctOutput));
});

// TEST CASE 4:  requestNewPlaylist processes returned playlist correctly
test(" requestNewPlaylist processes returned playlist correctly", () => {
  // Mock backend response (sample of playlist response)
  const axiosResponse = {
    status: 200,
    statusText: "OK",
    data: {
      idx: 2,
      mood_id: "15",
      tracks: [
        {
          album: {
            album_type: "ALBUM",
            external_urls: {
              spotify: "https://open.spotify.com/album/3XzbVl7oibSdnmpCGzCK6A",
            },
            href: "https://api.spotify.com/v1/albums/3XzbVl7oibSdnmpCGzCK6A",
            id: "3XzbVl7oibSdnmpCGzCK6A",
          },
        },
        {
          album: {
            album_type: "ALBUM",
            external_urls: {
              spotify: "https://open.spotify.com/album/2vTelM2ZV20cLPqQwfWhYa",
            },
            href: "https://api.spotify.com/v1/albums/2vTelM2ZV20cLPqQwfWhYa",
            id: "2vTelM2ZV20cLPqQwfWhYa",
          },
        },
      ],
      uri: "spotify:playlist:1IVSv8wtcuQwLFTUthFfWY",
    },
  };
  axios.get.mockResolvedValue(axiosResponse);

  const correctOutput = {
    error: "",
    playlist: {
      idx: 2,
      mood_id: "15",
      tracks: [
        {
          album: {
            album_type: "ALBUM",
            external_urls: {
              spotify: "https://open.spotify.com/album/3XzbVl7oibSdnmpCGzCK6A",
            },
            href: "https://api.spotify.com/v1/albums/3XzbVl7oibSdnmpCGzCK6A",
            id: "3XzbVl7oibSdnmpCGzCK6A",
          },
        },
        {
          album: {
            album_type: "ALBUM",
            external_urls: {
              spotify: "https://open.spotify.com/album/2vTelM2ZV20cLPqQwfWhYa",
            },
            href: "https://api.spotify.com/v1/albums/2vTelM2ZV20cLPqQwfWhYa",
            id: "2vTelM2ZV20cLPqQwfWhYa",
          },
        },
      ],
      uri: "spotify:playlist:1IVSv8wtcuQwLFTUthFfWY",
    },
  };

  return fetch
    .requestNewPlaylist(123, 15, "mood")
    .then((data) => expect(data).toEqual(correctOutput));
});

// TEST CASE 5: submitQuestionnaire processes returned mood correctly
test("submitQuestionnaire should process returned mood correctly", () => {
  // Mock backend response
  const axiosResponse = {
    status: 200,
    statusText: "OK",
    data: {
      danceability: [0, 1, 0.28],
      energy: [0, 1, 0.5],
      instrumentalness: [0, 1, 0.5],
      mood_id: 50,
      speechiness: [0, 1, 0.71],
      valence: [0, 1, 0.5],
    },
  };
  axios.put.mockResolvedValue(axiosResponse);

  const correctOutput = {
    error: "",
    data: {
      danceability: [0, 1, 0.28],
      energy: [0, 1, 0.5],
      instrumentalness: [0, 1, 0.5],
      mood_id: 50,
      speechiness: [0, 1, 0.71],
      valence: [0, 1, 0.5],
    },
  };

  const questionnaireResponses = {
    danceability: [0.0, 1.0, 0.28],
    instrumentalness: [0.0, 1.0, 0.5],
    speechiness: [0.0, 1.0, 0.71],
    valence: [0.0, 1.0, 0.5],
    energy: [0.0, 1.0, 0.5],
  };

  return fetch
    .submitQuestionnaire(123, "Test mood", questionnaireResponses)
    .then((data) => expect(data).toEqual(correctOutput));
});

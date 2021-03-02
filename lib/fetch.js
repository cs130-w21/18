import { parseCookies, setCookie, destroyCookie } from "nookies";

const axios = require('axios');
// API calls will go here
export async function requestNewPlaylist() {
  // Request a new playlist for this user and a given mood.
  return {name: "Brand new playlist!", id: 505050};
}

export async function fetchHomePageData() {
  // Fetch any user data from the backend
  // const res = await fetch(`https://.../data`)
  // const data = await res.json()
  return {};
}

export async function submitQuestionnaire(responses) {
  // Make POST request to send questionnaire responses to the backend
  // TODO: Add JWT in to headers after that information is stored in the frontend
  const cookies = parseCookies();
  console.log({ cookies });

  // PUT Request
  axios.put("https://musaic-13018.herokuapp.com/api/v1/mood/mood", {
    headers: {"Authorization" : `Bearer ${cookies.jwt}`},
    body: responses
  })

  // GET Request to test that PUT request was successful
  axios.get("https://musaic-13018.herokuapp.com/api/v1/mood/mood", {
    headers: {"Authorization" : `Bearer ${cookies.jwt}`},
    body: responses
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });

  return {};
}

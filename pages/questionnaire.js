import React, { useState } from "react";
import { useRouter } from "next/router";
import Questionnaire from "../views/questionnaire";
import { submitQuestionnaire } from "../lib/fetch";
var _ = require("lodash");

/**
 * @typedef QuestionnaireSettings
 * @memberof Questionnaire
 * @property {String} name - mood name
 * @property {number[]} danceability - danceability min, max, target
 * @property {number[]} instrumentalness - instrumentalness min, max, target
 * @property {number[]} speechiness - speechiness min, max, target
 * @property {number[]} valence - positivity measure min, max, target
 * @property {number[]} energy - energy min, max, target
 */
const defaultSettings = {
  // attribute: [min, max, target]
  name: "moodName",
  danceability: [0.0, 1.0, 0.5],
  instrumentalness: [0.0, 1.0, 0.5],
  speechiness: [0.0, 1.0, 0.5],
  valence: [0.0, 1.0, 0.5],
  energy: [0.0, 1.0, 0.5],
};

/**
 * Component to handle processing of user input
 * @memberof Questionnaire
 * @param {*} props
 */
const QuestionnaireController = (props) => {
  const router = useRouter();
  const [error, setError] = useState("");

  const submitResponses = async (responses) => {
    let moodName = responses.name;
    let paramResponses = _.omit(responses, ["name"]);

    try {
      const response = await submitQuestionnaire(moodName, paramResponses);
      if (response.error !== "") {
        throw response.error;
      }
    } catch (err) {
      console.log(err);
      if (err === "Access Token expired") {
        setError("Your session has expired. Please log in again.");
      } else {
        setError(
          "Sorry, we couldn't submit your responses. Please try again later."
        );
      }

      return;
    }

    router.push("/");
  };

  return (
    <Questionnaire
      defaultSettings={defaultSettings}
      submitResponses={submitResponses}
      error={error}
    />
  );
};

export default QuestionnaireController;

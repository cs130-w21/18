import React, { useState } from "react";
import { useRouter } from "next/router";
import Questionnaire from "../views/questionnaire";
import { submitQuestionnaire } from "../lib/fetch";
var _ = require("lodash");

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

  const defaultSettings = {
    // attribute: [min, max, target]
    name: "moodName",
    danceability: [0.0, 1.0, 0.5],
    instrumentalness: [0.0, 1.0, 0.5],
    speechiness: [0.0, 1.0, 0.5],
    valence: [0.0, 1.0, 0.5],
    energy: [0.0, 1.0, 0.5],
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

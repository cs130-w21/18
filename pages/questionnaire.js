import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Questionnaire from "../views/questionnaire";
import { submitQuestionnaire } from "../lib/fetch";

const QuestionnaireController = (props) => {
  const router = useRouter();

  const submitResponses = (responses) => {
    responses = JSON.stringify(responses);
    console.log(responses);
    submitQuestionnaire(responses);

    router.push('/playlist/2');
  };

  const defaultSettings = {
    // attribute: [min, max, target]
    name: "moodName",
    danceability: [0.3, 0.7, 0.5],
    instrumentalness: [0.3, 0.7, 0.5],
    popularity: [0.3, 0.7, 0.5],
    speechiness: [0.3, 0.7, 0.5],
    valence: [0.3, 0.7, 0.5],
    energy: [0.3, 0.7, 0.5],
  };

  return (
    <Questionnaire
      defaultSettings={defaultSettings}
      submitResponses={submitResponses}
    />
  );
};

export default QuestionnaireController;

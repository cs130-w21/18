import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Questionnaire from "../views/questionnaire";
import { submitQuestionnaire } from "../lib/fetch";

const QuestionnaireController = (props) => {
  const router = useRouter();

  const submitResponses = (responses) => {
    console.log(responses);
    submitQuestionnaire();

    router.push('/playlist/2');
  };

  const defaultSettings = {
    danceability: 0.5,
    instrumentalness: 0.5,
    popularity: 0.5,
    speechiness: 0.5,
    valence: 0.5,
    energy: 0.5
  };

  return (
    <Questionnaire
      defaultSettings={defaultSettings}
      submitResponses={submitResponses}
    />
  );
};

export default QuestionnaireController;

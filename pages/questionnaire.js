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
    energy: 5
  };

  return (
    <Questionnaire
      defaultSettings={defaultSettings}
      submitResponses={submitResponses}
    />
  );
};

export default QuestionnaireController;

import React from "react";
import Home from "../views/home";
import { fetchHomePageData } from "../lib/fetch";

export default function HomeController() {
  return (
    <Home
      questionnaireUrl={'/questionnaire'}
    />
  );
};

export async function getServerSideProps(context) {
  const data = await fetchHomePageData();
  // Pass data to the page via props
  return { props: { data } }
}

/**
 * @jest-environment jsdom
 */

import React from "react";
import { render } from "@testing-library/react";
import HomeController from "../pages/index.js";

// A test suite to check the basic functionality of the home page.

// TEST CASE 1: Home page renders moods and user greeting
test("Home page should render moods and user greeting", () => {
  const data = {
    moods: [
      {
        mood_name: "Test mood 1",
        mood_id: 1,
        playlists: [
          { id: "6fwIXqpQNiKvR1wWB0wvzp", idx: 1, name: "Playlist 1" },
          { id: "0z3fVofHoQKNeqZulMexbg", idx: 2, name: "Playlist 2" },
        ],
      },
      { mood_name: "Test! Test!", mood_id: 39, playlists: [] },
      { mood_name: "1234", mood_id: 40, playlists: [] },
    ],
  };

  const { getByText } = render(
    <HomeController data={data} username="Test Master" jwt="1234" error="" />
  );

  const mood1 = getByText(/Test mood 1/);
  expect(mood1).toBeInTheDocument();

  const mood2 = getByText(/Test! Test!/);
  expect(mood2).toBeInTheDocument();

  const mood3 = getByText(/1234/);
  expect(mood3).toBeInTheDocument();

  const greeting = getByText(/Welcome, Test Master!/);
  expect(greeting).toBeInTheDocument();
});

// TEST CASE 2: Home page renders playlists
test("Home page should render moods and user greeting", () => {
  const data = {
    moods: [
      {
        mood_name: "Happy Mood",
        mood_id: 1,
        playlists: [
          { id: "6fwIXqpQNiKvR1wWB0wvzp", idx: 1, name: "Happy Mood 1" },
          { id: "0z3fVofHoQKNeqZulMexbg", idx: 2, name: "Happy Mood 2" },
        ],
      },
    ],
  };

  const { getByText } = render(
    <HomeController data={data} username="Test Master" jwt="1234" error="" />
  );

  const playlist1 = getByText(/Happy Mood 1/);
  expect(playlist1).toBeInTheDocument();

  const playlist2 = getByText(/Happy Mood 2/);
  expect(playlist2).toBeInTheDocument();
});

// TEST CASE 3: Home page displays error message if input data is malformed
test("Home page should display error message if input data is malformed", () => {
  const data = {};

  const { getByText } = render(
    <HomeController data={data} username="Test Master" jwt="1234" error="" />
  );

  const error = getByText(
    /Sorry, we're having trouble accessing your playlists right now. Please try again later./
  );
  expect(error).toBeInTheDocument();
});

// TEST CASE 4: Home page displays error message if one is provided
test("Home page should display error message if one is provided", () => {
  const data = {
    moods: [],
  };

  const { getByText } = render(
    <HomeController
      data={data}
      username="Test Master"
      jwt="1234"
      error="A terrible error happened!"
    />
  );

  const error = getByText(/A terrible error happened!/);
  expect(error).toBeInTheDocument();
});

import Head from "next/head";
import React from "react";

/**
 * Component to standardize Page Headers
 * @class PageHead
 */
const PageHead = () => (
  <Head>
    <title>Custom Mood-Based Playlists</title>
    <link rel="icon" href="/favicon.ico" />
    <link rel="preconnect" href="https://fonts.gstatic.com" />
    <link
      href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap"
      rel="stylesheet"
    />
  </Head>
);

export default PageHead;

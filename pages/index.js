import Head from 'next/head'
import React from 'react';
import Link from 'next/link';
import { Button } from 'react-bootstrap';

export default function Home() {

  return (
    <div>
      {/* Todo: Pull this out into its own component so we can reuse it */}
      <Head>
        <title>Custom Mood-Based Playlists</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Todo: automatically redirect user if they're not logged in. */}
      <Link href='/login'>
        <Button>Log in</Button>
      </Link>

      <p>Hello!</p>
      <Link href="/questionnaire">
        <Button>
          Generate your playlist!
        </Button>
      </Link>

      <Link href="/explore">
        <Button>
          Explore
        </Button>
      </Link>
    </div>
  );
};

export async function getServerSideProps(context) {
  // Fetch any user data from the backend
  // const res = await fetch(`https://.../data`)
  // const data = await res.json()

  // Pass data to the page via props
  return { props: { data: '' } }
}

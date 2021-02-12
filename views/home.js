import React from "react";
import Link from "next/link";
import { Button } from "react-bootstrap";
import PageHead from "../components/head";

const Home = (props) => {
  return (
    <>
      <PageHead/>
      <div>
        {/* Todo: automatically redirect user if they're not logged in. */}
        <Link href='/login'>
          <Button>Log in</Button>
        </Link>

        <p>Hello!</p>
        <Link href={props.questionnaireUrl}>
          <Button>
            Generate your playlist!
          </Button>
        </Link>
      </div>
    </>
  );
};

export default Home;
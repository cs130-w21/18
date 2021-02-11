import React from "react";
import Link from 'next/link';
import "../styles/Login.module.css";

const LoginPage = (props) => {
  if (props.loggedIn) {
    return <Redirect to="/" />;
  }

  return (
    <div>
      <p>Hello!</p>
      <Link href="/questionnaire">
        <button type="button" className="btn btn-primary">
          Log in!
        </button>
      </Link>
    </div>
  );
};

export default LoginPage;

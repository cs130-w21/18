import React from "react";
import Link from "next/link";
import PageHead from "../components/head";
import "../styles/Login.module.css";

const LoginPage = (props) => {
  return (<>
    <PageHead/>
    <div>
      <p>Hello!</p>
      <Link href={props.loginUrl}>
        <button type="button" className="btn btn-primary">
          Log in!
        </button>
      </Link>
    </div>
  </>);
};

export default LoginPage;

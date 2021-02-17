import React, { useEffect } from "react";
import Link from 'next/link';
import "../styles/Login.module.css";

const LoginPage = (props) => {
  if (props.loggedIn) {
    return <Redirect to="/" />;
  } else {
    useEffect(() => {
      fetch('https://musaic-13018.herokuapp.com/login/appdetails')
      .then(response => response.json())
      .then(data => {
        const redurl = new URL("https://accounts.spotify.com/authorize");
        redurl.searchParams.append("client_id",data.client_id);
        redurl.searchParams.append("response_type","code");
        redurl.searchParams.append("redirect_uri",data.redirect_uri);
        redurl.searchParams.append("scope",data.scopes);
        window.location.href = redurl.href}/*this.setState({ client_id:data.client_id, scopes:data.scopes, redirect_uri:data.redirect_uri })*/);
        //window.location.href="https://google.com";
      }, []);
  }

  /*fetch('https://musaic-13018.herokuapp.com/login/appdetails')
    .then(response => response.json())
    .then(data => {
      const redurl = new URL("https://accounts.spotify.com/authorize");
      redurl.searchParams.append("client_id",data.client_id);
      redurl.searchParams.append("response_type","code");
      redurl.searchParams.append("redirect_uri",data.redirect_uri);
      redurl.searchParams.append("scope",data.scopes);
      window.location.href = redurl.href}/*this.setState({ client_id:data.client_id, scopes:data.scopes, redirect_uri:data.redirect_uri }));*/


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

//get app details from https://musaic-13018.herokuapp.com/login/appdetails
//
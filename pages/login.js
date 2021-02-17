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
      .then((data) => {
        const redurl = new URL("https://accounts.spotify.com/authorize");
        redurl.searchParams.append("client_id",data.client_id);
        redurl.searchParams.append("response_type","code");
        redurl.searchParams.append("redirect_uri",data.redirect_uri);
        redurl.searchParams.append("scope",data.scopes);
        //return <div>redurl.href</div>;
        window.location.href = redurl.href;
        },
        (error) => {});
      }, [])
    return null;
  }

};

export default LoginPage;
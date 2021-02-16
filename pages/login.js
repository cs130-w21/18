import React from "react";
import LoginPage from "../views/login";

const LoginPageController = (props) => {
  if (props.loggedIn) {
    return <Redirect to="/" />;
  }

  return (
    <LoginPage
      loginUrl={'/questionnaire'}
    />
  );
};

export default LoginPageController;

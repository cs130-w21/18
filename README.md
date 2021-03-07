# Musaic Backend API

[![Build Status](https://travis-ci.org/cs130-w21/18.svg?branch=be/master)](https://travis-ci.org/cs130-w21/18)
[![Release](https://img.shields.io/github/v/release/cs130-w21/18?label=release)](https://github.com/cs130-w21/18/releases/latest)

Welcome to Musaic's Backend API. Our backend is reponsible for maintaining and updating user information and allowing new users to onboard. 

## Building our app

Please note that our app is not meant to be built locally by a user. For the best experience with our app, please visit [our frontend website](https://test-fe-130.herokuapp.com/).

If you still want to build our backend app locally, read on. 

A pre-requisite for our app is Python3 (>=3.6).

You must set some required environment variables, as so:
```
export ALLOW_ORIGINS='*'
export DATABASE_URL=<DATABASE_URL>
export FRONT_END_URI='https://test-fe-130.herokuapp.com'
export JWT_SECRET='psst...idontlikeshawnmendez...sshhh'
export SPOTIFY_REDIRECT_URI='https://musaic-13018.herokuapp.com/login/callback'
``` 

You can find a database URL to use [here](test.sh). 

You'll also need to install dependencies via `pip install -r requirements.txt` from the project root directory. We recommend using Python's `venv` module to containerize your Python environment.

Finally, you can run `gunicorn main:app` which will launch our backend application. 

Note that the backend app will not work when run locally like this. For one, certain sensitive information stored in environment variables is only available on our Heroku dynos. It is not good practice to disclose such information (client IDs and secrets for Spotify, for example). Therefore, we have not exposed this data anywhere on our repo.

## Triggering test suite

To trigger the test suite, run:

```
./test.sh
```

from the project root directory. This performs many of the steps outlined above. The server is terminated, however, after testing completes. Any installed dependencies are also deleted to reduce clutter. 

Testing is performed via `pytest`. 

Triggering a test is a safe operation. It can be done locally by anyone. Any changes to the app state are only made to the staging database, and so production remains unaffected. The tests do not cover API endpoints that require Spotify authentication. Obtaining a Spotify access token requires manually logging in to Spotify. We have decided, therefore, to cover this aspect of our codebase through manual integration tests instead of automated unit tests.

## Deployment

Deployment is done via Travis CI. As mentioned before, builds are not meant to be done manually (in a local environment). Travis CI creates a build and tests it whenever a commit is pushed onto any backend branch. See [the Travis build script](./.travis.yml) for more information on the specification of the test job (under the `jobs` action). 

Whenever a commit is pushed onto be/master (and the testing job succeeds without error) the build is deployed to our Heroku staging dyno. Whenever a **tagged** commit is pushed to the repo (need not be just be/master) that commit is built and deployed to production. So, care must be taken to only tag commits on be/master, to prevent unstaged, untested code from being deployed to production. See [the Travis build script](./.travis.yml) for more information on deployment (under the `deploy` action).


## Documentation

We have documented our API endpoints via Sphinx. See the html pages created [here](docs/build/html).

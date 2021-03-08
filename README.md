[![Build Status](https://travis-ci.com/cs130-w21/18.svg?branch=fe%2Fmaster)](https://travis-ci.com/cs130-w21/18)

This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started for Developers

To run the app locally, first make sure Node.js and npm are installed. Run `npm install` to install all the dependencies.
Then run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result. Pages auto-update as you edit the files.

## About Next.js

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

## CI/CD

Musaic is automatically deployed to https://test-fe-130.herokuapp.com every time a commit is pushed to the branch fe/master that builds
successfully and passes our automated tests. Any push to GitHub will trigger the Travis CI script, found in .travis.yml, which builds the production version of the app and runs all Jest tests.

To manually trigger a build of the production version locally, you can use `npm run build`. To manually run the tests, use
`npm run test`.

You can manually trigger a build of the production frontend app and run our unit tests by visiting https://travis-ci.com/github/cs130-w21/18, selecting the most recent build of the branch fe/master, and clicking "Restart build."

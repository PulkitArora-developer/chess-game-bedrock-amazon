const Dotenv = require('dotenv-webpack');

module.exports = {
  plugins: [
    new Dotenv({
      path: '.env', // Path to your .env file
      systemvars: true, // Use system variables if no .env file is found
    }),
  ],
};

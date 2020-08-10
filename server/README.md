# Steps to build the server side with node.js

1) initialize as an npm package `npm init -y`

2) install base dependencies `npm i express cors morgan helmet`  
express -> for the server  
cors -> cross origin domain sharing... apparently we need the right cors headers for such access (https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)  
morgan -> used for logging  
helmet -> for secure headers  

3) install dev dependencies `npm i -D eslint nodemon`  
eslint -> for linting  
nodemon -> for a live server (i think)

4) build a simple express app in /src/index.js

5) set up a start script and the linter in /src/package.json

6) set up eslint in the server dir `npx eslint --init`  
go through the questions with the following answers)  
To check syntax, find problems, and enforce style  
CommonJS (require/exports)  
None of these  
No  
Node  
Use a popular style guide  
Airbnb  
Javascript

7) start the server in the /server dir `npm run dev`
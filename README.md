# nomama

## Goal
Design, build and deploy a web app that can keep track of our expenses. The prices, quantity, and the date of the goods should be taken from the shop receipt. Preferably, the technologies used should be free for personal use. 

## Implementation
>❗Design change to a framework in python.

We decided on using [Flask](https://flask.palletsprojects.com/en/1.1.x/) together with [Dash/Plotly](https://dash.plotly.com/).

Setting up a development server:  

Install requirements:  
~~~
pip install -r requirements.txt
~~~

Set the environment variables:  
~~~
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run
~~~

## Deployment
The webapp is deployed on Pythonanywhere. The deployment is set to be automatic via github webhooks. A 'push' event on the github repo triggers the update to the server.

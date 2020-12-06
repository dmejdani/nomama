# nomama

## Goal
Design, build and deploy a web app that can keep track of our expenses. The prices, quantity, and the date of the goods should be taken from the shop receipt. Preferably, the technologies used should be free for personal use. 

## Implementation

Using [Flask](https://flask.palletsprojects.com/en/1.1.x/) together with [Dash/Plotly](https://dash.plotly.com/).

## Setting up a development server:  

Install requirements:  
~~~
pip install -r requirements.txt
~~~

Create initial default.db sqlite database:
~~~
python _create_db.py
~~~
*Note: This empties the database!*

Create a .env file at the project root for the environment variables. Similar to the following:
~~~
export WEBHOOK_SECRET=secret_string
export SQLALCHEMY_DATABASE_URI="sqlite:///default.db"
export SECRET_KEY=a-very-very-secret-key
~~~

Set the environment variables in the terminal for a local server. *Do not do this for production!*
~~~
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run
~~~

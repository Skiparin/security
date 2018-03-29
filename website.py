from flask import Flask
from flask_simplelogin import SimpleLogin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import (create_engine, Column, String, Text, Integer,
		Float, DateTime, Boolean, BIGINT, ARRAY, JSON, ForeignKey)
from sqlalchemy.orm import sessionmaker

def db_connect():
		"""
		Connect to database where we'll save properties.
		"""
		return create_engine(URL(**{
		'drivername': 'postgres',
		'host': 'localhost',
		'port': '54320',
		'username': 'spider',
		'password': 'secret',
		'database': 'website'
}))

def website_login(user):
		conn = db_connect().connect()
		sql = "select id from users where username = '" + user.get('username') + "' and password = '" + user.get('password') + "';"
		result = conn.execute(sql)
		#"user = {'username': 'foo', 'password': 'bar'}"
		# do the authentication here, it is up to you!
		# query your database, check your user/passwd file
		# connect to external service.. anything.
		if result.fetchone():
			return True  # Allowed
		return False  # Denied

app = Flask(__name__)
SimpleLogin(app, login_checker=website_login)

@app.route('/')
def hello_world():
    return 'Welcome, you have logged in.'
from flask import Flask, render_template, redirect, url_for, request
from flask_simplelogin import SimpleLogin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import (create_engine, Column, String, Text, Integer,
		Float, DateTime, Boolean, BIGINT, ARRAY, JSON, ForeignKey)
from sqlalchemy.orm import sessionmaker
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextField
import hashlib, uuid
import random

Base = declarative_base()

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
		engine = db_connect()
		Session = sessionmaker(bind=engine)
		session = Session()
		
		result = session.query(User).filter(User.username == user.get('username')).first()
		if result == None:
			return False

		hash = hashlib.md5( (result.salt + user.get('password')).encode('utf-8') ).hexdigest()
		print("%s:%s" % (result.salt, hash)) # Store these
		print(result.password)
		if result.password == hash:
			return True  # Allowed
		return False  # Denied

class User(Base):
		"""Sqlalchemy listing model."""
		__tablename__ = "users"

		job_id = Column(Integer, primary_key=True)
		username = Column('username', String, nullable=False)
		password = Column('password', String, nullable=False)
		salt = Column('salt', String, nullable=False)

app = Flask(__name__)
SimpleLogin(app, login_checker=website_login)

@app.route('/', methods=["GET", "POST"])
def register():
		form = RegistrationForm(request.form)
		if request.method == 'POST' and form.validate():
				engine = db_connect()
				Session = sessionmaker(bind=engine)
				session = Session()
				ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
				chars=[]
				salt = ''.join(random.choice(ALPHABET) for i in range(16))
				hash = hashlib.md5( (salt + form.password.data).encode('utf-8') ).hexdigest()
				user = User(username = form.username.data,
										password = hash,
										salt = salt)
				session.add(user)
				session.commit()
				return redirect('/login/')
		return render_template('register.html', form=form)

class RegistrationForm(Form):
		username = StringField('Username', [validators.Length(min=4, max=25)])
		email = StringField('Email Address', [validators.Length(min=6, max=35)])
		password = PasswordField('New Password', [
				validators.DataRequired(),
				validators.EqualTo('confirm', message='Passwords must match')
		])
		confirm = PasswordField('Repeat Password')
		accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

#Base.metadata.create_all(db_connect())
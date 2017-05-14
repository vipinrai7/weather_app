'''
This is a POC to work on AWS.
Author: Vipin B Rai.
Version: 0.1
'''

from flask import Flask, request, g, jsonify, render_template
from flask_bootstrap import Bootstrap
from helper import data_dict
import sqlite3
import os
import requests
import json

def create_app():
	app = Flask(__name__)
	Bootstrap(app)
	return app
app = create_app()

# API url and Keys to openweathermap.org
params={'id':1263780,
		'APPID':'3b689091aaee29dc3b8a297267fd1618',
		'units':'metric'}
API_URL='http://api.openweathermap.org/data/2.5/weather'

# DB config for aws.
DATABASE = os.path.join(app.root_path,'test.db')
app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/add',methods=['POST'])
def addinfo():
	db=get_db()
	input_str=dict(request.get_json(force=True))
	t=float(input_str['temp'])
	h=float(input_str['humidity'])
	i=int(input_str['id'])
	db.execute('insert into test (id, temp, humidity) values(?,?,?);',\
		   [i,t,h])
	db.commit()
	db.close()
	return "Values inserted."

# This shows the basic contents of the db.
# To-Do The front end part yet to be decided.
@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM test;""")
    return '<br>'.join(str(row) for row in rows)

@app.route("/report")
def report():
	response=requests.get(API_URL,params=params)
	data=response.json()
	cleaned_data=data_dict(data)
	interim=json.dumps(cleaned_data)
	weather_data=json.loads(interim)

	return render_template('report.html',data=weather_data)

@app.route("/analytics")
def analytics():
	return render_template('super.html')

if __name__=='__main__':
	app.run(debug=True)


'''
This is a POC to work on AWS.
Author: Vipin B Rai.
Version: 0.1
'''

from flask import Flask, request, g, jsonify, render_template
from flask_bootstrap import Bootstrap
import sqlite3
import os

def create_app():
	app = Flask(__name__)
	Bootstrap(app)
	return app
app = create_app()


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

if __name__=='__main__':
	app.run()


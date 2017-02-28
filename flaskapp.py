from flask import Flask, request, g, jsonify
import sqlite3
#DB configs
DATABASE = '/home/ubuntu/flaskapp/test.db'

app = Flask(__name__)
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
	return "<h1> Hello from the Amazonians!!!!</h2>"

@app.route('/add',methods=['POST'])
def addinfo():
	db=get_db()
	input_str=dict(request.get_json(force=True))
	t=int(input_str['temp'])
	h=int(input_str['humidity'])
	db.execute('insert into test (temp, humidity) values(?,?);',\
		   [t,h])
	db.commit()
	db.close()
	return "Values insrted"

@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM test;""")
    return '<br>'.join(str(row) for row in rows)

if __name__=='__main__':
	app.run()


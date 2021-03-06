import sqlite3
from flask import Flask,request,render_template,flash
from flask import g
DATABASE = 'base.db'
app = Flask(__name__) 
if __name__ == "__main__":
    app.secret_key = '3123123asd' #secret enough
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.debug = True
    app.run()

#Get instanse of db if none is present
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.cursor().execute('CREATE TABLE IF NOT EXISTS data (tok REAL NOT NULL DEFAULT 0, time INTEGER DEFAULT 0, mA INTEGER);') 
        db.commit()

#Close DB connection on exit
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into data (tok, time) values (?, ?)',
                 [request.form['tok'], request.form['time']])
    db.commit()
    flash('New entry commiеted')
    return redirect(url_for('show_entries'))

@app.route('/')
def index():
	cur = get_db().execute('select tok, time, mA from data  order by time desc')
	entries = cur.fetchall()
	return render_template('show_entries.html', entries=entries)

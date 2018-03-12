from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import Column, Table, ForeignKey, desc, asc, Date, cast,and_
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound
import os
import calendar
import configparser
from datetime import date, timedelta



app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

APP_ENV = os.environ.get('APP_ENV') or 'local'
INI_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        './conf/{}.ini'.format(APP_ENV))

CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)
MYSQL = CONFIG['mysql']


if APP_ENV == 'live' or APP_ENV == 'local':
    DB_CONFIG = (MYSQL['user'], MYSQL['password'], MYSQL['host'], MYSQL['database'])
    DATABASE_URL = "mysql://%s:%s@%s/%s" % DB_CONFIG

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)
    due_date = db.Column(db.DATE)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    members = relationship('Subtask', backref="Subtask", cascade="all, delete-orphan", lazy='dynamic')



class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)
    due_date = db.Column(db.DATE)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    todo_id = Column(Integer, ForeignKey('todo.id'))

def week():
    today = date.today()

    ##weeks records
    weekday = today.weekday()
    # lower bound
    mon = today - timedelta(days=weekday)
    # upper bound
    sun = today + timedelta(days=(6 - weekday))

    week_task_record = Todo.query.filter(Todo.due_date >= mon,Todo.due_date <= sun).all()
    week_sabtask_record = Subtask.query.filter(Subtask.due_date >= mon,Subtask.due_date <= sun).all()


    week_com = []
    for i in week_task_record:
        if i.complete == True:
            week_com.append(i)

    week_incom = []
    for i in week_task_record:
        if i.complete == False:
            week_incom.append(i)



    week_subcom = []
    for i in week_sabtask_record:
        if i.complete == False:
            week_subcom.append(i)

    week_incsubcom = []
    for i in week_sabtask_record:
        if i.complete == True:
            week_incsubcom.append(i)

    return week_com, week_incom, week_subcom, week_incsubcom



def nextweek():
    today = date.today()

    ##weeks records
    weekday = today.weekday()
    # upper bound
    sun = today + timedelta(days=(6 - weekday))
    # next week records
    next_mon = sun + timedelta(days=(6 + weekday))


    next_week = Todo.query.filter(Todo.due_date >= sun,Todo.due_date <= next_mon).all()
    next_week_subtask = Subtask.query.filter(Subtask.due_date >= sun,Subtask.due_date <= next_mon).all()


    next_week_com = []
    for i in next_week:
        if i.complete == True:
            next_week_com.append(i)

    next_week_incom = []
    for i in next_week:
        if i.complete == False:
            next_week_incom.append(i)



    next_week_subcom = []
    for i in next_week_subtask:
        if i.complete == False:
            next_week_subcom.append(i)

    next_week_incsubcom = []
    for i in next_week_subtask:
        if i.complete == True:
            next_week_incsubcom.append(i)

    return next_week_com, next_week_incom, next_week_subcom, next_week_incsubcom




def overduedate():

    # over due date
    today = date.today()

    year = int(today.year)
    month = int(today.month)

    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)

    over_due_date = Todo.query.filter(Todo.due_date <= start_date).all()
    subtask_over_due_date = Subtask.query.filter(Subtask.due_date <= start_date).all()



    overduedate_week_com = []
    for i in over_due_date:
        if i.complete == True:
            overduedate_week_com.append(i)

    overduedate_week_incom = []
    for i in over_due_date:
        if i.complete == False:
            overduedate_week_incom.append(i)



    overduedate_week_subcom = []
    for i in subtask_over_due_date:
        if i.complete == False:
            overduedate_week_subcom.append(i)

    overduedate_week_incsubcom = []
    for i in subtask_over_due_date:
        if i.complete == True:
            overduedate_week_incsubcom.append(i)

    return overduedate_week_com, overduedate_week_incom, overduedate_week_subcom, overduedate_week_incsubcom



@app.route('/')
def index():

    #collecting week data
    week_com, week_incom, week_subcom, week_incsubcom = week()
    #collecting  nexxt week
    next_week_com, next_week_incom, next_week_subcom, next_week_incsubcom = nextweek()
    #collecting  over due date
    overduedate_week_com, overduedate_week_incom, overduedate_week_subcom, overduedate_week_incsubcom = overduedate()
    incomplete = Todo.query.filter_by(complete=False).order_by(Todo.due_date.asc()).all()
    complete = Todo.query.filter_by(complete=True).order_by(Todo.due_date.asc()).all()
    subtask = Subtask.query.filter_by(complete=False).order_by(Subtask.due_date.asc()).all()
    completesbtask = Subtask.query.filter_by(complete=True).order_by(Subtask.due_date.asc()).all()

    return render_template('index.html', incomplete=incomplete, complete=complete,subtask=subtask, completesbtask=completesbtask,
                           week_com=week_com,week_incom=week_incom, week_subcom=week_subcom,week_incsubcom=week_incsubcom,
                           next_week_com = next_week_com, next_week_incom = next_week_incom, next_week_subcom = next_week_subcom, next_week_incsubcom = next_week_incsubcom,
                           overduedate_week_com = overduedate_week_com, overduedate_week_incom = overduedate_week_incom, overduedate_week_subcom = overduedate_week_subcom, overduedate_week_incsubcom = overduedate_week_incsubcom)

@app.route('/add', methods=['POST'])
def add():
    todo = Todo()
    todo.text = request.form['todoitem']
    todo.complete = False
    date_obj = datetime.datetime.strptime(str(request.form['todoitemdate']), "%m/%d/%Y")
    str_now = date_obj.date().isoformat()
    todo.due_date = str_now
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/addsubtask/<todo_id>', methods=['POST'])
def addsubtask(todo_id):
    todo = Subtask()
    todo.text = request.form['todoitem']
    todo.complete = False
    date_obj = datetime.datetime.strptime(str(request.form['todoitemdate']), "%m/%d/%Y")
    str_now = date_obj.date().isoformat()
    todo.due_date = str_now
    todo.todo_id = todo_id
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/completesubtask/<id>')
def completesubtask(id):

    subt = Subtask.query.filter_by(id=int(id)).first()
    subt.complete = True
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/delete/<id>')
def delete(id):
    task = Todo.query.filter_by(id=int(id)).first()
    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/')


@app.route('/deletesubtask/<id>')
def deletesubtask(id):
    task = Subtask.query.filter_by(id=int(id)).first()
    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

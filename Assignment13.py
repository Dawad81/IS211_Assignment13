#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Docstring."""


import sqlite3
from flask import (Flask, request, session, g, url_for, redirect,
                   render_template, flash)
from flask_bootstrap import Bootstrap

DATABASE = 'hw13.db'
SECRET_KEY = '.g*lVD?s?HU?Ƅ?'
USERNAME = 'admin'
PASSWORD = 'password'


app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)


@app.before_request
def before_request():
    g.db = get_db()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME:
            session['logged_in'] = False
            error = 'The username you entered is incorrect. Please re-enter ' \
                    'a valid username.'
            flash('The username you entered is incorrect. Please re-enter a '
                  'valid username.', 'error')
            return render_template('login.html', error=error)
        elif request.form['password'] != PASSWORD:
            session['logged_in'] = False
            error = 'The password you entered is incorrect. Please re-enter ' \
                    'the valid password for this username.'
            flash('The password you entered is incorrect. Please re-enter '
                  'the valid password for this username.')
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            return redirect('/dashboard')
    else:
        return render_template('login.html', error=error)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if  session['logged_in'] == False:
        flash("You are not logged in! Please login to access the site.")
        return redirect(url_for('login'))
    else:
        student_info = g.db.execute(
            "SELECT student_id, first_name, last_name FROM students")
        students = [dict(student_id=row[0], first_name=row[1],
                         last_name=row[2]) for row in student_info.fetchall()]
        quiz_info = g.db.execute(
            'SELECT quiz_id, subject, questions, quiz_date FROM quizzes')
        quizzes = [dict(quiz_id=row[0], subject=row[1], questions=row[2],
                        date=row[3]) for row in quiz_info.fetchall()]
        return render_template("dashboard.html", students=students,
                               quizzes=quizzes)


@app.route('/student/add', methods=['GET', 'POST'])
def student_add():
    if session['logged_in'] == False:
        flash("You are not logged in! Please login to access the site.")
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            return render_template('student_add.html')
        elif request.method == 'POST':
            if request.form['first_name'] == "":
                flash("First Name field empty, please enter a valid"
                      "first name ")
                return redirect('/student/add')
            elif request.form['last_name'] == "":
                flash("Last Name field empty, please enter a valid last name")
                return redirect('/student/add')
            else:
                try:
                    g.db.execute('INSERT INTO students (first_name,'
                                 'last_name) VALUES (?,?)', (
                        request.form['first_name'], request.form['last_name']))
                    g.db.commit()
                    return redirect('/dashboard')
                except:
                    flash("An ERROR occurred! Please re-enter name and try"
                          "again.")
                    return redirect('/student/add')


@app.route('/quiz/add', methods=['GET', 'POST'])
def quiz_add():
    if session['logged_in'] == False:
        flash("You are not logged in! Please login to access the site.",
              'error')
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            return render_template('quiz_add.html')
        elif request.method == 'POST':
            if request.form['subject'] == "":
                flash("Quiz Subject field empty! Please enter a valid Quiz "
                      "Subject", 'error')
                return redirect('/quiz/add')
            elif request.form['questions'] == "":
                flash("Number of questions on Quiz field empty! Please enter a "
                      "valid Number of questions on Quiz", 'error')
                return redirect('/quiz/add')
            elif request.form['date'] == "":
                flash("Date of Quiz field empty! Please enter a valid Date of "
                      "Quiz", 'error')
                return redirect('/quiz/add')
            else:
                try:
                    g.db.execute('INSERT INTO quizzes (subject, questions,'
                                 'quiz_date)VALUES (?,?,?)',
                                 (request.form['subject'],
                                  request.form['questions'],
                                  request.form['date']))
                    g.db.commit()
                    return redirect('/dashboard')
                except:
                    flash("An ERROR occurred! Please re-enter Quiz information"
                          "and try again.", 'error')
                    return redirect('/quiz/add')


@app.route('/student/<id>', methods=['GET'])
def student_id_results(id):
    if session['logged_in'] == False:
        flash("You are not logged in! Please login to access the site.",)
        return redirect(url_for('login'))
    else:
        student_info = g.db.execute(
            'SELECT first_name, last_name FROM students WHERE student_id = ?',
            id)
        student = student_info.fetchall()[0]
        student_name = student[0] + " " + student[1]
        qiz_info = g.db.execute(
            'SELECT quiz_id, score FROM results WHERE student_id = ?', id)
        results = [dict(quiz_id=row[0], score=row[1])
                   for row in qiz_info.fetchall()]
        return render_template('student_id_results.html', results=results,
                               student_name=student_name)


@app.route('/results/add', methods=['GET', 'POST'])
def results_add():
    if session['logged_in'] == False:
        flash("You are not logged in! Please login to access the site.")
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            quiz_info = g.db.execute('SELECT quiz_id, subject FROM quizzes')
            quizzes = [dict(quiz_id=row[0], subject=row[1])
                       for row in quiz_info.fetchall()]
            student_info = g.db.execute(
                'SELECT student_id, first_name, last_name FROM students')
            students = [dict(
                student_id=row[0], student_name=row[1] + " " + row[2])
                for row in student_info.fetchall()]
            return render_template('results_add.html',
                                   quizzes=quizzes, students=students)
        elif request.method == 'POST':
            if request.form['score'] == '':
                flash("Score field is empty! Please enter a valid score and "
                      "try again.")
                return redirect("/results/add")
            else:
                g.db.execute('INSERT INTO results (student_id, quiz_id, '
                             'score) VALUES (?, ?, ?)',
                             (request.form['student_id'],
                              request.form['quiz_id'],
                              request.form['score']))
                g.db.commit()
                flash("You have successfully updated Quiz Results", 'info')
                return redirect("/dashboard")


if __name__ == '__main__':
    app.run(debug=1)

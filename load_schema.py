#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module creates the hw13.db SQL data base."""


import sqlite3 as lite


CON = lite.connect('hw13.db')

with CON:
    cur = CON.cursor()
    cur.execute("DROP TABLE IF EXISTS students")
    cur.execute("CREATE TABLE students(student_id INTEGER PRIMARY KEY ASC, first_name TEXT, last_name TEXT)")
    cur.execute("INSERT INTO students VALUES (01, 'John', 'Smith')")
    cur.execute("DROP TABLE IF EXISTS quizzes")
    cur.execute("CREATE TABLE quizzes (quiz_id INTEGER PRIMARY KEY ASC, subject TEXT, questions INTEGER, quiz_date TEXT)")
    cur.execute("INSERT INTO quizzes VALUES (01, 'Python Basics', 5, 'February 5th, 2015')")
    cur.execute("DROP TABLE IF EXISTS results")
    cur.execute("CREATE TABLE results(student_id INTEGER, quiz_id INTEGER, score INTEGER)")
    cur.execute("INSERT INTO results (student_id, quiz_id, score) VALUES (01,01,85)")

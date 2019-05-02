DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS results;

CREATE TABLE students(student_id INTEGER PRIMARY KEY ASC, first_name TEXT, last_name TEXT);

CREATE TABLE quizzes (quiz_id INTEGER PRIMARY KEY ASC, subject TEXT, questions INTEGER, quiz_date TEXT);

CREATE TABLE results(student_id INTEGER, quiz_id INTEGER, score INTEGER);

INSERT INTO students (student_id, first_name, last_name) VALUES (01, "John", "Smith");
INSERT INTO quizzes (quiz_id, subject, questions, quiz_date) VALUES (01, "Python Basics", 5, "February, 5th, 2015");
INSERT INTO results (student_id, quiz_id, score) VALUES (01,01,85);

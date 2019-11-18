#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is used to create the database class and execute all sql commands
# I am using mysql to connect to my online database
import mysql.connector  # This is a main connection to the database
import hashlib  # This is a hash library for my password storage
import uuid  # This is a salting library to keep hashed passwords unique
from datetime import date  # This allows me to collect the dates set
from tkinter import messagebox  # This is a part of the tkinter module that creates pop-ups

# Connecting to the host database#

mydb = mysql.connector.connect(
    host="db4free.net",
    user="alex_welch",
    passwd="A1exandm3",
    database='projectquiz')


class Database:

    # This initialises the database making sure all the tables are created
    def __init__(self):
        self.success = False
        tries = 0
        while not self.success:
            try:
                self.conn = mydb.cursor()
                self.conn.execute(
                    """CREATE TABLE IF NOT EXISTS USERS
               (USER_ID INT AUTO_INCREMENT PRIMARY KEY ,
               USERNAME     TEXT    NOT NULL,
               ENCRYPT_PASS TEXT   NOT NULL,
               SALT_VAL    TEXT    NOT NULL,
               ADMIN       INTEGER NOT NULL);"""
                )
                self.conn.execute(
                    """CREATE TABLE IF NOT EXISTS QUIZ
               (QUIZ_ID INT AUTO_INCREMENT PRIMARY KEY,
               TOPIC TEXT   NOT NULL,
               DATE_SET TEXT NOT NULL);"""
                )
                self.conn.execute(
                    """CREATE TABLE IF NOT EXISTS QUESTIONS
               (QUESTION_ID INT AUTO_INCREMENT PRIMARY KEY,
               QUESTION_TEXT TEXT   NOT NULL,
               TIMER        INT     NOT NULL);"""
                )
                self.conn.execute(
                    """CREATE TABLE IF NOT EXISTS ANSWERS
               (ANSWER_ID INT AUTO_INCREMENT PRIMARY KEY,
               ANSWER_TEXT TEXT NOT NULL,
               CORRECT INTEGER NOT NULL,
               PARENT_QUESTION INT NOT NULL,
               FOREIGN KEY (PARENT_QUESTION) REFERENCES QUESTIONS(QUESTION_ID));"""
                )
                self.conn.execute(
                    """CREATE TABLE IF NOT EXISTS QUIZ_QUESTIONS
               (QUIZ_NUM INT,
                QUESTION_NUM INT,
                QUESTION_NUMBER INT NOT NULL,
                FOREIGN KEY (QUIZ_NUM) REFERENCES QUIZ(QUIZ_ID),
                FOREIGN KEY (QUESTION_NUM) REFERENCES QUESTIONS(QUESTION_ID));"""
                )
                self.conn.execute(
                    """CREATE TABLE IF NOT EXISTS ASSIGNED_QUIZ
               (QUIZ_ASSIGNED INT NOT NULL,
               USER INT NOT NULL,
               COMPLETE INT NOT NULL,
               SCORE  TEXT,
               DATE_COMPLETED TEXT,
               FOREIGN KEY (QUIZ_ASSIGNED) REFERENCES QUIZ(QUIZ_ID),
               FOREIGN KEY (USER) REFERENCES USERS(USER_ID),
               PRIMARY KEY(QUIZ_ASSIGNED, USER));"""
                )
                mydb.commit()
                self.current_questions = []
                self.current_user = ""
                self.current_test = None
                self.quiz_details = []
                self.question_id = []
                self.answers = []
                self.question_details = []
                self.personal_progress = []
                self.success = True
            except ConnectionRefusedError:
                tries += 1
                if tries == 3:
                    messagebox.showerror('Max Attempts Reached',
                                         'The max amount of attempts have been reached please try again later')
                else:
                    msgbox = messagebox.askquestion(
                        'Try Again?", "It seems there was an error with the connection to the server'
                        '\nWould you like to try again?', icon='warning')
                    if msgbox == 'no':
                        exit()

    # Searches for a user in the database
    def search_user(self, target):
        self.conn.execute(
            "SELECT USERNAME FROM USERS WHERE USERNAME='"
            + target
            + "'"
        )
        results = self.conn.fetchone()
        if results is None:
            results = []
        if len(results) >= 1:
            return True

    # Searches for the password in the user table
    def search_password(self, password, user):
        self.conn.execute(
            "SELECT SALT_VAL FROM USERS WHERE USERNAME='"
            + user
            + "'"
        )
        results = self.conn.fetchone()
        salt = results[0]
        new_pass = password + salt
        self.close_data()
        self.open_data()
        self.conn.execute(
            "SELECT ENCRYPT_PASS FROM USERS WHERE USERNAME='"
            + user
            + "'"
        )
        results = self.conn.fetchone()
        hash_pass = hashlib.md5(new_pass.encode())
        coded_pass = hash_pass.hexdigest()
        true_pass = results[0]
        if coded_pass == true_pass:
            self.current_user = user
            return True
        else:
            return False

    # Checks if the user is an admin
    def admin(self, user):
        self.conn.execute(
            "SELECT ADMIN FROM USERS WHERE USERNAME='"
            + user
            + "'"
        )
        results = self.conn.fetchall()
        for row in results:
            admin = row[0]
        if admin == 1:
            return True
        else:
            return False

    # This method makes sure the new account's password is encrypted and has a salt to make it even harder to crack
    def create_account(
            self, user, password, conf_password, admin
    ):
        if admin == "True":
            admin = 1
        else:
            admin = 0
        if not self.search_user(user):
            if conf_password == password:
                salt = str(uuid.uuid4())
                salted_pass = password + str(salt)
                hashed_pass = hashlib.md5(
                    salted_pass.encode()
                )
                coded_pass = str(hashed_pass.hexdigest())
                sql = """INSERT INTO USERS(USERNAME,ENCRYPT_PASS,SALT_VAL,ADMIN) VALUES(%s,%s,%s,%s)"""
                val = [user, coded_pass, salt, admin]
                self.conn.execute(sql, val)
            else:
                messagebox.showerror(
                    "Error", "Passwords do not match"
                )
        else:
            messagebox.showerror(
                "Error", "That username is already taken"
            )

    # This adds a question to the database
    def add_question(self, details):
        timer = details[5].get('1.0', 'end-1c')
        # checking that the timer is an integer and not any other input
        if timer.isdigit():
            timer = int(timer)
            sql = """INSERT INTO QUESTIONS(QUESTION_TEXT,TIMER) VALUES(%s,%s)"""
            q_text = details[0].get("1.0", 'end-1c')
            self.conn.execute(sql, [q_text, timer])
            self.conn.execute(
                "SELECT QUESTION_ID FROM QUESTIONS WHERE QUESTION_TEXT='"
                + q_text
                + "'"
            )
            question_id = self.conn.fetchone()[0]
            self.current_questions.append(question_id)
            for answer in range(1, 5):
                if answer == 1:
                    correct = 1
                else:
                    correct = 0
                sql = """INSERT INTO ANSWERS(ANSWER_TEXT,CORRECT,PARENT_QUESTION) VALUES(%s,%s,%s)"""
                vals = [
                    str(details[answer].get('1.0', 'end-1c')),
                    correct,
                    question_id,
                ]
                self.conn.execute(sql, vals)
        else:
            messagebox.showerror(
                "Error", "Timer should be an integer"
            )

    # This method assigned the quiz just made by a teacher to
    # all of the students in their class through the link table, quiz questions
    def question_assigned_to_test(self, topic):
        if len(self.current_questions) == 0:
            messagebox.showerror(
                "Error", "No questions created"
            )
            pass
        elif topic == "":
            messagebox.showerror("Error", "No topic given")
            pass
        else:
            sql = """INSERT INTO QUIZ(TOPIC,DATE_SET) VALUES(%s,%s)"""
            vals = [topic, date.today()]
            self.conn.execute(sql, vals)
            quiz_id = self.conn.lastrowid
            sql = """INSERT INTO QUIZ_QUESTIONS(QUIZ_ID,QUESTION_ID,QUESTION_NUMBER) VALUES(%s,%s,%s)"""
            for q in range(len(self.current_questions)):
                vals = [
                    quiz_id,
                    self.current_questions[q],
                    q,
                ]
                self.conn.execute(sql, vals)
            sql = """INSERT INTO ASSIGNED_QUIZ(QUIZ_ASSIGNED,USER,COMPLETE,SCORE,DATE_COMPLETED) VALUES(%s,%s,%s,%s,
            %s) """
            self.conn.execute("SELECT USER_ID FROM USERS WHERE ADMIN=0")
            num_users = self.conn.fetchall()
            for user in range(len(num_users)):
                vals = [
                    quiz_id,
                    (num_users[user])[0],
                    0,
                    0,
                    "N/A",
                ]
                self.conn.execute(sql, vals)
            self.current_questions = []

    # This collects the quizzes that have been assigned to the user and adds them to a list
    def retrieve_quizes(self, complete=0):
        self.conn.execute(
            "SELECT USER_ID FROM USERS WHERE USERNAME='"
            + self.current_user
            + "'"
        )
        user_id = str(self.conn.fetchone()[0])
        self.conn.execute(
            "SELECT QUIZ_ASSIGNED FROM ASSIGNED_QUIZ WHERE USER='"
            + user_id
            + "' AND COMPLETE='"
            + str(complete)
            + "'"
        )
        quizzes = self.conn.fetchall()
        complete_quiz_data = ""
        for quiz in range(len(quizzes)):
            self.conn.execute(
                "SELECT * FROM QUIZ WHERE QUIZ_ID='"
                + str(quizzes[quiz][0])
                + "'"
            )
            quiz_data = self.conn.fetchall()
            for data in range(len(quiz_data[0])):
                complete_quiz_data = (
                        complete_quiz_data + " " + str(quiz_data[0][data])
                )
                if (data + 1) % 3 == 0:
                    if data != 0:
                        self.quiz_details.append(
                            complete_quiz_data
                        )
                        complete_quiz_data = ""

    # This function takes all the quizzes and decompiles them into their questions
    def start_test(self, test):
        self.current_test = test
        self.conn.execute(
            "SELECT QUESTION_ID FROM QUIZ_QUESTIONS WHERE QUIZ_ID='"
            + self.quiz_details[test][1:3]
            + "'"
        )
        for row in self.conn:
            self.question_id.append(row[0])
        for details in range(len(self.question_id)):
            self.conn.execute(
                "SELECT * FROM QUESTIONS WHERE QUESTION_ID='"
                + str(self.question_id[details])
                + "'"
            )
            self.question_details.append(
                self.conn.fetchall()
            )
        for ans in range(len(self.question_details)):
            self.conn.execute(
                "SELECT * FROM ANSWERS WHERE PARENT_QUESTION='"
                + str(self.question_details[ans][0][0])
                + "'"
            )
            self.answers.append(self.conn.fetchall())

    def end_test(self, score, question):
        self.conn.execute(
            "SELECT USER_ID FROM USERS WHERE USERNAME='"
            + self.current_user
            + "'"
        )
        user_id = str(self.conn.fetchone()[0])
        percentage = str((score / question) * 100)
        sql = "UPDATE ASSIGNED_QUIZ SET COMPLETE = %s, SCORE = %s, DATE_COMPLETED = %s WHERE USER = %s AND " \
              "QUIZ_ASSIGNED = %s "
        vals = (
            1,
            str(percentage),
            str(date.today()),
            user_id,
            self.quiz_details[self.current_test][1:3],
        )
        self.conn.execute(sql, vals)

    def retrieve_completed(self, query_type):
        if query_type == 1:
            self.conn.execute(
                "SELECT USER_ID FROM USERS WHERE USERNAME='"
                + self.current_user
                + "'"
            )
            user_id = str(self.conn.fetchone()[0])
            self.conn.execute("SELECT QUIZ_ASSIGNED FROM ASSIGNED_QUIZ WHERE USER='" + user_id + "'AND COMPLETE = 1")
            quizzes_completed = self.conn.fetchall()
            dates_set = []
            for quiz_id in range(len(quizzes_completed)):
                self.conn.execute(
                    "SELECT DATE_SET FROM QUIZ WHERE QUIZ_ID='" + str(quizzes_completed[quiz_id][0]) + "'")
                dates_set.append(self.conn.fetchone())
            self.personal_progress = []
            self.conn.execute("SELECT SCORE FROM ASSIGNED_QUIZ WHERE USER='" + user_id + "'AND COMPLETE = 1")
            for row in self.conn:
                self.personal_progress.append(list(row))
            for date in range(len(self.personal_progress)):
                self.personal_progress[date].append(dates_set[date][0])
            print(self.personal_progress)
            return self.personal_progress
        # elif type == 2:
        # self.conn.execute()
        else:
            pass

    # Establish a connection to the database
    def open_data(self):
        self.conn = mydb.cursor()

    # Save all the changes made to the database
    def close_data(self):
        mydb.commit()

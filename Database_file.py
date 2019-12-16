#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib  # This is a hash library for my password storage
import re
import smtplib
import ssl
import uuid  # This is a salting library to keep hashed passwords unique
from datetime import date  # This allows me to collect the dates set
from tkinter import messagebox  # This is a part of the tkinter module that creates pop-ups

# This file is used to create the database class and execute all sql commands
# I am using mysql to connect to my online database
import mysql.connector  # This is a main connection to the database

# Connecting to the host database#

mydb = mysql.connector.connect(
    host="db4free.net",
    user="alex_welch",
    passwd="A1exandm3",
    database='projectquiz',
    buffered=True)


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
               ADMIN       INTEGER NOT NULL,
               EMAIL       VARCHAR(320) NOT NULL,
               TARGET      TEXT);"""
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
                self.question_names = []
                self.current_test = None
                self.quiz_details = []
                self.question_id = []
                self.answers = []
                self.question_details = []
                self.personal_progress = []
                self.average_progress = []
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
            self, user, password, conf_password, admin, email, target
    ):
        if admin == "True":
            admin = 1
            if target != "N/A":
                messagebox.showerror("Error", "Teachers should not have targets")
        else:
            admin = 0
            if target == "N/A":
                messagebox.showerror("Error", "Students should have a target")
        regex_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        regex_pass = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        if re.search(regex_email, email):
            if not self.search_user(user):
                if conf_password == password:
                    if re.search(regex_pass, password):
                        salt = str(uuid.uuid4())
                        salted_pass = password + str(salt)
                        hashed_pass = hashlib.md5(
                            salted_pass.encode()
                        )
                        coded_pass = str(hashed_pass.hexdigest())
                        sql = """INSERT INTO USERS(USERNAME,ENCRYPT_PASS,SALT_VAL,ADMIN,EMAIL,TARGET) VALUES(%s,%s,%s,%s,
                        %s,%s) """
                        val = [user, coded_pass, salt, admin, email, target]
                        self.conn.execute(sql, val)
                    else:
                        messagebox.showerror(
                            "Error", "Passwords must contain\nat least one letter and one number"
                        )
                else:
                    messagebox.showerror(
                        "Error", "Passwords do not match"
                    )
            else:
                messagebox.showerror(
                    "Error", "That username is already taken"
                )
        else:
            messagebox.showerror(
                "Error", "Email does not exist"
            )

    # this function sends emails to users after a quiz has been set for them
    def send_email(self):
        self.conn.execute('SELECT EMAIL,USERNAME FROM USERS WHERE ADMIN = 0')
        receivers = self.conn.fetchone()
        port = 465
        smpt_server = "smpt.gmail.com"
        sender = 'mathsappproject@gmail.com'
        password = 'A1exandme'
        for student in range(len(receivers)):
            message = """\ 
            Subject: New Assignment
            
            
            Hello %s there is a new assignment for you to complete at MathsApp\n please complete it for one week from 
            now, good luck!\n Kind regards\n The MathsApp Team """.format(receivers[student][1])
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smpt_server, port, context=context) as server:
                server.login(sender, password)
                server.sendmail(sender, receivers[student][0], message)

    # This adds a question to the database
    def add_question(self, details):
        timer = details[5].get('1.0', 'end-1c')
        # checking that the timer is an integer and not any other input
        if timer.isdigit():
            timer = int(timer)
            sql = """INSERT INTO QUESTIONS(QUESTION_TEXT,TIMER) VALUES(%s,%s)"""
            q_text = details[0].get("1.0", 'end-1c')

            self.question_names.append(q_text)
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

    def remove_question(self, selected, tree):
        tree.delete(selected)
        index_of_deleted = int(selected[2::])
        self.current_questions.pop(index_of_deleted - 1)
        self.question_names.pop(index_of_deleted - 1)

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
            # self.send_email()

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
        if score == 0:
            score = 1
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

    def retrieve_completed(self, query_type, user=0):
        if user == 0:
            user = self.current_user
        if query_type == 1:
            self.conn.execute(
                "SELECT USER_ID FROM USERS WHERE USERNAME='"
                + user
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
            return self.personal_progress
        else:
            pass

    def user_target(self, num, user=0):
        if user == 0:
            user = self.current_user
        self.conn.execute(
            "SELECT TARGET FROM USERS WHERE USERNAME='"
            + user
            + "'"
        )
        target = self.conn.fetchone()[0]
        if target == "A*":
            target_percent = 90
        elif target == "A":
            target_percent = 80
        elif target == "B":
            target_percent = 70
        elif target == "C":
            target_percent = 60
        elif target == "D":
            target_percent = 50
        elif target == "E":
            target_percent = 40
        else:
            target_percent = 0
        target_list = []
        for i in range(len(num)):
            target_list.append(target_percent)
        return target_list

    def user_weakness(self):
        weaknesses = []
        self.conn.execute(
            "SELECT USER_ID FROM USERS WHERE USERNAME='"
            + self.current_user
            + "'"
        )
        user_id = self.conn.fetchone()[0]
        sql = "SELECT QUIZ,SCORE FROM ASSIGNED_QUIZ WHERE (USER = %s AND SCORE <= 50)"
        val = (user_id,)
        self.conn.execute(sql, val)
        quiz_scores = self.conn.fetchall()
        for i in range(quiz_scores):
            self.conn.execute("SELECT TOPIC FROM QUIZ WHERE QUIZ_ID ='" + quiz_scores[i][0] + "'")
            weaknesses.append(self.conn.fetchone()[0])
        print(weaknesses)
        return weaknesses

    # Establish a connection to the database
    def open_data(self):
        self.conn = mydb.cursor()

    def first_user(self):
        self.conn.execute("SELECT USERNAME FROM USERS WHERE ADMIN = 0")
        user = self.conn.fetchone()[0]
        print(user)
        return user

    # Save all the changes made to the database
    def close_data(self):
        mydb.commit()

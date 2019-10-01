#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
from Database_file import *

# These are the base size and colour variables for the program
# I put these here so that if i wanna change the size of my window everything else will change in proportion

x_cord = 1200
y_cord = 750
size = '{}x{}'.format(x_cord, y_cord)
bgc = '#4281A4'
fgc = '#EEEBD3'
def_font = ('Times New Roman', 20)


# Creates account by taking data from entries
# and then passing them as parameters to the database class methods

def create_acc(vals, win):
    db.open_data()
    user = str(vals[0].get())
    password = str(vals[1].get())
    conf_password = str(vals[2].get())
    admin = str(vals[3].get())
    db.create_account(user, password, conf_password, admin)
    db.close_data()
    win.destroy()
    Login()


# Checks if the inputted password matches the user password on the database

def login_check(vals, win):
    db.open_data()
    user = str(vals[0].get())
    password = str(vals[1].get())
    if db.search_user(user):
        if db.search_password(password, user):
            win.destroy()
            if db.admin(user):
                main_screen_admin()
            else:
                main_screen_user()
                db.close_data()
        else:
            messagebox.showerror('Error', 'Password is incorrect')
            db.close_data()
    else:
        messagebox.showerror('Error', 'Username does not exist')
        db.close_data()


# This is the login form for the website, it passes the inputs into the database and validates them
def Login():
    log = Tk()
    log.geometry(size)
    log.resizable(False, False)
    log.configure(bg=bgc)
    log.title('Maths Quiz~Alex Welch')
    Lbls = ['Username', 'Password']
    for x in range(len(Lbls)):
        Label(log, text=Lbls[x], bg=bgc, fg=fgc,
              font=def_font).place(x=x_cord * 1 / 3, y=y_cord * 2 / 5
                                                       + 50 * x, anchor='center')

    Label(log, text='Please enter user details below', bg=bgc, fg=fgc,
          font=def_font).place(x=x_cord * 1 / 2, y=y_cord * 1 / 5,
                               anchor='center')
    User = Entry(log, width=25, bg=bgc, fg=fgc, justify='center')
    Password = Entry(log, show='*', width=25, bg=bgc, fg=fgc, justify='center')
    User.place(x=x_cord * 3 / 5, y=y_cord * 2 / 5, anchor='center')
    Password.place(x=x_cord * 3 / 5, y=y_cord * 2 / 5 + 50,
                   anchor='center')
    data = [User, Password]
    Button(log, text='Login', bg=bgc, fg=fgc, command=lambda: \
        login_check(data, log)).place(x=x_cord * 1 / 2, y=y_cord * 5
                                                          / 7, anchor='center')
    Button(log, text='Exit', bg=bgc, fg=fgc, command=lambda: \
        log.destroy()).place(x=x_cord * 1 / 2, y=y_cord * 4 / 5,
                             anchor='center')
    Button(log, text='Temporary', bg=bgc, fg=fgc, command=lambda: \
        register(log)).place(x=x_cord * 1 / 2, y=y_cord * 6 / 7,
                             anchor='center')
    log.mainloop()


# This is the main screen with different options such as creating tasks and viewing the students progress
def main_screen_admin():
    main_win = Tk()
    main_win.title('Main Admin Window')
    main_win.geometry(size)
    main_win.configure(bg=bgc)
    main_lbls = ['Welcome Back',
                 'Here you can either assign work or check your students performance'
                 ]
    for lbls in range(len(main_lbls)):
        Label(main_win, text=main_lbls[lbls], bg=bgc, fg=fgc,
              font=def_font).place(x=x_cord * 1 / 2, y=y_cord * 1 / 5
                                                       + 50 * lbls, anchor='center')

    Button(main_win,
           text='Make new account',
           bg=bgc,
           fg=fgc,
           command=lambda: register(main_win)
           ).place(x=x_cord * 1 / 2, y=y_cord * 4 / 5, anchor='center')

    Button(
        main_win,
        text='Log Out',
        bg=bgc,
        fg=fgc,
        command=lambda: (main_win.destroy(), Login()),
    ).place(x=x_cord * 1 / 2, y=y_cord * 9 / 10, anchor='center')

    Button(
        main_win,
        text='Create a Quiz',
        bg=bgc,
        fg=fgc,
        width=20,
        height=7,
        command=lambda: create_quiz(main_win),
    ).place(x=x_cord * 1 / 3, y=y_cord * 1 / 2, anchor='center')

    Button(
        main_win,
        text='Class Review',
        bg=bgc,
        fg=fgc,
        width=20,
        height=7,
        command=lambda: view_students(main_win),
    ).place(x=x_cord * 2 / 3, y=y_cord * 1 / 2, anchor='center')


## This allows teachers to create accounts for students
def register(win):
    win.destroy()
    reg = Tk()
    reg.title('Register')
    reg.geometry(size)
    reg.resizable(False, False)
    reg.configure(bg=bgc)
    Lbls = ['Username', 'Password', 'Confirm Password', 'Admin']
    for x in range(len(Lbls)):
        Label(reg, text=Lbls[x], bg=bgc, fg=fgc,
              font=def_font).place(x=x_cord * 1 / 3, y=y_cord * 2 / 5
                                                       + 50 * x, anchor='center')
    admin = StringVar(reg)
    admin.set('True')
    choices = ['True', 'False']

    Label(reg, text='Insert your details below to register your account'
          , bg=bgc, fg=fgc, font=def_font).place(x=x_cord * 1 / 2,
                                                 y=y_cord * 1 / 5, anchor='center')
    new_user = Entry(reg, justify='center', width=25)
    new_pass = Entry(reg, show='*', justify='center', width=25)
    conf_pass = Entry(reg, show='*', justify='center', width=25)
    new_user.place(x=x_cord * 3 / 5, y=y_cord * 2 / 5, anchor='center')
    new_pass.place(x=x_cord * 3 / 5, y=y_cord * 2 / 5 + 50,
                   anchor='center')
    conf_pass.place(x=x_cord * 3 / 5, y=y_cord * 2 / 5 + 100,
                    anchor='center')
    admin_opt = OptionMenu(reg, admin, *choices)
    admin_opt.place(x=x_cord * 3 / 5, y=y_cord * 2 / 5 + 150,
                    anchor='center')
    data = [new_user, new_pass, conf_pass, admin]
    Button(reg, text='Register', bg=bgc, fg=fgc, command=lambda: \
        create_acc(data, reg)).place(x=x_cord * 1 / 3, y=y_cord * 5
                                                         / 6, anchor='center')
    Button(reg, text='Back', bg=bgc, fg=fgc, command=lambda: \
        (reg.destroy(), main_screen_admin())).place(x=x_cord * 2
                                                      / 3, y=y_cord * 5 / 6, anchor='center')


def view_students(win):
    win.destroy()
    pass


## From here the teachers can view their current test theyre making and publish it to students

def create_quiz(win):
    win.destroy()
    quiz = Tk()
    quiz.geometry(size)
    quiz.configure(bg=bgc)
    quiz.resizable(False, False)
    topic = Entry(quiz, justify='center')
    topic.place(x=x_cord * 1 / 2, y=y_cord * 1 / 2, anchor='center')
    Lbls = ['Create a quiz',
            'Give the quiz a name and the topic it is based on',
            'Use the plus Icon to add a question',
            'Then give 4 answers for the student to select from']
    for lbl in range(len(Lbls)):
        Label(quiz, bg=bgc, fg=fgc, text=Lbls[lbl],
              font=def_font).place(x=x_cord * 1 / 2, y=y_cord * 1 / 5
                                                       + 35 * lbl, anchor='center')
    create = Button(
        quiz,
        text='+',
        bg=bgc,
        fg=fgc,
        font=('System', 10),
        width=10,
        height=2,
        command=lambda: create_question(),
    )
    exit = Button(
        quiz,
        text='Exit',
        bg=bgc,
        fg=fgc,
        font=('System', 10),
        width=10,
        height=2,
        command=lambda: (main_screen_admin(), quiz.destroy()),
    )
    save_quiz = Button(
        quiz,
        text='Publish Quiz',
        bg=bgc,
        fg=fgc,
        font=('System', 10),
        width=10,
        height=2,
        command=lambda: (main_screen_admin(), db.open_data(), db.question_assigned_to_test(topic.get()), db.close_data(), quiz.destroy()))
    create.place(x=x_cord * 1 / 6, y=y_cord * 1 / 4, anchor='center')
    exit.place(x=x_cord * 5 / 6, y=y_cord * 1 / 4, anchor='center')
    save_quiz.place(x=x_cord * 5 / 6, y=y_cord * 4 / 5, anchor='center')


# Gives GUI for creating questions including database input

def create_question():
    question = Tk()
    question.geometry(size)
    question.configure(bg=bgc)
    question.resizable(False, False)
    q_var = Entry(question, justify='center', width=40)
    ans_1 = Entry(question, justify='center', width=25)
    ans_2 = Entry(question, justify='center', width=25)
    ans_3 = Entry(question, justify='center', width=25)
    ans_4 = Entry(question, justify='center', width=25)
    timer = Entry(question, justify='center', width=25)
    q_details = [
        q_var,
        ans_1,
        ans_2,
        ans_3,
        ans_4,
        timer,
    ]
    lbls = [
        'Enter the Question here',
        'Enter correct answer here',
        'Wrong answer',
        'Wrong answer',
        'Wrong answer',
        'Timer',
    ]
    for entry in range(len(q_details)):
        if entry == 0:
            q_details[entry].place(x=x_cord * 1 / 2, y=y_cord * entry
                                                       + 40, anchor='center')

            Label(question, text=lbls[entry], bg=bgc, fg=fgc,
                  font=def_font).place(x=x_cord * 1 / 6, y=y_cord
                                                           * entry + 45, anchor='center')
        q_details[entry].place(x=x_cord * 1 / 2, y=y_cord * entry / 6
                                                   + 50, anchor='center')

        Label(question, text=lbls[entry], bg=bgc, fg=fgc,
              font=def_font).place(x=x_cord * 1 / 6, y=y_cord * entry
                                                       / 6 + 50, anchor='center')
    add_q_btn = Button(question, text='Create\nQuestion', bg=bgc,
                       fg=fgc, command=lambda: (db.open_data(),
                                                db.add_question(q_details), db.close_data(), question.destroy()))
    delete_q_btn = Button(question, text='Back', bg=bgc,
                          fg=fgc, command=lambda: question.destroy())
    add_q_btn.place(x=x_cord * 5 / 6, y=y_cord * 1 / 3, anchor='center')
    delete_q_btn.place(x=x_cord * 5 / 6, y=y_cord * 2 / 3,
                       anchor='center')


# This the main screen for the students, they can complete quizzes or view their progress
def main_screen_user():
    main_win = Tk()
    main_win.title('Main Window')
    main_win.geometry(size)
    main_win.configure(bg=bgc)
    main_lbls = ['Welcome Back',
                 'Here you can either complete work or check your performance'
                 ]
    for lbls in range(len(main_lbls)):
        Label(main_win, text=main_lbls[lbls], bg=bgc, fg=fgc,
              font=def_font).place(x=x_cord * 1 / 2, y=y_cord * 1 / 5
                                                       + 50 * lbls, anchor='center')

    Button(
        main_win,
        text='Complete a Quiz',
        bg=bgc,
        fg=fgc,
        width=20,
        height=7,
        command=lambda: complete_quiz(main_win),
    ).place(x=x_cord * 1 / 3, y=y_cord * 1 / 2, anchor='center')

    Button(
        main_win,
        text='Personal Review',
        bg=bgc,
        fg=fgc,
        width=20,
        height=7,
        command=lambda: view_progress(main_win),
    ).place(x=x_cord * 2 / 3, y=y_cord * 1 / 2, anchor='center')

    Button(
        main_win,
        text='Log Out',
        bg=bgc,
        fg=fgc,
        command=lambda: (main_win.destroy(), Login()),
    ).place(x=x_cord * 1 / 2, y=y_cord * 5 / 6, anchor='center')


# This function retrieves the quizzes assigned to the user and lets them complete questions
def complete_quiz(win):
    win.destroy()
    quiz = Tk()
    quiz.title('Quiz')
    quiz.geometry(size)
    quiz.configure(bg=bgc)
    db.retrieve_quizes()
    Label(quiz, text='Here are the quizzes available to you', bg=bgc, fg=fgc, font=def_font
          ).place(x=x_cord / 2, y=y_cord / 10, anchor='center')
    Button(quiz, text='Back', fg=fgc, bg=bgc, font=def_font, command=lambda: (main_screen_user(), quiz.destroy())
           ).place(x=x_cord * 3 / 4, y=y_cord / 10, anchor='center')
    for data in range(int(len(db.quiz_details))):
        x_pos=1
        if data + 1 % 3 == 1:
            x_pos=x_pos*2
        Label(quiz, text=db.quiz_details[data], bg=bgc, fg=fgc, font=def_font
              ).place(x=x_cord * (x_pos / 4), y=(y_cord * (data % 3) / 5) + 200, anchor='center')
        Button(quiz, text="Complete This Quiz", bg=bgc, fg=fgc, font=def_font
               ).place(x=x_cord * (x_pos / 4), y=(y_cord * (data % 3) / 5) + 250, anchor='center')


def view_progress(win):
    pass


if __name__ == '__main__':
    db = database()
    Login()

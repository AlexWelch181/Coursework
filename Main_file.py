#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
from Database_file import *
import time
import random

# from pandas import DataFrame
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt

# I am using tkinter as it is a simple GUI tool
# I import my other file to handle my database functions

# These are the base size and colour variables for the program
# I put these here so that if i wanna change the size of my window everything else will change in proportion

x_cord = 1200
y_cord = 750
size = "{}x{}".format(x_cord, y_cord)
bgc = "#4281A4"
fgc = "#EEEBD3"
def_font = ("Times New Roman", 20)


# Creates account by taking data from entries
# and then passing them as parameters to the database class methods


def create_acc(create_vals, win):
    db.open_data()
    user = str(create_vals[0].get())
    password = str(create_vals[1].get())
    conf_password = str(create_vals[2].get())
    admin = str(create_vals[3].get())
    db.create_account(user, password, conf_password, admin)
    db.close_data()
    win.destroy()
    login()


# Checks if the inputted password matches the user password on the database


def login_check(login_vals, win):
    db.open_data()
    user = str(login_vals[0].get())
    password = str(login_vals[1].get())
    if db.search_user(user):
        if db.search_password(password, user):
            win.destroy()
            if db.admin(user):
                main_screen_admin()
            else:
                main_screen_user()
                db.close_data()
        else:
            messagebox.showerror(
                "Error", "Password is incorrect"
            )
            db.close_data()
    else:
        messagebox.showerror(
            "Error", "Username does not exist"
        )
        db.close_data()


# This is the login form for the website, it passes the inputs into the database and validates them


def login():
    log = Tk()
    log.geometry(size)
    log.resizable(False, False)
    log.configure(bg=bgc)
    log.title("Maths Quiz~Alex Welch")
    lbls = ["Username", "Password"]
    for x in range(len(lbls)):
        Label(
            log, text=lbls[x], bg=bgc, fg=fgc, font=def_font
        ).place(
            x=x_cord * 1 / 3,
            y=y_cord * 2 / 5 + 50 * x,
            anchor="center",
        )
    Label(
        log,
        text="Please enter user details below",
        bg=bgc,
        fg=fgc,
        font=def_font,
    ).place(
        x=x_cord * 1 / 2, y=y_cord * 1 / 5, anchor="center"
    )
    user = Entry(
        log, width=25, bg=bgc, fg=fgc, justify="center"
    )
    password = Entry(
        log,
        show="*",
        width=25,
        bg=bgc,
        fg=fgc,
        justify="center",
    )
    user.place(
        x=x_cord * 3 / 5, y=y_cord * 2 / 5, anchor="center"
    )
    password.place(
        x=x_cord * 3 / 5,
        y=y_cord * 2 / 5 + 50,
        anchor="center",
    )
    data = [user, password]
    Button(
        log,
        text="Login",
        bg=bgc,
        fg=fgc,
        width=20,
        height=3,
        command=lambda: login_check(data, log),
    ).place(
        x=x_cord * 1 / 2, y=y_cord * 5 / 7, anchor="center"
    )
    Button(
        log,
        text="Exit",
        bg=bgc,
        fg=fgc,
        width=20,
        height=3,
        command=lambda: log.destroy(),
    ).place(
        x=x_cord * 1 / 2, y=y_cord * 4 / 5, anchor="center"
    )
    log.mainloop()


# This is the main screen with different options such as creating tasks and viewing the students progress
def main_screen_admin():
    main_win = Tk()
    main_win.title("Main Admin Window")
    main_win.geometry(size)
    main_win.configure(bg=bgc)
    main_lbls = [
        "Welcome Back",
        "Here you can either assign work or check your students performance",
    ]
    for lbls in range(len(main_lbls)):
        Label(
            main_win,
            text=main_lbls[lbls],
            bg=bgc,
            fg=fgc,
            font=def_font,
        ).place(
            x=x_cord * 1 / 2,
            y=y_cord * 1 / 5 + 50 * lbls,
            anchor="center",
        )
    Button(
        main_win,
        text="Make new account",
        bg=bgc,
        fg=fgc,
        width=20,
        height=3,
        command=lambda: register(main_win),
    ).place(
        x=x_cord * 1 / 2, y=y_cord * 4 / 5, anchor="center"
    )

    Button(
        main_win,
        text="Log Out",
        bg=bgc,
        fg=fgc,
        width=20,
        height=3,
        command=lambda: (main_win.destroy(), login()),
    ).place(
        x=x_cord * 1 / 2, y=y_cord * 9 / 10, anchor="center"
    )

    Button(
        main_win,
        text="Create a Quiz",
        bg=bgc,
        fg=fgc,
        width=20,
        height=7,
        command=lambda: create_quiz(main_win),
    ).place(
        x=x_cord * 1 / 3, y=y_cord * 1 / 2, anchor="center"
    )

    Button(
        main_win,
        text="Class Review",
        bg=bgc,
        fg=fgc,
        width=20,
        height=7,
        command=lambda: view_students(main_win),
    ).place(
        x=x_cord * 2 / 3, y=y_cord * 1 / 2, anchor="center"
    )


# This allows teachers to create accounts for students
def register(win):
    win.destroy()
    reg = Tk()
    reg.title("Register")
    reg.geometry(size)
    reg.resizable(False, False)
    reg.configure(bg=bgc)
    lbls = [
        "Username",
        "Password",
        "Confirm Password",
        "Admin",
    ]
    for x in range(len(lbls)):
        Label(
            reg, text=lbls[x], bg=bgc, fg=fgc, font=def_font
        ).place(
            x=x_cord * 1 / 3,
            y=y_cord * 2 / 5 + 50 * x,
            anchor="center",
        )
    admin = StringVar(reg)
    admin.set("True")
    choices = ["True", "False"]

    Label(
        reg,
        text="Insert your details below to register your account",
        bg=bgc,
        fg=fgc,
        font=def_font,
    ).place(
        x=x_cord * 1 / 2, y=y_cord * 1 / 5, anchor="center"
    )
    new_user = Entry(reg, justify="center", width=25)
    new_pass = Entry(
        reg, show="*", justify="center", width=25
    )
    conf_pass = Entry(
        reg, show="*", justify="center", width=25
    )
    new_user.place(
        x=x_cord * 3 / 5, y=y_cord * 2 / 5, anchor="center"
    )
    new_pass.place(
        x=x_cord * 3 / 5,
        y=y_cord * 2 / 5 + 50,
        anchor="center",
    )
    conf_pass.place(
        x=x_cord * 3 / 5,
        y=y_cord * 2 / 5 + 100,
        anchor="center",
    )
    admin_opt = OptionMenu(reg, admin, *choices)
    admin_opt.place(
        x=x_cord * 3 / 5,
        y=y_cord * 2 / 5 + 150,
        anchor="center",
    )
    data = [new_user, new_pass, conf_pass, admin]
    Button(
        reg,
        text="Register",
        bg=bgc,
        fg=fgc,
        command=lambda: create_acc(data, reg),
    ).place(
        x=x_cord * 1 / 3, y=y_cord * 5 / 6, anchor="center"
    )
    Button(
        reg,
        text="Back",
        bg=bgc,
        fg=fgc,
        command=lambda: (
            reg.destroy(),
            main_screen_admin(),
        ),
    ).place(
        x=x_cord * 2 / 3, y=y_cord * 5 / 6, anchor="center"
    )


def view_students(win):
    win.destroy()
    pass


# From here the teachers can view their current test they're making and publish it to students


def create_quiz(win):
    win.destroy()
    quiz = Tk()
    quiz.geometry(size)
    quiz.configure(bg=bgc)
    quiz.resizable(False, False)
    topic = Text(quiz, width=20, height=4)
    topic.place(
        x=x_cord * 1 / 2, y=y_cord * 1 / 2, anchor="center"
    )
    lbls = [
        "Create a quiz",
        "Give the quiz a name and the topic it is based on",
        "Use the plus Icon to add a question",
        "Then give 4 answers for the student to select from",
    ]
    for lbl in range(len(lbls)):
        Label(
            quiz,
            bg=bgc,
            fg=fgc,
            text=lbls[lbl],
            font=def_font,
        ).place(
            x=x_cord * 1 / 2,
            y=y_cord * 1 / 5 + 35 * lbl,
            anchor="center",
        )
    create = Button(
        quiz,
        text="+",
        bg=bgc,
        fg=fgc,
        font=("System", 10),
        width=10,
        height=2,
        command=lambda: create_question(),
    )
    exit = Button(
        quiz,
        text="Exit",
        bg=bgc,
        fg=fgc,
        font=("System", 10),
        width=10,
        height=2,
        command=lambda: (
            main_screen_admin(),
            quiz.destroy(),
        ),
    )
    save_quiz = Button(
        quiz,
        text="Publish Quiz",
        bg=bgc,
        fg=fgc,
        font=("System", 10),
        width=10,
        height=2,
        command=lambda: (
            main_screen_admin(),
            db.open_data(),
            db.question_assigned_to_test(topic.get("1.0", 'end-1c')),
            db.close_data(),
            quiz.destroy(),
        ),
    )

    create.place(
        x=x_cord * 1 / 6, y=y_cord * 1 / 4, anchor="center"
    )
    exit.place(
        x=x_cord * 5 / 6, y=y_cord * 1 / 4, anchor="center"
    )
    save_quiz.place(
        x=x_cord * 5 / 6, y=y_cord * 4 / 5, anchor="center"
    )


# Gives GUI for creating questions including database input
def create_question():
    question = Tk()
    question.geometry(size)
    question.configure(bg=bgc)
    question.resizable(False, False)
    q_var_ent = Text(question, width=45, height=5)
    ans_1_ent = Entry(question, justify="center", width=25)
    ans_2_ent = Entry(question, justify="center", width=25)
    ans_3_ent = Entry(question, justify="center", width=25)
    ans_4_ent = Entry(question, justify="center", width=25)
    timer_ent = Entry(question, justify="center", width=25)
    q_details = [q_var_ent, ans_1_ent, ans_2_ent, ans_3_ent, ans_4_ent, timer_ent]
    lbls = [
        "Enter the Question here",
        "Enter correct answer here",
        "Wrong answer",
        "Wrong answer",
        "Wrong answer",
        "Timer",
    ]
    for entry in range(len(q_details)):
        if entry == 0:
            q_details[entry].place(
                x=x_cord * 1 / 2,
                y=y_cord * entry + 40,
                anchor="center",
            )

            Label(
                question,
                text=lbls[entry],
                bg=bgc,
                fg=fgc,
                font=def_font,
            ).place(
                x=x_cord * 1 / 6,
                y=y_cord * entry + 45,
                anchor="center",
            )
        q_details[entry].place(
            x=x_cord * 1 / 2,
            y=y_cord * entry / 6 + 50,
            anchor="center",
        )

        Label(
            question,
            text=lbls[entry],
            bg=bgc,
            fg=fgc,
            font=def_font,
        ).place(
            x=x_cord * 1 / 6,
            y=y_cord * entry / 6 + 50,
            anchor="center",
        )
    add_q_btn = Button(
        question,
        text="Create\nQuestion",
        bg=bgc,
        fg=fgc,
        width=20,
        height=3,
        command=lambda: (
            db.open_data(),
            db.add_question(q_details),
            db.close_data(),
            question.destroy(),
        ),
    )
    delete_q_btn = Button(
        question,
        text="Back",
        bg=bgc,
        fg=fgc,
        width=20,
        height=3,
        command=lambda: question.destroy(),
    )
    superscript_btn = Button(
        question,
        text='²',
        bg=bgc,
        fg=fgc,
        width=20,
        height=3,
        command=lambda: [question.focus_get()]
    )
    add_q_btn.place(
        x=x_cord * 5 / 6, y=y_cord * 1 / 3, anchor="center"
    )
    delete_q_btn.place(
        x=x_cord * 5 / 6, y=y_cord * 2 / 3, anchor="center"
    )


# This the main screen for the students, they can complete quizzes or view their progress
def main_screen_user():
    main_win = Tk()
    main_win.title("Main Window")
    main_win.geometry(size)
    main_win.configure(bg=bgc)
    main_lbls = [
        "Welcome Back",
        "Here you can either complete work or check your performance",
    ]
    for lbls in range(len(main_lbls)):
        Label(
            main_win,
            text=main_lbls[lbls],
            bg=bgc,
            fg=fgc,
            font=def_font,
        ).place(
            x=x_cord * 1 / 2,
            y=y_cord * 1 / 5 + 50 * lbls,
            anchor="center",
        )
    Button(
        main_win,
        text="Complete a Quiz",
        bg=bgc,
        fg=fgc,
        width=20,
        height=7,
        command=lambda: complete_quiz(main_win),
    ).place(
        x=x_cord * 1 / 3, y=y_cord * 1 / 2, anchor="center"
    )

    Button(
        main_win,
        text="Personal Review",
        bg=bgc,
        fg=fgc,
        width=20,
        height=7,
        command=lambda: view_progress(main_win),
    ).place(
        x=x_cord * 2 / 3, y=y_cord * 1 / 2, anchor="center"
    )

    Button(
        main_win,
        text="Log Out",
        bg=bgc,
        fg=fgc,
        width=20,
        height=3,
        command=lambda: (main_win.destroy(), login()),
    ).place(
        x=x_cord * 1 / 2, y=y_cord * 5 / 6, anchor="center"
    )


# This function retrieves the quizzes assigned to the user and lets them complete questions
def reset_tests():
    db.quiz_details = []


def time_out(win, frame, next_question):
    print("You ran out of time!")
    win.after(2000, quiz_active, win, frame, next_question)


# This is a countdown timer for the student to complete the question
def timer(
        time_left, time_tkvar, time_lbl, win, frame, question
):
    if submit_ans.has_been_called:
        pass
    else:
        time_left -= 1
        time_tkvar.set("Time left: " + str(time_left))
        if time_left == 0:
            question += 1
            time_out(win, frame, question)
            pass
        else:
            # this makes sure that the label updates every second by adding a callback to the event loop
            time_lbl.after(
                1000,
                timer,
                time_left,
                time_tkvar,
                time_lbl,
                win,
                frame,
                question,
            )


def submit_ans(correct, score, win, frame, next_question):
    submit_ans.has_been_called = True
    next_question += 1
    if correct == 1:
        score += 1
        print("Correct!")
        win.after(
            500,
            quiz_active,
            win,
            frame,
            next_question,
            score,
        )
    else:
        print("Incorrect")
        win.after(
            500,
            quiz_active,
            win,
            frame,
            next_question,
            score,
        )


def end_test(win, score, question):
    print("test has ended")
    win.destroy()
    end_screen = Tk()
    end_screen.geometry(size)
    end_screen.title("Quiz Complete!")
    end_screen.configure(bg=bgc)
    Label(
        end_screen,
        text="You Completed a quiz",
        fg=fgc,
        bg=bgc,
        font=def_font,
    ).place(x=x_cord / 2, y=y_cord * 1 / 7, anchor="center")
    Label(
        end_screen,
        text="You Scored "
             + str(score)
             + "/"
             + str(question),
        fg=fgc,
        bg=bgc,
        font=def_font,
    ).place(x=x_cord / 2, y=y_cord * 1 / 2, anchor="center")
    Button(
        end_screen,
        text="Exit",
        fg=fgc,
        bg=bgc,
        font=def_font,
        command=lambda: main_screen_user()
    ).place(x=x_cord * 4 / 5, y=y_cord / 5, anchor='center')
    db.end_test(score, question)
    db.close_data()


def quiz_active(win, frame, question=0, score=0):
    frame.destroy()
    if question > (len(db.question_details) - 1):
        end_test(win, score, question)
    else:
        if submit_ans.has_been_called:
            submit_ans.has_been_called = False
        time_for_q = db.question_details[question][0][2]
        current_time = StringVar(win)
        current_time.set("Time left: " + str(time))
        Label(
            win,
            text=db.question_details[question][0][1],
            bg=bgc,
            fg=fgc,
            font=def_font,
        ).place(
            x=x_cord / 2, y=y_cord / 10, anchor="center"
        )
        time_label = Label(
            win,
            textvariable=current_time,
            bg=bgc,
            fg=fgc,
            font=def_font,
        )
        time_label.place(
            x=x_cord * 4 / 5,
            y=y_cord * 1 / 10,
            anchor="center",
        )
        correct_ans = Button(
            win,
            text=db.answers[question][0][1],
            bg=bgc,
            fg=fgc,
            font=def_font,
            width=20,
            height=3,
            command=lambda: submit_ans(
                1, score, win, frame, question
            ),
        )
        incorrect_ans_1 = Button(
            win,
            text=db.answers[question][1][1],
            bg=bgc,
            fg=fgc,
            font=def_font,
            width=20,
            height=3,
            command=lambda: submit_ans(
                0, score, win, frame, question
            ),
        )
        incorrect_ans_2 = Button(
            win,
            text=db.answers[question][2][1],
            bg=bgc,
            fg=fgc,
            font=def_font,
            width=20,
            height=3,
            command=lambda: submit_ans(
                0, score, win, frame, question
            ),
        )
        incorrect_ans_3 = Button(
            win,
            text=db.answers[question][3][1],
            bg=bgc,
            fg=fgc,
            font=def_font,
            width=20,
            height=3,
            command=lambda: submit_ans(
                0, score, win, frame, question
            ),
        )
        ans_buttons = [
            correct_ans,
            incorrect_ans_1,
            incorrect_ans_2,
            incorrect_ans_3,
        ]
        # this randomly assigns the placement of the buttons so that the correct answer isn't always in the same place
        for elements in range(4):
            selected = random.choice(ans_buttons)
            if elements == 0:
                selected.place(
                    x=x_cord / 3,
                    y=y_cord / 3,
                    anchor="center",
                )
            elif elements == 1:
                selected.place(
                    x=x_cord * (2 / 3),
                    y=y_cord / 3,
                    anchor="center",
                )
            elif elements == 2:
                selected.place(
                    x=x_cord / 3,
                    y=y_cord * (2 / 3),
                    anchor="center",
                )
            else:
                selected.place(
                    x=x_cord * (2 / 3),
                    y=y_cord * (2 / 3),
                    anchor="center",
                )
            ans_buttons.remove(selected)
        # starts the timer after all the widgets have been created
        timer(
            time_for_q,
            current_time,
            time_label,
            win,
            frame,
            question,
        )
        win.mainloop()


# This function shows all of the quizzes available to the user and lets them load them
def complete_quiz(win):
    win.destroy()
    quiz = Tk()
    quiz.title("Quiz")
    quiz.geometry(size)
    quiz.configure(bg=bgc)
    quiz_area = Frame(
        quiz, width=x_cord, height=y_cord, bg=bgc
    )
    quiz_area.pack()
    db.retrieve_quizes()
    Label(
        quiz_area,
        text="Here are the quizzes available to you",
        bg=bgc,
        fg=fgc,
        font=def_font,
    ).place(x=x_cord / 2, y=y_cord / 10, anchor="center")
    Button(
        quiz_area,
        text="Back",
        fg=fgc,
        bg=bgc,
        font=def_font,
        command=lambda: (
            main_screen_user(),
            quiz.destroy(),
            reset_tests(),
        ),
    ).place(
        x=x_cord * 3 / 4, y=y_cord / 10, anchor="center"
    )
    x_pos = 1
    y_pos = 1
    for data in range(len(db.quiz_details)):
        if (data + 1) % 4 == 0 and data != 0:
            x_pos += 1
            y_pos = 1
        y_pos += 1
        Label(
            quiz_area,
            text=db.quiz_details[data],
            bg=bgc,
            fg=fgc,
            font=def_font,
        ).place(
            x=x_cord * (x_pos / 4),
            y=(y_cord * y_pos / 5) - 100,
            anchor="center",
        )
        Button(
            quiz_area,
            text="Complete This Quiz",
            command=lambda selected_quiz=data: (
                db.start_test(selected_quiz),
                quiz_active(quiz, quiz_area),
            ),
            bg=bgc,
            fg=fgc,
            font=def_font,
        ).place(x=x_cord * (x_pos / 4), y=(y_cord * y_pos / 5) - 50, anchor="center")


def stop_graph(win):
    win.quit()
    win.destroy()


# Shows the progress of the individual showing their past performance
def view_progress(win):
    win.destroy()
    progress = Tk()
    progress.geometry(size)
    progress.configure(bg=bgc)
    progress.title("Personal Progress")
    # using matplotlib to create the graph
    scores_over_time = Figure(figsize=(4, 3))
    canvas_scores = FigureCanvasTkAgg(scores_over_time, master=progress)
    all_points = db.retrieve_completed(1)
    # sort the points via date
    print(all_points)
    x_points = []
    y_points = []
    for point in range(len(all_points)):
        x_points.append(all_points[point][1])
        y_points.append(all_points[point][0])
    data = {'Date': x_points,
            'Percentage': y_points
            }
    scores_over_time.add_subplot(111).plot(x_points, y_points, 'bo')
    canvas_scores.draw()
    canvas_scores.get_tk_widget().place(x=x_cord / 4, y=y_cord / 4, anchor='center')
    scores_compared_to_average = Figure(figsize=(4, 3))
    canvas_scores_average = FigureCanvasTkAgg(scores_compared_to_average, master=progress)
    all_points = db.retrieve_completed(2)
    Label(
        progress,
        text="This is your Progress",
        bg=bgc,
        fg=fgc,
        font=def_font,
    ).place(x=x_cord / 2, y=(y_cord / 10) - 50, anchor='center')
    Button(
        progress,
        text="Back",
        bg=bgc,
        fg=fgc,
        font=def_font,
        command=lambda: (stop_graph(progress), main_screen_user())
    ).place(x=x_cord * 9 / 10, y=y_cord / 7, anchor='center')
    progress.mainloop()


if __name__ == "__main__":
    db = Database()
    submit_ans.has_been_called = False
    login()

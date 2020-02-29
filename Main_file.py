#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import Treeview
from Database_file import *
import time
import random

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

# I decided to use matplotlib to display the student data to the teacher and back to the student,
# for personal feedback
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
    email = str(create_vals[4].get())
    target = str(create_vals[5].get())
    db.create_account(user, password, conf_password, admin, email, target)
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
    # Creating Labels
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
    #Entry boxes for user data
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
    # passes login details to function to check them
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
    Button(
        log,
        text="Enable/Disable\nDark Theme",
        bg=bgc,
        fg=fgc,
        width=20,
        height=3,
        command=lambda: dark_theme(log),
    ).place(
        x=x_cord * 3 / 4, y=y_cord * 9 / 10, anchor="center"
    )
    # tkinter function to keep awaiting user input
    log.mainloop()

def dark_theme(win):
    global bgc, fgc
    win.destroy()
    if bgc == "#4281A4" and fgc == "#EEEBD3":
        bgc = "#262730"
        fgc = "#FBFBF2"
    elif bgc == "#262730" and fgc == "#FBFBF2":
        bgc = "#4281A4"
        fgc = "#EEEBD3"
    login()

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
        "Email",
        "Target",
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
    target = StringVar(reg)
    target.set("N/A")
    grades = ["N/A", "A*", "A", "B", "C", "D", "E"]
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
    new_email = Entry(reg, justify='center',  width=40)
    new_user.place(
        x=x_cord * 3 / 5, y=y_cord * 2 / 5, anchor="center"
    )
    new_email.place(
        x=x_cord * 3 / 5, y=(y_cord * 3 / 5) + 50, anchor="center"
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
    # Allowing an admin to create a standard or admin account
    admin_opt = OptionMenu(reg, admin, *choices)
    admin_opt.place(
        x=x_cord * 3 / 5,
        y=y_cord * 2 / 5 + 150,
        anchor="center",
    )
    # Lets teachers set targets for students
    target_opt = OptionMenu(reg, target, *grades)
    target_opt.place(
        x=x_cord * 3 / 5,
        y=y_cord * 3 / 5 + 100,
        anchor="center"
    )
    data = [new_user, new_pass, conf_pass, admin, new_email, target]
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
    progress = Tk()
    graph_frame = Frame(progress)
    progress.geometry(size)
    progress.configure(bg=bgc)
    progress.title("Class Progress")
    # using matplotlib to create the graph
    all_points = db.retrieve_completed(1, user=db.first_user())
    renamed_points = []
    for point in range(len(all_points)):
        renamed_points.append([float(all_points[point][0]), point])
    x_points, y_points, x_index = bubble_sorting_data(renamed_points)
    scores_over_time = Figure(figsize=(5, 4), dpi=80)
    canvas_scores = FigureCanvasTkAgg(scores_over_time, master=graph_frame)
    ax_1 = scores_over_time.add_subplot(111)
    ax_1.set_xlabel('Homework-Number')
    ax_1.set_ylabel('Student Percentage %')
    # this is to make sure the x-axis only shows integers
    rectangles = ax_1.bar(x_index, y_points, 0.25)
    target_rect = ax_1.bar(x_index, db.user_target(x_index), 0.25)
    ax_1.set_xticklabels(x_points)
    ax_1.xaxis.set_major_locator(MaxNLocator(integer=True))
    canvas_scores.draw()
    canvas_scores.get_tk_widget().place(x=x_cord / 4, y=(y_cord / 4) + 25, anchor='center')

    Label(
        progress,
        text="This is your Classes Progress",
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


# From here the teachers can view their current test they're making and publish it to students

def create_quiz(win):
    win.destroy()
    quiz = Tk()
    quiz.geometry(size)
    quiz.configure(bg=bgc)
    quiz.resizable(False, False)
    topic = Text(quiz, width=35, height=4, font=('quicksand', 11))
    topic.place(
        x=x_cord * 1 / 2, y=y_cord * 1 / 2, anchor="center"
    )
    tree = Treeview(quiz, column=("column1", "column2"), show="headings")
    tree.heading("#1", text="Question")
    tree.heading("#2", text="Question No.")
    for question in range(len(db.current_questions)):
        insert_tree_vals = tree.insert("", "end", text=db.question_names[question], values=(db.question_names[question], question+1))
    tree.update()
    tree.place(x=x_cord / 2, y=y_cord * 4 / 5, anchor="center")
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
        command=lambda: [quiz.destroy(), create_question(tree)]
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
            db.current_questions.clear(),
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
            db.current_questions.clear(),
            quiz.destroy(),
        ),
    )
    # button to remove the question from the quiz
    delete_question = Button(
        quiz,
        text="Delete Question",
        bg=bgc,
        fg=fgc,
        font=("System", 10),
        width=20,
        height=2,
        command=lambda: db.remove_question(tree.selection()[0], tree)
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
    delete_question.place(
        x=x_cord * 1 / 5, y=y_cord * 4 / 5, anchor="center"
    )


def insert_integral(root):
    focus = root.focus_get()
    focus.insert('insert', '∫')


# Gives GUI for creating questions including database input
def create_question(tree):
    question = Tk()
    question.geometry(size)
    question.configure(bg=bgc)
    question.resizable(False, False)
    q_var_ent = Text(question, width=45, height=5, font=('Quicksand', 11))
    ans_1_ent = Text(question, width=25, height=1, font=('Quicksand', 8))
    ans_2_ent = Text(question, width=25, height=1, font=('Quicksand', 8))
    ans_3_ent = Text(question, width=25, height=1, font=('Quicksand', 8))
    ans_4_ent = Text(question, width=25, height=1, font=('Quicksand', 8))
    timer_ent = Text(question, width=25, height=1, font=('Quicksand', 8))
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
            create_quiz(question),
        ),
    )
    delete_q_btn = Button(
        question,
        text="Back",
        bg=bgc,
        fg=fgc,
        width=20,
        height=3,
        command=lambda: create_quiz(question)
    )
    superscript_btn = Button(
        question,
        text='²',
        bg=bgc,
        fg=fgc,
        width=10,
        height=2,
        command=lambda: change_offset(question, 'super')
    )
    subscript_btn = Button(
        question,
        text='ₐ',
        bg=bgc,
        fg=fgc,
        width=10,
        height=2,
        command=lambda: change_offset(question, 'sub')
    )
    integral_btn = Button(
        question,
        text='∫',
        bg=bgc,
        fg=fgc,
        width=10,
        height=2,
        command=lambda: insert_integral(question)
    )
    add_q_btn.place(
        x=x_cord * 5 / 6, y=y_cord * 1 / 3, anchor="center"
    )
    delete_q_btn.place(
        x=x_cord * 5 / 6, y=y_cord * 2 / 3, anchor="center"
    )
    superscript_btn.place(
        x=x_cord * 5 / 7, y=y_cord * 1 / 8, anchor="center"
    )
    subscript_btn.place(
        x=x_cord * 5 / 7, y=y_cord * 1 / 5, anchor="center"
    )
    integral_btn.place(
        x=x_cord * 7 / 8, y=y_cord * 1 / 5, anchor="center"
    )
    question.mainloop()

# a function to return the window focus and let an entry be inserted to that focus
def change_offset(root, offset_type):
    entry_box = root.focus_get()
    offset = Tk()
    offset.geometry('300x400')
    offset.configure(bg=bgc)
    Label(offset, text='Insert the text that\nyou would like with an offset',
          bg=bgc, fg=fgc).place(x=150, y=100, anchor='center')
    ent = Entry(offset)
    ent.place(x=150, y=200, anchor='center')
    if offset_type == 'super':
        enter_btn = Button(
            offset,
            text='Enter',
            bg=bgc,
            fg=fgc,
            command=lambda: [entry_box.insert('insert', to_sup(ent.get())), offset.destroy()]
        )
        enter_btn.place(x=150, y=350, anchor='center')
    elif offset_type == 'sub':
        enter_btn = Button(
            offset,
            text='Enter',
            bg=bgc,
            fg=fgc,
            command=lambda: [entry_box.insert('insert', to_sub(ent.get())), offset.destroy()]
        )
        enter_btn.place(x=150, y=350, anchor='center')
    else:
        messagebox.showerror('Coding Error', 'No offset type specified')

# dictionary for all the superscript characters
# checks that every character in the input is available before allowing the dictionary to be used
def to_sup(s):
    sups = {'1': u'\xb9',
            '0': u'\u2070',
            '3': u'\xb3',
            '2': u'\xb2',
            '5': u'\u2075',
            '4': u'\u2074',
            '7': u'\u2077',
            '6': u'\u2076',
            '9': u'\u2079',
            '8': u'\u2078',
            '+': u'\u207a',
            '-': u'\u207b',
            'i': u'\u2071'}
    for characters in range(len(s)):
        counter = 0
        found = False
        for super_version in sups:
            counter += 1
            if s[characters] == super_version:
                found = True
                pass
            if counter == len(sups) and not found:
                messagebox.showerror('Error', 'Character not found')
                return ""
    return ''.join([sups[i] for i in s])

# same as above but for subscript characters instead
def to_sub(s):
    subs = {'1': u'\u2081',
            '0': u'\u2080',
            '3': u'\u2083',
            '2': u'\u2082',
            '5': u'\u2085',
            '4': u'\u2084',
            '7': u'\u2087',
            '6': u'\u2086',
            '9': u'\u2089',
            '8': u'\u2088',
            '+': u'\u208a',
            '-': u'\u208b',
            'i': u'\u1d62',
            'a': u'\u2090',
            'e': u'\u2091',
            't': u'\u209c'}
    for characters in range(len(s)):
        counter = 0
        found = False
        for super_version in subs:
            counter += 1
            if s[characters] == super_version:
                found = True
                pass
            if counter == len(subs) and not found:
                messagebox.showerror('Error', 'Character not found')
                return ""
    return ''.join([subs[i] for i in s])


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

# callback loop for the time out state when a user runs out of time for a question
def time_out(win, frame, next_question):
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

# submitting an answer and checkin against the database before moving on to next question
def submit_ans(correct, score, win, frame, next_question):
    submit_ans.has_been_called = True
    next_question += 1
    if correct == 1:
        score += 1
        win.after(
            500,
            quiz_active,
            win,
            frame,
            next_question,
            score,
        )
    else:
        win.after(
            500,
            quiz_active,
            win,
            frame,
            next_question,
            score,
        )

# results screen for the test that has just been completed
def end_test(win, score, question):
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
        command=lambda: (end_screen.destroy(), main_screen_user())
    ).place(x=x_cord * 4 / 5, y=y_cord / 5, anchor='center')
    db.end_test(score, question)
    db.close_data()

# recursive function for the test which repeats for each question
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
    if len(db.quiz_details) > 9:
        length = 9
    else:
        length = len(db.quiz_details)
    for data in range(length):
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

# external function to stop the graph as if the window is just destroyed then an error is created
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
    all_points = db.retrieve_completed(1)
    renamed_points = []
    for point in range(len(all_points)):
        renamed_points.append([float(all_points[point][0]), point])
    x_points, y_points, x_index = bubble_sorting_data(renamed_points)
    scores_over_time = Figure(figsize=(5, 4), dpi=80)
    canvas_scores = FigureCanvasTkAgg(scores_over_time, master=progress)
    ax_1 = scores_over_time.add_subplot(111)
    ax_1.set_xlabel('Homework-Number')
    ax_1.set_ylabel('Percentage %')
    # this is to make sure the x-axis only shows integers
    rectangles = ax_1.bar(x_index, y_points, 0.25)
    target_rect = ax_1.bar(x_index, db.user_target(x_index), 0.25)
    ax_1.set_xticklabels(x_points)
    ax_1.xaxis.set_major_locator(MaxNLocator(integer=True))
    canvas_scores.draw()
    canvas_scores.get_tk_widget().place(x=x_cord / 4, y=(y_cord / 4) + 25, anchor='center')
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
    for weakness in range(len(db.user_weakness())):
        Label(
            progress,
            text=db.user_weakness()[weakness],
            bg=bgc,
            fg=fgc,
            font=def_font,
        ).place(x=x_cord * 3 / 4, y=(y_cord * 7 / 10) + (50 * weakness), anchor='center')

    progress.mainloop()


def bubble_sorting_data(graph_data):
    for it in range(len(graph_data)):
        for sub_it in range(len(graph_data) - 1):
            try:
                if graph_data[sub_it][0] > graph_data[sub_it + 1][0]:
                    temp = graph_data[sub_it]
                    graph_data[sub_it] = graph_data[sub_it + 1]
                    graph_data[sub_it + 1] = temp
            except:
                pass
    x_points = ['',]
    y_points = []
    amount_of_x = []
    for size in range(len(graph_data)):
        y_points.append(graph_data[size][0])
        x_points.append(("HW: " + str(graph_data[size][1] + 1)))
        amount_of_x.append(graph_data[size][1] + 1)
    if len(y_points) == 1:
        y_points.append(0)
        x_points.append('')
        amount_of_x.append(amount_of_x[-1]+1)
    return x_points, y_points, amount_of_x


if __name__ == "__main__":
    db = Database()
    submit_ans.has_been_called = False
    login()

from tkinter import *
from Database_file import *
from Main_file import *
from Teacher_Side import *
from tkinter import messagebox
import hashlib
import uuid

db = database()

x_cord = 1200
y_cord = 750
size = '{}x{}'.format(x_cord, y_cord)
bgc = '#4281A4'
fgc = '#EEEBD3'
def_font = ('Times New Roman', 20)


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
        command=lambda: (main_win.destroy(), login()),
    ).place(x=x_cord * 1 / 2, y=y_cord * 5 / 6, anchor='center')

    main_win.mainloop()


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
    for data in range(int(len(db.quiz_details) / 3)):
        x_pos = data % 3
        Label(quiz, text=db.quiz_details[data], bg=bgc, fg=fgc, font=def_font
              ).place(x=x_pos + 150, y=(y_cord * data / 3) + 100, anchor='center')
        Button(quiz, text="Complete This Quiz", bg=bgc, fg=fgc, font=def_font
               ).place(x=x_pos + 150, y=(y_cord * data / 3) + 150, anchor='center')

    quiz.mainloop()


def view_progress(win):
    pass

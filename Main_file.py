#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
import hashlib
import uuid
from Database_file import *
from Student_Side import *
from Teacher_Side import *

# These are the base size and colour variables for the program
# I put these here so that if i wanna change the size of my window everything else will change in proportion

x_cord = 1200
y_cord = 750
size = '{}x{}'.format(x_cord, y_cord)
bgc = '#4281A4'
fgc = '#EEEBD3'
def_font = ('Times New Roman', 20)


# Creates account by taking data from entries
# and then passing them as paraneters to the database class methods

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



## Checks if the inputted password matches the user password on the database

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

## This is the login form for the website, it passes the inputs into the database and validates them
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
    Button(log, text='Login', bg=bgc, fg=fgc, command=lambda : \
           login_check(data, log)).place(x=x_cord * 1 / 2, y=y_cord * 5
            / 7, anchor='center')
    Button(log, text='Exit', bg=bgc, fg=fgc, command=lambda : \
           log.destroy()).place(x=x_cord * 1 / 2, y=y_cord * 4 / 5,
                                anchor='center')
    Button(log, text='Temporary', bg=bgc, fg=fgc, command=lambda : \
           register(log)).place(x=x_cord * 1 / 2, y=y_cord * 6 / 7,
                                anchor='center')
    log.mainloop()


if __name__ == '__main__':
    db = database()
    Login()

import mysql.connector
import tkinter as tk
from tkinter import messagebox

connectionDB = ''

def OpenConnection():
    root = tk.Tk()
    root.wm_title("CONNECTION")
    tk.Label(root, text="Host:").grid(row=1)
    tk.Label(root, text="User:").grid(row=2)
    tk.Label(root, text="Password:").grid(row=3)
    tk.Label(root, text="Database:").grid(row=4)
    e1 = tk.Entry(root)
    e2 = tk.Entry(root)
    e3 = tk.Entry(root, show="*")
    e4 = tk.Entry(root)
    e1.grid(row=1, column=1)
    e2.grid(row=2, column=1)
    e3.grid(row=3, column=1)
    e4.grid(row=4, column=1)

    def connect():
        h = e1.get()
        u = e2.get()
        p = e3.get()
        d = e4.get()
        while True:
            try:
                #global connectionDB
                connectionDB = mysql.connector.connect(host=h, user=u, passwd=p, database=d)
                break
            except mysql.connector.Error as err:
                messagebox.showerror("Error","Something went wrong: {}".format(err))
        print("WHILE LOOP EXITED")

    tk.Button(root, text="Connect", command=lambda: connect()).grid(row=5)
    root.mainloop()

    return connectionDB

"""
h = input("Host: ")
u = input("User: ")
p = input("Password: ")
d = input("Database: ")
connectionDB = mysql.connector.connect(host=h, user=u, passwd=p, database=d)
return connectionDB
"""

def GetCursor(db):
    return db.cursor()


def CloseConnection(db):
    db.commit()
    db.close()
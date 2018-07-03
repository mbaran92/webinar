import tkinter as tk
from tkinter import ttk

import mysql.connector
import datetime
import re

import matplotlib
matplotlib.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# import matplotlib.animation as animation
# from matplotlib import style
#
# import urllib
# import json
#
# import pandas as pd
# import numpy as np
#
# from matplotlib import pyplot as plt

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

# style.use("ggplot")
# f = Figure()
# a = f.add_subplot(111)



def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Message")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def tutorial():
    # def leavemini(what):
    #     what.destroy()

    def page2():
        tut.destroy()
        tut2 = tk.Tk()

        def page3():
            tut2.destroy()
            tut3 = tk.Tk()

            tut3.wm_title("Part 3!")
            label=ttk.Label(tut3, text="Part 3", font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)
            B13=ttk.Button(tut3, text="Done!", command=tut3.destroy)
            B13.pack()
            tut3.mainloop()

        tut2.wm_title("Part 2!")
        label = ttk.Label(tut2, text="Part 2", font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(tut2, text="Next", command=page3)
        B1.pack()
        tut2.mainloop()

    tut = tk.Tk()
    tut.wm_title("Tutorial")
    label = ttk.Label(tut, text="What do you need help with?", font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)

    B1 = ttk.Button(tut, text="Overview of the application", command=page2)
    B1.pack()
    B2 = ttk.Button(tut, text="How do I trade with this client", command=lambda:popupmsg("Not yet completed."))
    B2.pack()
    B3 = ttk.Button(tut, text="Indicator Questions/Help", command=lambda:popupmsg("Not yet completed."))
    B3.pack()

    tut.mainloop()

class ContactsApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self,"Contacts Client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar,tearoff=0)
        filemenu.add_command(label="Save settings",command = lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        actionsmenu = tk.Menu(menubar, tearoff=0)
        actionsmenu.add_command(label="Add New Contact", command=lambda: popupmsg("This will soon let you add a new contact."))
        actionsmenu.add_command(label="Remove Contact", command=lambda: popupmsg("This will soon let you remove a contact."))
        actionsmenu.add_command(label="Update Contact(s)",
                                command=lambda: popupmsg("This will soon let you update a contact record (e.g. add note)."))
        actionsmenu.add_separator()
        actionsmenu.add_command(label="Find Contact(s)", command=lambda: popupmsg("This will soon let you search the database for a contact."))
        menubar.add_cascade(label="Actions", menu=actionsmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Tutorial", command=tutorial)
        menubar.add_cascade(label="Help", menu=helpmenu)

        tk.Tk.config(self,menu=menubar)

        self.frames = {}
        for F in (StartPage, SearchContactsPage, ContactPage, AddContactPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="uGRIDD Webinar Contacts Application", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Enter", command=lambda: controller.show_frame(ContactPage))
        button1.pack()

        button2 = tk.Button(self, text="Quit", command=quit)
        button2.pack()

class ContactPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Contact Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text="Search Contacts", command=lambda: controller.show_frame(SearchContactsPage))
        button2.pack()
        button3 = tk.Button(self, text="Add Contacts", command=lambda: controller.show_frame(AddContactPage))
        button3.pack()


class SearchContactsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pagelabel = tk.Label(self, text="Search Contacts", font=LARGE_FONT)
        pagelabel.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text="Contacts Page", command=lambda: controller.show_frame(ContactPage))
        button2.pack()

        def fetch(entries):
            for entry in entries:
                field = entry[0]
                text = entry[1].get()
                print('%s: "%s"' % (field, text))

        def makeform(root, fields):
            entries = []
            for field in fields:
                row = tk.Frame(root)
                lab = tk.Label(row, width=15, text=field, anchor='w')
                ent = tk.Entry(row)
                row.pack(side='top', fill='x', padx=5, pady=5)
                lab.pack(side='left')
                ent.pack(side='right', expand='yes', fill='x')
                entries.append((field, ent))
            return entries

        fields = 'Email Address', 'First Name', 'Last Name'
        ents = makeform(self, fields)
        self.bind('<Return>', (lambda event, e=ents: fetch(e)))
        b1 = tk.Button(self, text='Show',
                    command=(lambda e=ents: fetch(e)))
        b1.pack(side='left', padx=5, pady=5)

        # def show_entry_fields():
        #     print("First Name: %s\nLast Name: %s"
        #           % (e1.get(), e2.get()))
        # label1 = tk.Label(self, text="First Name")
        # label1.grid(row=10)
        # e1=tk.Entry(self)
        # e1.insert(0, "Enter First Name")
        # e1.grid(row=10, column=11)
        # label2 = tk.Label(self, text="Last Name")
        # label2.grid(row=11)
        # e2=tk.Entry(self)
        # e2.insert(0, "Enter Last Name")
        # e2.grid(row=11, column=11)
        #
        # buttonSubmit = tk.Button(self, text='Submit', command=show_entry_fields)
        # buttonSubmit.pack()

class AddContactPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pagelabel = tk.Label(self, text="Add Contact", font=LARGE_FONT)
        pagelabel.grid(row=0, pady=10, padx=10)

        button1 = tk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=0)
        button2 = tk.Button(self, text="Contacts Page", command=lambda: controller.show_frame(ContactPage))
        button2.grid(row=1, column=1)

        labelEmail = tk.Label(self, width=20, text="E-mail (Username)", anchor='w')
        entryEmail = tk.Entry(self)
        labelEmail.grid(row=3, column=0)
        entryEmail.grid(row=3, column=1)
        buttonSubmit = tk.Button(self, text="Submit", command=lambda: callback())
        buttonSubmit.grid(row=10)

        def callback():
            email = entryEmail.get()
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("Added Email: "+ email)
                popupmsg("Added Email:" + email)
            else:
                print("Invalid E-mail: " + email)


app = ContactsApp()
app.geometry("600x300")
app.mainloop()
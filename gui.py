import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
from datetime import datetime
import re
import connection

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

contactTableFields = ["EmailAddress","FirstName","LastName","Source","UserSince","EventbriteContactList","AddedDate","RemovedReason","RemoveDate","Note"]
myDB = connection.OpenConnection()
cursor = connection.GetCursor(myDB)

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Message")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    okayButton = ttk.Button(popup, text="Okay", command = popup.destroy)
    okayButton.pack()
    popup.mainloop()


def ask_quit():
    if messagebox.askokcancel("Quit", "Are you sure you want to quit the application?"):
        connection.CloseConnection(myDB)
        quit()

def tutorial():
    # not program-ending error result

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

        self.frames = {}
        for F in (StartPage, SearchContactsPage, AddContactPage, RemoveContactPage, UpdateContactPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar,tearoff=0)
        filemenu.add_command(label="Home", command=lambda: self.show_frame(StartPage))
        filemenu.add_command(label="Save settings",command = lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Quit App", command=ask_quit)
        menubar.add_cascade(label="File", menu=filemenu)

        actionsmenu = tk.Menu(menubar, tearoff=0)
        actionsmenu.add_command(label="Search Contacts", command=lambda: self.show_frame(SearchContactsPage))
        actionsmenu.add_separator()
        actionsmenu.add_command(label="Add New Contact", command=lambda: self.show_frame(AddContactPage))
        actionsmenu.add_command(label="Remove Contact", command=lambda: popupmsg("This will soon let you remove a contact."))
        actionsmenu.add_command(label="Update Contact(s)", command=lambda: popupmsg("This will soon let you update a contact record (e.g. add note)."))
        menubar.add_cascade(label="Actions", menu=actionsmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Tutorial", command=tutorial)
        menubar.add_cascade(label="Help", menu=helpmenu)

        tk.Tk.config(self,menu=menubar)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="uGRIDD Webinar Contacts Application", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # ADD WELCOME TEXT HERE

class SearchContactsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pagelabel = tk.Label(self, text="Search Contacts", font=LARGE_FONT)
        pagelabel.grid(row=0, columnspan=4, pady=10, padx=10)

        labelEmail = tk.Label(self, width=20, text="E-mail (Username)", anchor='w').grid(row=2, column=0, columnspan=2)
        entryEmail = tk.Entry(self)
        entryEmail.grid(row=2, column=2, columnspan=2)
        labelFirstName = tk.Label(self, width=20, text="First Name", anchor='w').grid(row=3, column=0, columnspan=2)
        entryFirstName = tk.Entry(self)
        entryFirstName.grid(row=3, column=2, columnspan=2)
        labelLastName = tk.Label(self, width=20, text="Last Name", anchor='w').grid(row=4, column=0, columnspan=2)
        entryLastName = tk.Entry(self)
        entryLastName.grid(row=4, column=2, columnspan=2)
        labelSource = tk.Label(self, width=20, text="Source", anchor='w').grid(row=5, column=0, columnspan=2)
        entrySource = tk.Entry(self)
        entrySource.grid(row=5, column=2, columnspan=2)
        labelUserSince = tk.Label(self, width=20, text="Account Since", anchor='w').grid(row=6, column=0, columnspan=2)
        entryUserSince = tk.Entry(self)
        entryUserSince.grid(row=6, column=2, columnspan=2)
        entryUserSince.insert(tk.END, "YYYY-MM-DD hh:mm:ss")
        labelContactList = tk.Label(self, width=20, text="Eventbrite Contact List", anchor='w').grid(row=7, column=0, columnspan=2)
        entryContactList = tk.Entry(self)
        entryContactList.grid(row=7, column=2, columnspan=2)
        labelAddedDate = tk.Label(self, width=20, text="Added Date", anchor='w').grid(row=8, column=0,columnspan=2)
        entryAddedDate = tk.Entry(self)
        entryAddedDate.grid(row=8, column=2, columnspan=2)
        labelRemovedReason = tk.Label(self, width=20, text="Removed Reason", anchor='w').grid(row=9, column=0, columnspan=2)
        entryRemovedReason = tk.Entry(self)
        entryRemovedReason.grid(row=9, column=2, columnspan=2)
        labelRemovedDate = tk.Label(self, width=20, text="Remove Date", anchor='w').grid(row=10, column=0,columnspan=2)
        entryRemovedDate = tk.Entry(self)
        entryRemovedDate.grid(row=10, column=2, columnspan=2)
        labelNote = tk.Label(self, width=20, text="Note", anchor='w').grid(row=11, column=0,columnspan=2)
        entryNote = tk.Entry(self)
        entryNote.grid(row=11, column=2, columnspan=2)

        buttonSubmit = tk.Button(self, text="Submit", command=lambda: find())
        buttonSubmit.grid(row=15)
        #buttonClear = tk.Button(self, text="Clear", command=)

        def find():
            entries = [entryEmail.get(),entryFirstName.get(),entryLastName.get(),entrySource.get(),entryUserSince.get(),entryContactList.get(),entryAddedDate.get(),entryRemovedReason.get(),entryRemovedDate.get(),entryNote.get()]

            workingDBTable = "contactstest"
            sqlStatement = "SELECT * FROM "+ workingDBTable +" WHERE"

            if len(entries) == entries.count(""): popupmsg("No search criteria selected.")
            else: pass

            i = 0
            whereClause = 0
            values = ""
            while i<len(entries):
                if entries[i] =="":pass
                else:
                    whereClause += 1
                    if whereClause >= 2:
                        sqlStatement = sqlStatement + " AND"
                        values = values + ","
                    else: pass
                    sqlStatement = sqlStatement + " " + contactTableFields[i] + "=%s"
                    values = values + "'"+ entries[i] + "'"
                i += 1
            sql = '"' + sqlStatement + '"'
            val = '[(' + values + ')]'
            cursor.execute(sql, val)
            result = cursor.fetchall()
            print(result)
            message = 'Code for SQL statement:\nsql = ' + sql + '\nval = ' + val + '\ncursor.execute(sql, val)'
            popupmsg(message)

class AddContactPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pagelabel = tk.Label(self, text="Add Contact", font=LARGE_FONT)
        pagelabel.grid(row=0, columnspan=4, pady=10, padx=10)

        labelEmail = tk.Label(self, width=20, text="E-mail (Username)", anchor='w').grid(row=2, column=0, columnspan=2)
        entryEmail = tk.Entry(self)
        entryEmail.grid(row=2, column=2, columnspan=2)
        labelFirstName = tk.Label(self, width=20, text="First Name", anchor='w').grid(row=3, column=0, columnspan=2)
        entryFirstName = tk.Entry(self)
        entryFirstName.grid(row=3, column=2, columnspan=2)
        labelLastName = tk.Label(self, width=20, text="Last Name", anchor='w').grid(row=4, column=0, columnspan=2)
        entryLastName = tk.Entry(self)
        entryLastName.grid(row=4, column=2, columnspan=2)
        labelSource = tk.Label(self, width=20, text="Source", anchor='w').grid(row=5, column=0, columnspan=2)
        entrySource = tk.Entry(self)
        entrySource.insert(tk.END,"'uGRIDD User' if from User Management")
        entrySource.grid(row=5, column=2, columnspan=2)
        labelUserSince = tk.Label(self, width=20, text="Account Since", anchor='w').grid(row=6, column=0, columnspan=2)
        entryUserSince = tk.Entry(self)
        entryUserSince.grid(row=6, column=2, columnspan=2)
        entryUserSince.insert(tk.END, "YYYY-MM-DD hh:mm:ss")
        labelNote = tk.Label(self, width=20, text="Note", anchor='w').grid(row=7, column=0, columnspan=2)
        entryNote = tk.Entry(self)
        entryNote.grid(row=7, column=2, columnspan=2)

        buttonSubmit = tk.Button(self, text="Submit", command=lambda: callback())
        buttonSubmit.grid(row=10)

        def callback():
            entries = {
                "email" : entryEmail.get(),
                "firstname" : entryFirstName.get(),
                "lastname" : entryLastName.get(),
                "source" : entrySource.get(),
                "usersince" : entryUserSince.get(),
                "note": entryNote.get()
            }
            invalidEntries = []

            workingDBTable = "contactstest"
            sqlStatement = '"INSERT INTO ' + workingDBTable + ' (EmailAddress,FirstName,LastName,Source,UserSince,EventbriteContactList,AddedDate,RemovedReason,RemoveDate,Note) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"'

            for i in entries:
                if entries[i] =="":
                    entries[i] = None
                else: pass

            #Require email entry
            if entries["email"] == None: popupmsg("Email is required.")
            else:
                #Check if the email is already in database
                emailFound = False

                sql = "SELECT COUNT(*) FROM contactstest WHERE EmailAddress='"+ entries["email"] +"'"


                if emailFound:
                    popupmsg("Email found in table. Duplicate email addresses not allowed.")
                else:
                    #Check for correct email format
                    if re.match(r"[^@]+@[^@]+\.[^@]+", entries["email"]): pass
                    else: invalidEntries.append("Invalid email format")

                    #Check for correct date format
                    if entries["usersince"] == None: pass
                    else:
                        try: datetime.strptime(entries["usersince"], '%Y-%m-%d %H:%M:%S')
                        except ValueError: invalidEntries.append("Invalid date format (Account Since)")
                        else: pass

                    if len(invalidEntries) == 0:
                        #All checks OK, create SQL Statement
                        sql = sqlStatement
                        val = [(entries["email"], entries["firstname"], entries["lastname"], entries["source"], entries["usersince"], None,datetime.now().strftime("%Y-%m-%d %H:%M:%S"), None, None, entries["note"])]
                        #mycursor.executemany(sql, val)
                        message = "Code for SQL statement:\nsql = " + sql +"\nval = " + str(val) + "\nmycursor.executemany(sql, val)"
                        popupmsg(message)
                    else:
                        #Prompt for corrections
                        message = "INVALID ENTRIES:"
                        for i in invalidEntries:
                            message = message + "\n" + i
                        popupmsg(message)


class RemoveContactPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Remove Contact Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

class UpdateContactPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Update Contact Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


app = ContactsApp()
app.geometry("600x300")
app.protocol("WM_DELETE_WINDOW", ask_quit)
app.mainloop()


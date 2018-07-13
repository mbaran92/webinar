import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
from datetime import datetime
import re
import mysql.connector
import sys
import os

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

contactTableFields = ["EmailAddress","FirstName","LastName","Source","UserSince","EventbriteContactList","AddedDate","RemovedReason","RemoveDate","Note"]
contactFieldsRead = ["E-mail (Username)","First Name","Last Name","Source","Account Since","Eventbrite Contact List","Added Date","Removed Reason","Remove Date","Note"]
workingDBTable = "contactstest"


#def restartApp():
#    if messagebox.askokcancel("Restart", "All entries will be erased.\nAre you sure you want to restart the application?"):
#        if myDB == '': pass
#        else: connection.CloseConnection(myDB)
#        python = sys.executable
#        os.execl(python, python, *sys.argv)

class ContactsApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.myDB = ''
        self.cursor = ''

        self.wm_protocol("WM_DELETE_WINDOW", lambda: self.ask_quit())

        tk.Tk.wm_title(self,"Contacts Client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, SearchContactsPage, AddContactPage, UpdateContactPage, RemoveContactPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar,tearoff=0)
        filemenu.add_command(label="Home", command=lambda: self.show_frame(StartPage))
        #filemenu.add_command(label="Save settings",command = lambda: messagebox.showinfo("Not yet supported","Not supported just yet!"))
        filemenu.add_separator()
        #filemenu.add_command(label="Restart App", command=restartApp)
        filemenu.add_command(label="Quit App", command=lambda: self.ask_quit())
        menubar.add_cascade(label="File", menu=filemenu)

        actionsmenu = tk.Menu(menubar, tearoff=0)
        actionsmenu.add_command(label="Search Contacts", command=lambda: self.show_frame(SearchContactsPage))
        actionsmenu.add_separator()
        actionsmenu.add_command(label="Add New Contact", command=lambda: self.show_frame(AddContactPage))
        actionsmenu.add_command(label="Update Contact", command=lambda: self.show_frame(UpdateContactPage))
        actionsmenu.add_command(label="Remove Contact", command=lambda: self.show_frame(RemoveContactPage))
        menubar.add_cascade(label="Actions", menu=actionsmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Tutorial", command=lambda: messagebox.showinfo("Not yet supported","Not supported just yet!"))
        menubar.add_cascade(label="Help", menu=helpmenu)

        tk.Tk.config(self,menu=menubar)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def openConnection(self):
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
                    self.myDB = mysql.connector.connect(host=h, user=u, passwd=p, database=d)
                    break
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", "Something went wrong: {}".format(err))
            self.cursor = self.myDB.cursor()
            root.destroy()

        tk.Button(root, text="Connect", command=lambda: connect()).grid(row=5)
        root.mainloop()

    def createConnection(self):
        self.openConnection()

    def closeConnection(self):
        self.myDB.commit()
        self.myDB.close()

    def ask_quit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit the application?"):
            if self.myDB == '':
                pass
            else:
                self.closeConnection()
            quit()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="uGRIDD Webinar Contacts Application", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # ADD WELCOME TEXT HERE

        tk.Button(self, text="Open Connection", command=lambda: controller.createConnection()).pack()


class SearchContactsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Search Contacts", font=LARGE_FONT).grid(row=0, columnspan=4, pady=10, padx=10)
        #self.grid_columnconfigure(1, weight=1)

        tk.Label(self, width=20, text="E-mail (Username)", anchor='w').grid(row=2, column=0, columnspan=2)
        entryEmail = tk.Entry(self, width=30)
        entryEmail.grid(row=2, column=2)
        tk.Label(self, width=20, text="First Name", anchor='w').grid(row=3, column=0, columnspan=2)
        entryFirstName = tk.Entry(self, width=30)
        entryFirstName.grid(row=3, column=2)
        tk.Label(self, width=20, text="Last Name", anchor='w').grid(row=4, column=0, columnspan=2)
        entryLastName = tk.Entry(self, width=30)
        entryLastName.grid(row=4, column=2)
        tk.Label(self, width=20, text="Source", anchor='w').grid(row=5, column=0, columnspan=2)
        entrySource = tk.Entry(self, width=30)
        entrySource.grid(row=5, column=2)
        tk.Label(self, width=20, text="Account Since", anchor='w').grid(row=6, column=0, columnspan=2)
        entryUserSince = tk.Entry(self, width=30)
        entryUserSince.grid(row=6, column=2)
        tk.Label(self, width=20, text="(YYYY-MM-DD hh:mm:ss)", anchor='w').grid(row=6, column=3)
        tk.Label(self, width=20, text="Eventbrite Contact List", anchor='w').grid(row=7, column=0, columnspan=2)
        entryContactList = tk.Entry(self, width=30)
        entryContactList.grid(row=7, column=2)
        tk.Label(self, width=20, text="Added Date", anchor='w').grid(row=8, column=0, columnspan=2)
        entryAddedDate = tk.Entry(self, width=30)
        entryAddedDate.grid(row=8, column=2)
        tk.Label(self, width=20, text="(YYYY-MM-DD hh:mm:ss)", anchor='w').grid(row=8, column=3)
        tk.Label(self, width=20, text="Removed Reason", anchor='w').grid(row=9, column=0, columnspan=2)
        entryRemovedReason = tk.Entry(self, width=30)
        entryRemovedReason.grid(row=9, column=2)
        tk.Label(self, width=20, text="Remove Date", anchor='w').grid(row=10, column=0, columnspan=2)
        entryRemovedDate = tk.Entry(self, width=30)
        entryRemovedDate.grid(row=10, column=2)
        tk.Label(self, width=20, text="(YYYY-MM-DD hh:mm:ss)", anchor='w').grid(row=10, column=3)
        tk.Label(self, width=20, text="Note", anchor='w').grid(row=11, column=0, columnspan=2)
        entryNote = tk.Entry(self, width=30)
        entryNote.grid(row=11, column=2)

        tk.Button(self, text="Submit", command=lambda: find()).grid(row=15, column=0, pady=5)
        tk.Button(self, text="Clear", command=lambda: clear()).grid(row=15, column=1, pady=5)

        def find():
            entries = [entryEmail.get(),entryFirstName.get(),entryLastName.get(),entrySource.get(),entryUserSince.get(),entryContactList.get(),entryAddedDate.get(),entryRemovedReason.get(),entryRemovedDate.get(),entryNote.get()]
            sql = "SELECT * FROM "+ workingDBTable +" WHERE"

            if len(entries) == entries.count(""): messagebox.showerror("Error","No search criteria selected.")
            else: pass

            i = 0
            whereClause = 0
            val = []
            while i<len(entries):
                if entries[i] =="":pass
                else:
                    whereClause += 1
                    if whereClause >= 2: sql = sql + " AND"
                    else: pass
                    sql = sql + " " + contactTableFields[i] + "=%s"
                    val.append(entries[i])
                i += 1
            sql = sql + " LIMIT 10"
            if controller.cursor == '':
                messagebox.showerror("Error", "Not connected to database.")
            else:
                controller.cursor.execute(sql, val)
                result = controller.cursor.fetchall()
                showResults(result)

        def clear():
            entryEmail.delete(0, tk.END)
            entryFirstName.delete(0, tk.END)
            entryLastName.delete(0, tk.END)
            entrySource.delete(0, tk.END)
            entryUserSince.delete(0, tk.END)
            entryContactList.delete(0, tk.END)
            entryAddedDate.delete(0, tk.END)
            entryRemovedReason.delete(0, tk.END)
            entryRemovedDate.delete(0, tk.END)
            entryNote.delete(0, tk.END)

        def showResults(results):
            tk.Label(self, text="Results", font=LARGE_FONT).grid(row=20, columnspan=4, padx=10)
            message = ""
            if results == []:
                tk.Label(self, text="0 matched records.").grid(row=21, columnspan=4, padx=10)
            else:
                tk.Label(self, text=str(len(results)) + " matched records.").grid(row=21, columnspan=4, padx=10)
                for record in results:
                    message += "\n" + str(record)

            textbox = tk.Text(self, height=5, width=70)
            scrollbar = tk.Scrollbar(self, command=textbox.yview)
            textbox.grid(row=25, columnspan=4)
            scrollbar.grid(row=25, column=4, sticky='ns')
            textbox.config(yscrollcommand=scrollbar.set)
            textbox.insert(tk.END, message)

class AddContactPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Add Contact", font=LARGE_FONT).grid(row=0, columnspan=4, pady=10, padx=10)

        tk.Label(self, width=20, text="E-mail (Username)", anchor='w').grid(row=2, column=0, columnspan=2)
        entryEmail = tk.Entry(self, width=30)
        entryEmail.grid(row=2, column=2)
        tk.Label(self, width=20, text="First Name", anchor='w').grid(row=3, column=0, columnspan=2)
        entryFirstName = tk.Entry(self, width=30)
        entryFirstName.grid(row=3, column=2)
        tk.Label(self, width=20, text="Last Name", anchor='w').grid(row=4, column=0, columnspan=2)
        entryLastName = tk.Entry(self, width=30)
        entryLastName.grid(row=4, column=2)
        tk.Label(self, width=20, text="Source", anchor='w').grid(row=5, column=0, columnspan=2)
        entrySource = tk.Entry(self, width=30)
        entrySource.grid(row=5, column=2)
        tk.Label(self, width=35, text="'uGRIDD User' if from User Management", anchor='w').grid(row=5, column=3)
        tk.Label(self, width=20, text="Account Since", anchor='w').grid(row=6, column=0, columnspan=2)
        entryUserSince = tk.Entry(self, width=30)
        entryUserSince.grid(row=6, column=2)
        tk.Label(self, width=35, text="(YYYY-MM-DD hh:mm:ss)", anchor='w').grid(row=6, column=3)
        tk.Label(self, width=20, text="Note", anchor='w').grid(row=7, column=0, columnspan=2)
        entryNote = tk.Entry(self, width=30)
        entryNote.grid(row=7, column=2)

        tk.Button(self, text="Submit", command=lambda: add()).grid(row=10, column=0, pady=5)
        tk.Button(self, text="Clear", command=lambda: clear()).grid(row=10, column=1, pady=5)

        def add():
            entries = {
                "email" : entryEmail.get(),
                "firstname" : entryFirstName.get(),
                "lastname" : entryLastName.get(),
                "source" : entrySource.get(),
                "usersince" : entryUserSince.get(),
                "note": entryNote.get()
            }
            invalidEntries = []

            sqlStatement = 'INSERT INTO ' + workingDBTable + ' (EmailAddress,FirstName,LastName,Source,UserSince,EventbriteContactList,AddedDate,RemovedReason,RemoveDate,Note) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

            for i in entries:
                if entries[i] =="": entries[i] = None
                else: pass

            #Require email entry
            if entries["email"] == None: messagebox.showerror("Error","Email is required.")
            else:
                #Check if the email is already in database
                emailFound = False

                sql = "SELECT COUNT(*) FROM "+ workingDBTable +" WHERE EmailAddress=%s"
                val= [entries["email"]]
                if controller.cursor == '':
                    messagebox.showerror("Error", "Not connected to database.")
                else:
                    controller.cursor.execute(sql,val)
                    result = controller.cursor.fetchall()
                    if result[0][0] > 0:
                        emailFound = True
                    else: pass

                    if emailFound:
                        messagebox.showerror("Error","Email found in table. Duplicate email addresses not allowed.")
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
                            #All checks OK, run SQL Statement
                            val = [(entries["email"], entries["firstname"], entries["lastname"], entries["source"], entries["usersince"], None,datetime.now().strftime("%Y-%m-%d %H:%M:%S"), None, None, entries["note"])]
                            controller.cursor.executemany(sqlStatement, val)
                            sql = "SELECT * FROM "+ workingDBTable +" WHERE EmailAddress=%s"
                            val = [entries["email"]]
                            controller.cursor.execute(sql,val)
                            result = controller.cursor.fetchall()

                            tk.Label(self, text="Entry added", font=LARGE_FONT).grid(row=20, columnspan=4, padx=10)
                            textbox = tk.Text(self, height=5, width=75)
                            scrollbar = tk.Scrollbar(self, command=textbox.yview)
                            textbox.grid(row=25, columnspan=4)
                            scrollbar.grid(row=25, column=4, sticky='ns')
                            textbox.config(yscrollcommand=scrollbar.set)
                            textbox.insert(tk.END, str(result))
                        else:
                            #Prompt for corrections
                            message = "INVALID ENTRIES:"
                            for i in invalidEntries:
                                message = message + "\n" + i
                            messagebox.showerror("Error",message)

        def clear():
            entryEmail.delete(0, tk.END)
            entryFirstName.delete(0, tk.END)
            entryLastName.delete(0, tk.END)
            entrySource.delete(0, tk.END)
            entryUserSince.delete(0, tk.END)
            entryNote.delete(0, tk.END)

class UpdateContactPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        tk.Label(self, text="Update Contact Page", font=LARGE_FONT).grid(row=0, columnspan=3, pady=5, padx=10)

        tk.Label(self, width=70, text="Please enter the email address of the record you want to update.\n"
                                      "You can use the Search Contacts under the Actions menu to find the record.", anchor='w').grid(row=3, columnspan=3, pady=5)
        tk.Label(self, width=20, text="E-mail (Username)", anchor='w').grid(row=6, column=0)
        mainEntryEmail = tk.Entry(self, width=30)
        mainEntryEmail.grid(row=6, column=1)

        tk.Button(self, text="Submit", command=lambda: check()).grid(row=10, pady=10)

        def check():
            email = mainEntryEmail.get()
            if email == "": messagebox.showerror("Error", "Email not entered.")
            else:
                sql = "SELECT COUNT(*) FROM " + workingDBTable + " WHERE EmailAddress=%s"
                val = [email]
                if controller.cursor == '':
                    messagebox.showerror("Error", "Not connected to database.")
                else:
                    controller.cursor.execute(sql,val)
                    result = controller.cursor.fetchall()
                    if result[0][0] == 1:
                        # Entry found
                        foundFields = []
                        for i in contactTableFields:
                            sql = "SELECT " + i + " FROM " + workingDBTable + " WHERE EmailAddress=%s"
                            controller.cursor.execute(sql, val)
                            result = controller.cursor.fetchall()
                            foundFields.append(result[0][0])
                        update(foundFields, email)
                    else:
                        messagebox.showerror("Error", "Email not found.")

        entryEmail = tk.Entry(self, width=30)
        entryFirstName = tk.Entry(self, width=30)
        entryLastName = tk.Entry(self, width=30)
        entrySource = tk.Entry(self, width=30)
        entryUserSince = tk.Entry(self, width=30)
        entryContactList = tk.Entry(self, width=30)
        entryAddedDate = tk.Entry(self, width=30)
        entryRemovedReason = tk.Entry(self, width=30)
        entryRemovedDate = tk.Entry(self, width=30)
        entryNote = tk.Entry(self, width=30)

        def update(fieldsArray, emailID):
            tk.Label(self, text="Entry Found", font=LARGE_FONT, anchor='w').grid(row=20, column=0, columnspan=3)
            tk.Label(self, width=70, text="Change the fields below to update the entry.",anchor='w').grid(row=22, columnspan=3, pady=5)

            tk.Label(self, width=20, text="E-mail (Username)", anchor='w').grid(row=30, column=0)
            entryEmail.grid(row=30, column=1)
            entryEmail.delete(0,tk.END)
            if fieldsArray[0] == None: pass
            else: entryEmail.insert(0, fieldsArray[0])
            tk.Label(self, width=20, text="First Name", anchor='w').grid(row=31, column=0)
            entryFirstName.grid(row=31, column=1)
            entryFirstName.delete(0, tk.END)
            if fieldsArray[1] == None: pass
            else: entryFirstName.insert(0, fieldsArray[1])
            tk.Label(self, width=20, text="Last Name", anchor='w').grid(row=32, column=0)
            entryLastName.grid(row=32, column=1)
            entryLastName.delete(0, tk.END)
            if fieldsArray[2] == None: pass
            else: entryLastName.insert(0, fieldsArray[2])
            tk.Label(self, width=20, text="Source", anchor='w').grid(row=33, column=0)
            entrySource.grid(row=33, column=1)
            entrySource.delete(0, tk.END)
            if fieldsArray[3] == None: pass
            else: entrySource.insert(0, fieldsArray[3])
            tk.Label(self, width=20, text="Account Since", anchor='w').grid(row=34, column=0)
            entryUserSince.grid(row=34, column=1)
            tk.Label(self, width=20, text="(YYYY-MM-DD hh:mm:ss)", anchor='w').grid(row=34, column=2)
            entryUserSince.delete(0, tk.END)
            if fieldsArray[4] == None: pass
            else: entryUserSince.insert(0, fieldsArray[4])
            tk.Label(self, width=20, text="Eventbrite Contact List", anchor='w').grid(row=35, column=0)
            entryContactList.grid(row=35, column=1)
            entryContactList.delete(0, tk.END)
            if fieldsArray[5] == None: pass
            else: entryContactList.insert(0, fieldsArray[5])
            tk.Label(self, width=20, text="Added Date", anchor='w').grid(row=36, column=0)
            entryAddedDate.grid(row=36, column=1)
            tk.Label(self, width=20, text="(YYYY-MM-DD hh:mm:ss)", anchor='w').grid(row=36, column=2)
            entryAddedDate.delete(0, tk.END)
            if fieldsArray[6] == None: pass
            else: entryAddedDate.insert(0, fieldsArray[6])
            tk.Label(self, width=20, text="Removed Reason", anchor='w').grid(row=37, column=0)
            entryRemovedReason.grid(row=37, column=1)
            entryRemovedReason.delete(0, tk.END)
            if fieldsArray[7] == None: pass
            else: entryRemovedReason.insert(0, fieldsArray[7])
            tk.Label(self, width=20, text="Remove Date", anchor='w').grid(row=38, column=0)
            entryRemovedDate.grid(row=38, column=1)
            tk.Label(self, width=20, text="(YYYY-MM-DD hh:mm:ss)", anchor='w').grid(row=38, column=2)
            entryRemovedDate.delete(0, tk.END)
            if fieldsArray[8] == None: pass
            else: entryRemovedDate.insert(0, fieldsArray[8])
            tk.Label(self, width=20, text="Note", anchor='w').grid(row=39, column=0)
            entryNote.grid(row=39, column=1)
            entryNote.delete(0, tk.END)
            if fieldsArray[9] == None: pass
            else: entryNote.insert(0, fieldsArray[9])

            tk.Button(self, text="Update", command=lambda: doUpdate(fieldsArray, emailID)).grid(row=45)

        def doUpdate(origEntries, emailID):
            updateEntries = [entryEmail.get(), entryFirstName.get(), entryLastName.get(), entrySource.get(),
                       entryUserSince.get(), entryContactList.get(), entryAddedDate.get(), entryRemovedReason.get(),
                       entryRemovedDate.get(), entryNote.get()]

            if updateEntries[0] == "": messagebox.showerror("Error", "Email is required.")
            else:
                invalidEntries = []
                # Check for correct email format
                if re.match(r"[^@]+@[^@]+\.[^@]+", updateEntries[0]): pass
                else: invalidEntries.append("Invalid email format")

                # Check for correct date format
                if updateEntries[4] == "": pass
                else:
                    try: datetime.strptime(updateEntries[4], '%Y-%m-%d %H:%M:%S')
                    except ValueError: invalidEntries.append("Invalid date format (Account Since)")
                    else: pass

                if updateEntries[6] == "": pass
                else:
                    try: datetime.strptime(updateEntries[6], '%Y-%m-%d %H:%M:%S')
                    except ValueError: invalidEntries.append("Invalid date format (Added Date)")
                    else: pass

                if updateEntries[8] == "": pass
                else:
                    try: datetime.strptime(updateEntries[8], '%Y-%m-%d %H:%M:%S')
                    except ValueError: invalidEntries.append("Invalid date format (Removed Date)")
                    else: pass

                if len(invalidEntries) == 0:
                    sql = "UPDATE " + workingDBTable + " SET"
                    val = []
                    updateCount = 0
                    i = 0
                    while i < len(origEntries):
                        if updateEntries[i] == "": updateEntries[i]=None
                        else:pass
                        if str(origEntries[i]) == str(updateEntries[i]): pass
                        else:
                            updateCount += 1
                            if updateCount >= 2: sql = sql + ","
                            else: pass
                            # column1 = value1, column2 = value 2, ...
                            sql = sql + " " + contactTableFields[i] + "=%s"
                            # ** column == contactTableFields[]
                            val.append(updateEntries[i])
                            # ** value == updateEntries[]
                        i += 1
                    if updateCount == 0: messagebox.showinfo("Message", "No changes were made to the entry.\nNo update to be made.")
                    else:
                        # WHERE condition
                        # ** condition == 'EmailAddress = %s'
                        sql = sql + " WHERE EmailAddress='" + emailID + "'"
                        controller.cursor.execute(sql, val)
                        sql1 = "SELECT * FROM " + workingDBTable + " WHERE EmailAddress=%s"
                        val1 = [updateEntries[0]]
                        controller.cursor.execute(sql1, val1)
                        result = controller.cursor.fetchall()

                        tk.Label(self, text="Entry updated", font=LARGE_FONT).grid(row=50, columnspan=3, padx=10)
                        textbox = tk.Text(self, height=5, width=70)
                        scrollbar = tk.Scrollbar(self, command=textbox.yview)
                        textbox.grid(row=55, columnspan=3)
                        scrollbar.grid(row=55, column=3, sticky='ns')
                        textbox.config(yscrollcommand=scrollbar.set)
                        textbox.insert(tk.END, str(result))
                else:
                    # Prompt for corrections
                    message = "INVALID ENTRIES:"
                    for i in invalidEntries:
                        message = message + "\n" + i
                    messagebox.showerror("Error", message)

class RemoveContactPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        tk.Label(self, text="Remove Contact Page", font=LARGE_FONT).grid(row=0, columnspan=3, pady=5, padx=10)

        tk.Label(self, width=70, text="Please enter the email address of the record you want to remove.\n"
                                      "You can use the Search Contacts under the Actions menu to find the record.", anchor='w').grid(row=3, columnspan=3, pady=5)
        tk.Label(self, width=20, text="E-mail (Username)", anchor='w').grid(row=6, column=0)
        mainEntryEmail = tk.Entry(self, width=30)
        mainEntryEmail.grid(row=6, column=1)

        tk.Button(self, text="Submit", command=lambda: check()).grid(row=10, pady=10)

        def check():
            email = mainEntryEmail.get()
            if email == "": messagebox.showerror("Error", "Email not entered.")
            else:
                sql = "SELECT * FROM " + workingDBTable + " WHERE EmailAddress=%s"
                val = [email]
                if controller.cursor == '':
                    messagebox.showerror("Error", "Not connected to database.")
                else:
                    controller.cursor.execute(sql,val)
                    result = controller.cursor.fetchall()
                    if result == []:
                        #Entry not found
                        messagebox.showerror("Error", "Email not found.")
                    else:
                        # Entry found
                        # Check if removed already
                        if result[0][7] == None:
                            getReason(result[0])
                        else:
                            messagebox.showerror("Error", "This email corresponds to an entry which has RemovedReason and RemovedDate fields.\nIf you need to edit those fields, use Update Contact under the Actions menu.")

        entryRemovedReason = tk.Entry(self, width=50)

        def getReason(entry):
            tk.Label(self, text="Entry Found", font=LARGE_FONT, anchor='w').grid(row=20, column=0, columnspan=3)

            textbox = tk.Text(self, height=5, width=70)
            textbox.grid(row=21, columnspan=3)
            textbox.insert(tk.END, str(entry))

            tk.Label(self, width=20, text="Give reason for removal:", anchor='w').grid(row=30, column=0, pady=10)
            entryRemovedReason.grid(row=30, column=1, pady=10)
            tk.Button(self, text="Remove", command=lambda: removeEntry(entry)).grid(row=35)

        def removeEntry(entry):
            removedReason = entryRemovedReason.get()
            if removedReason == "": messagebox.showerror("Error","Reason is required.")
            else:
                if messagebox.askyesno("Confirm", "Are you sure you want to remove this entry?"):
                    sql = "UPDATE " + workingDBTable + " SET " + contactTableFields[7] + "=%s, " + contactTableFields[8] + "=%s WHERE EmailAddress='" + entry[0] + "'"
                    val = [removedReason, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                    controller.cursor.execute(sql, val)
                    sql1 = "SELECT * FROM " + workingDBTable + " WHERE EmailAddress=%s"
                    val1 = [entry[0]]
                    controller.cursor.execute(sql1, val1)
                    result = controller.cursor.fetchall()

                    tk.Label(self, text="Entry marked 'removed'", font=LARGE_FONT).grid(row=50, columnspan=3, padx=10)
                    textbox = tk.Text(self, height=5, width=70)
                    scrollbar = tk.Scrollbar(self, command=textbox.yview)
                    textbox.grid(row=55, columnspan=3)
                    scrollbar.grid(row=55, column=3, sticky='ns')
                    textbox.config(yscrollcommand=scrollbar.set)
                    textbox.insert(tk.END, str(result))
                else: pass


app = ContactsApp()
app.geometry("650x600")
app.mainloop()
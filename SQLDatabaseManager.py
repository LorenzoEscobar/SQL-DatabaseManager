import os
from tkinter import *
from tkinter.tix import Tree
from tkinter.ttk import Treeview
import pyodbc
import pandas as pd
dir_path = os.path.dirname(os.path.realpath(__file__)) #gets path of file location

## DATABASE MANAGEMENT
database = 'master'    ##forcing database to master, for now.
gui = Tk()
gui.title('SQL DATABASE MANAGER')
gui.geometry("500x525")
gui.resizable(width=False, height=False)
# create background design using picture.
bg = PhotoImage(file = dir_path+r"\assets\bg.png")  
bgcanvas = Canvas(gui,width=500,height=525)
bgcanvas.pack(fill="both",expand =True)
bgcanvas.create_image(0,0,image=bg,anchor="nw")




def destroyDeleteDB():          ##Deletes the DeleteDB Menu
    deleteDBlabel.destroy()
    deleteDBentry.destroy()
    returnmenu4.destroy()
    deleteDBname.destroy()

def destroyUpdateDB():
    updateDBlabel.destroy()
    updateDBentry.destroy()
    updateDBlabel2.destroy()
    newDBentry.destroy()
    updateDBname.destroy()
    returnmenu3.destroy()
    
def destroyCreateDB():          ##Deletes the CreateDB Menu
    createDBlabel.destroy()
    createDBentry.destroy()
    returnmenu2.destroy()
    submitDBname.destroy()
    
def destoryCheckDB():           ##Deletes CheckDB Menu
    checkDBlabel.destroy()
    returnmenu.destroy()
    chkDB.destroy()

def destroyConnMenu():          ##Deletes the Connection menu, first page
    bgcanvas.destroy()
    serverlabel.destroy()
    userlabel.destroy()
    infolabel.destroy()
    passlabel.destroy()
    serverentry.destroy()
    userentry.destroy()
    passentry.destroy()
    serversubmit.destroy()

def destroycrudMenu():          ##Deletes CRUD menu
    b.destroy()
    b2.destroy()
    b3.destroy()
    b4.destroy()
##
##
def CheckDB():                  ##READ
    print("Checked Database")   #DEBUG
    destroycrudMenu()
    #get databases from master
    query = "SELECT name FROM master.dbo.sysdatabases"
    df = pd.read_sql(query, conn)           
    
    global checkDBlabel
    checkDBlabel = Label (gui,text = "Databases on '"+database+ "'",font=("Ebrima", 20))
    checkDBlabel.place(x=110,y=50)
    # creates a treeview, gets rows from dataframe with loop and inserts into treeview.
    global chkDB
    chkDB = Treeview(gui, columns=(1), show="headings")
    chkDB["column"] = list(df.columns)
    for column in chkDB["column"]:
        chkDB.heading(column,text=column)
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        chkDB.insert("","end",values=row)
    chkDB.place(x=125,y=100)
    
    global returnmenu 
    returnmenu = Button(gui, text="Return",font='Ebrima', command=lambda:[crudDB(),destoryCheckDB()])   #lambda in command allows for multiple function use.
    returnmenu.place(x=425,y=450)
   
def CreateDBMenu():             ##CREATE
    print("Create Database")    #DEBUG
    destroycrudMenu()
    global createDBlabel
    createDBlabel = Label(gui, text= "Enter name for database you would like to create: ",font='Ebrima')
    createDBlabel.place(x=30,y=95)
    global createDBentry
    createDBentry = Entry(gui, width =35)
    createDBentry.place(x=120,y=125)
    
    
    global submitDBname
    submitDBname = Button(gui, text="Enter",font='Ebrima', command=lambda:[CreateDB()])  
    submitDBname.place(x=325,y=175)
    global returnmenu2
    returnmenu2 = Button(gui, text="Return",font='Ebrima', command=lambda:[crudDB(),destroyCreateDB()])   
    returnmenu2.place(x=425,y=450)
    
def CreateDB():                 ##creates a database with name from entry
    DBname = createDBentry.get()                ##get name from entry from
    query = "CREATE DATABASE "+DBname+";";      ##create query using name from entry form
    pd.read_sql(query, conn)                    ##query to sql server
    createNotif = Label(gui,text= DBname+ " Database created! ")              ##
    createNotif.pack()
    print("Created "+createDBentry+ "Database")  

def UpdateDBMenu():             ##UPDATE
    print("Update Database")    #DEBUG
    global updateDBlabel
    updateDBlabel = Label(gui, text= "Enter name for database you would like to update: ",font='Ebrima')
    updateDBlabel.place(x=30,y=95)
    global updateDBentry
    updateDBentry = Entry(gui, width =35)
    updateDBentry.place(x=120,y=125)
    
    global updateDBlabel2
    updateDBlabel2 = Label(gui, text= "Enter new name for database: ",font='Ebrima')
    updateDBlabel2.place(x=30,y=195)
    global newDBentry
    newDBentry = Entry(gui, width =35)
    newDBentry.place(x=120,y=225)
    
    
    global updateDBname
    updateDBname = Button(gui, text="Enter",font='Ebrima', command=lambda:[UpdateDB()])  
    updateDBname.place(x=325,y=285)
    global returnmenu3
    returnmenu3 = Button(gui, text="Return",font='Ebrima', command=lambda:[crudDB(),destroyUpdateDB()])   
    returnmenu3.place(x=425,y=450)
    destroycrudMenu()

def UpdateDB():
    DBname = updateDBentry.get()                ##get name from entry from
    newDBname = newDBentry.get()
    query = "ALTER DATABASE "+"["+DBname+"]"+" MODIFY NAME = "+"["+newDBname+"]"     ##create query using name from entry form
    pd.read_sql(query, conn)               ##query to sql server
    print("Updated "+updateDBentry+ "Database with new name as " +newDBname)  
    
def DeleteDBMenu():             ##DELETE
    print("Delete Database")    #DEBUG
    destroycrudMenu()   
    global deleteDBlabel
    deleteDBlabel = Label(gui, text= "Enter name for database you would like to delete: ",font='Ebrima')
    deleteDBlabel.place(x=30,y=95)
    global deleteDBentry
    deleteDBentry = Entry(gui, width =35)
    deleteDBentry.place(x=120,y=125)
    
    
    global deleteDBname
    deleteDBname = Button(gui, text="Enter",font='Ebrima', command=lambda:[DeleteDB()])  
    deleteDBname.place(x=325,y=175)
    global returnmenu4
    returnmenu4 = Button(gui, text="Return",font='Ebrima', command=lambda:[crudDB(),destroyDeleteDB()])   
    returnmenu4.place(x=425,y=450)
    
def DeleteDB():                 ##deletes a database with name from entry
    DelDBname = deleteDBentry.get()  
    query = "DROP DATABASE "+DelDBname+";";      ##delete query from entry 
    pd.read_sql(query, conn)    
    print("Deleted"+deleteDBname+ "Database")     ##DEBUG
    
def dbCONN():                   ##Gets connection info from entry form and connects to sql server
    crudDB()
    server = serverentry.get()
    username = userentry.get()
    password = passentry.get()
    print(server)                   #DEBUG
    print(database)                 #DEBUG
    print(username)                 #DEBUG
    print(password)                 #DEBUG
    destroyConnMenu()
    global conn
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password,autocommit=True)  #connecting to sql server with pyodbc   
    query = "SELECT name FROM master.dbo.sysdatabases"
    df = pd.read_sql(query, conn)   #DEBUG
    print(df.head())                #DEBUG
   
def crudDB():                   ##Creates MENU to navigate CRUD options, uses pictures as buttons
    global b1photo,b2photo,b3photo,b4photo
    global b,b2,b3,b4
    b1photo = PhotoImage(file = dir_path+r"\assets\check.png")
    b = Button(gui, text="Check Databases", command=CheckDB, image = b1photo)
    b.pack()

    b2photo = PhotoImage(file = dir_path+r"\assets\create.png")
    b2 = Button(gui, text="Create Database", command=CreateDBMenu, image = b2photo)
    b2.pack()

    b3photo = PhotoImage(file = dir_path+r"\assets\update.png")
    b3= Button(gui, text="Update Database", command=UpdateDBMenu, image = b3photo)
    b3.pack()

    b4photo = PhotoImage(file = dir_path+r"\assets\delete.png")
    b4= Button(gui, text="Delete Database", command=DeleteDBMenu, image = b4photo)
    b4.pack()    

#Buttons and Labels, for ServerConnection form.
infolabel = Label (gui,text = "Connect to SQL Server!",font=("Ebrima", 25))
infolabel.place(x=85,y=50)

serverlabel = Label(gui, text= "Server: ",font='Ebrima')
serverlabel.place(x=30,y=120)
serverentry = Entry(gui, width =35)
serverentry.place(x=120,y=125)

userlabel = Label(gui, text= "Username: ",font='Ebrima')
userlabel.place(x=30,y=170)
userentry = Entry(gui, width =40)
userentry.place(x=120,y=175)

passlabel = Label(gui, text= "Password: ",font='Ebrima')
passlabel.place(x=30,y=220)
passentry = Entry(gui, width =40)
passentry.place(x=120,y=225)

serversubmit = Button(gui, text="Enter",font='Ebrima', command=dbCONN)
serversubmit.place(x=215,y=350)


gui.mainloop()

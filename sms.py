from datetime import time
from tkinter import *

import pandas as pandas
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql

def iexit():
    result=messagebox.showinfo('confirm','do you want to exit?')
    if result:
        root.destroy()
    else:
        pass

def export_data(newlist=None, pandas=None):
    url=filedialog.asksaveasfilename(defaultextensions='.csv')
    indexing=studentTable.get_children()
    for index in indexing:
        content=studentTable.item(index)
        datalist=content['values']
        newlist.append(datalist)

    table=pandas.DataFrame(newlist,columns=['id','name','phone','address','gender','dob'])
    table.to_csv(url, index=False)
    messagebox.showinfo('success','data saved')

def update_student():
    def update_data():
        query = 'update student set name=%s, phone=%s, email=%s, address=%s, gender=%s, dob=%s where id=%s'
        mycursor.execute(query, (
        idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(),
        dobEntry.get()))
        con.commit()
        messagebox.showinfo('success',f'id {idEntry.get()} is modified successfully',parent=update_window)
        update_window.destroy()
        show_student()

    update_window = Toplevel()
    update_window.title('update student')
    update_window.grab_set()
    update_window.resizable(False, False)

    idLabel = Label(update_window, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, pady=15, padx=10)
    idEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(update_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, pady=15, padx=10)
    nameEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(update_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, pady=15, padx=10)
    phoneEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(update_window, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, pady=15, padx=10)
    emailEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(update_window, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, pady=15, padx=10)
    addressEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(update_window, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, pady=15, padx=10)
    genderEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(update_window, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, pady=15, padx=10)
    dobEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    update_student_button = ttk.Button(update_window, text='update',command=update_data)
    update_student_button.grid(row=7, column=1, columnspan=2, pady=15)

    indexing=studentTable.focus()
    content=studentTable.item(indexing)
    listdata=content['values']
    idEntry.insert(0,listdata[0])
    nameEntry.insert(0, listdata[1])
    phoneEntry.insert(0, listdata[2])
    emailEntry.insert(0, listdata[3])
    addressEntry.insert(0, listdata[4])
    genderEntry.insert(0, listdata[5])
    dobEntry.insert(0, listdata[6])







def show_student():
    global mycursor, con
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def delete_student():
    indexing = studentTable.focus()
    print(indexing)
    content = studentTable.item(indexing)

    # Check if 'values' key exists and is not empty
    if 'values' in content and content['values']:
        content_id = content['values'][0]
        query = 'delete from student where id = %s'  # Corrected SQL query
        mycursor.execute(query, (content_id,))
        con.commit()
        messagebox.showinfo('deleted', f'ID {content_id} is deleted successfully')

        # Fetch updated data and display in the table
        query = 'select * from student'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('', END, values=data)
    else:
        messagebox.showerror('Error', 'No student selected for deletion')

def search_student():
    def search_data():
        global mycursor,con
        query = 'select * from student where id=%s or name=%s or phone=%s or  email=%s or address=%s or gender=%s or dob=%s'
        mycursor.execute(query,(idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get() ))
        studentTable.delete(*studentTable.get_children())
        fetched_data=mycursor.fetchall()
        for data in fetched_data:
            studentTable.insert('', END, values=data)

    search_window = Toplevel()
    search_window.title('search student')
    search_window.grab_set()
    search_window.resizable(False, False)

    idLabel = Label(search_window, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, pady=15, padx=10)
    idEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(search_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, pady=15, padx=10)
    nameEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(search_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, pady=15, padx=10)
    phoneEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(search_window, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, pady=15, padx=10)
    emailEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(search_window, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, pady=15, padx=10)
    addressEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(search_window, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, pady=15, padx=10)
    genderEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(search_window, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, pady=15, padx=10)
    dobEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    search_student_button = ttk.Button(search_window, text='search', command=search_data)
    search_student_button.grid(row=7, column=1, columnspan=2, pady=15)

def add_student():
    def add_data():
        if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
            messagebox.showerror('Error', 'All fields are required', parent=add_window)
        else:
            try:
                query = 'INSERT INTO student (id, name, mobile, email, address, gender, dob) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                mycursor.execute(query, (
                idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
                genderEntry.get(), dobEntry.get()))
                con.commit()
                result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clear the form?',
                                             parent=add_window)
                if result:
                    idEntry.delete(0, END)
                    nameEntry.delete(0, END)
                    phoneEntry.delete(0, END)
                    emailEntry.delete(0, END)
                    addressEntry.delete(0, END)
                    genderEntry.delete(0, END)
                    dobEntry.delete(0, END)
                else:
                    pass
            except:
                messagebox.showerror('error','id cannot be repeated',parent=add_window)
                return

            query = 'select * from student'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            studentTable.delete(*studentTable.get_children())
            for data in fetched_data:
                studentTable.insert('', END, values=data)


    add_window = Toplevel()
    add_window.grab_set()
    add_window.resizable(False, False)

    idLabel = Label(add_window, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, pady=15, padx=10)
    idEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(add_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, pady=15, padx=10)
    nameEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(add_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, pady=15, padx=10)
    phoneEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(add_window, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, pady=15, padx=10)
    emailEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(add_window, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, pady=15, padx=10)
    addressEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(add_window, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, pady=15, padx=10)
    genderEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(add_window, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, pady=15, padx=10)
    dobEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    add_student_button = ttk.Button(add_window, text='Add', command=add_data)
    add_student_button.grid(row=7, column=1, columnspan=2, pady=15)


def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host='localhost', user='root', password='root')
            mycursor = con.cursor()
            messagebox.showinfo('Success', 'Database connection is successful', parent=connectWindow)
        except Exception as e:
            messagebox.showerror('Error', f'Invalid details: {e}', parent=connectWindow)
            return

        def delete_student():
            indexing = studentTable.focus()
            print(indexing)
            content = studentTable.item(indexing)

            # Check if 'values' key exists and is not empty
            if 'values' in content and content['values']:
                content_id = content['values'][0]
                query = 'delete from student where id = %s'  # Corrected SQL query
                mycursor.execute(query, (content_id,))
                con.commit()
                messagebox.showinfo('deleted', f'ID {content_id} is deleted successfully')

                # Fetch updated data and display in the table
                query = 'select * from student'
                mycursor.execute(query)
                fetched_data = mycursor.fetchall()
                studentTable.delete(*studentTable.get_children())
                for data in fetched_data:
                    studentTable.insert('', END, values=data)
            else:
                messagebox.showerror('Error', 'No student selected for deletion')

        try:
            query = 'CREATE DATABASE IF NOT EXISTS student_system'
            mycursor.execute(query)
            query = 'USE student_system'
            mycursor.execute(query)
            query = '''CREATE TABLE IF NOT EXISTS student(
                        id INT NOT NULL PRIMARY KEY,
                        name VARCHAR(50),
                        mobile VARCHAR(10),
                        email VARCHAR(30),
                        address VARCHAR(50),
                        gender VARCHAR(20),
                        dob VARCHAR(20),
                        date VARCHAR(50),
                        time VARCHAR(50)
                    )'''
            mycursor.execute(query)
        except Exception as e:
            messagebox.showerror('Error', f'Error creating database or table: {e}', parent=connectWindow)

        connectWindow.destroy()
        addStudentButton.config(state=NORMAL)
        searchStudentButton.config(state=NORMAL)
        updateStudentButton.config(state=NORMAL)
        showStudentButton.config(state=NORMAL)
        exportStudentButton.config(state=NORMAL)
        deleteStudentButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0, 0)

    hostnameLabel = Label(connectWindow, text='Host name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0)

    hostEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectWindow, text='User name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton = Button(connectWindow, text='Connect', command=connect)
    connectButton.grid(row=3, column=0)

# GUI
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x680+0+0')
root.resizable(0, 0)
root.title('Student Management System')

connectButton = ttk.Button(root, text='Connect Database', command=connect_database)
connectButton.place(x=980, y=0)

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file='C:/Users/gauri/PycharmProjects/Student management system/student.png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0)

addStudentButton=ttk.Button(leftFrame,text='Add student',width=25,command=add_student)
addStudentButton.grid(row=1,column=0,pady=20)

searchStudentButton=ttk.Button(leftFrame,text='Search student',width=25,command=search_student)
searchStudentButton.grid(row=2,column=0,pady=20)

deleteStudentButton=ttk.Button(leftFrame,text='Delete student',width=25,command=delete_student)
deleteStudentButton.grid(row=3,column=0,pady=20)

updateStudentButton=ttk.Button(leftFrame,text='Update student',width=25,command=update_student)
updateStudentButton.grid(row=4,column=0,pady=20)

showStudentButton=ttk.Button(leftFrame,text='Show student',width=25,command=show_student)
showStudentButton.grid(row=5,column=0,pady=20)

exportStudentButton=ttk.Button(leftFrame,text='Export student',width=25,command=export_data)
exportStudentButton.grid(row=6,column=0,pady=20)

exitStudentButton=ttk.Button(leftFrame,text='Exit student',width=25,command= iexit)
exitStudentButton.grid(row=7,column=0,pady=20)


rightFrame=Frame(root)
rightFrame.place(x=350,y=80,width=820,height=600)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

studentTable=ttk.Treeview(rightFrame,columns=('ID','Name','Mobile no','Email','Address','Gender',
                                              'D.O.B','Added date','Added time'),
                                               xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

studentTable.pack(fill=BOTH,expand=1)

studentTable.heading('ID', text='ID')
studentTable.heading('Name', text='Name')
studentTable.heading('Mobile no', text='Mobile no')
studentTable.heading('Email', text='email')
studentTable.heading('Address', text='address')
studentTable.heading('Gender', text='gender')
studentTable.heading('D.O.B', text='D.O.B')
studentTable.heading('Added date', text='added date')
studentTable.heading('Added time', text='added time')

style=ttk.Style()
style.configure('Treeview',rowheight=40,font=('arial',15,'bold'),foreground='red4')


studentTable.config(show='headings')

root.mainloop()



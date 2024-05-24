import tkinter as tk
from tkinter import ttk
from tkinter import *
import datetime as dt
import mysql.connector
from tkinter import messagebox

# Global Valriables
count = 0
selected_rowid = 0

# Establish mysql connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="personalfinancemanager"
)

mycursor = mydb.cursor()

def insert_record():
    try:
        sql = "INSERT INTO expense_record (expenses, description, date) VALUES (%s, %s, %s)"
        val = (expense.get(), description.get(), dt.datetime.strptime(transaction_date.get(), '%d %B %Y'))
        mycursor.execute(sql, val)
        mydb.commit()

        # clear entry boxes
        expense.delete(0, END)
        description.delete(0, END)
        transaction_date.delete(0, END)
        tree_view.after(400, refreshData)

    except Exception as e:
        messagebox.showerror("Error", e)


def fetch_records():
    mycursor.execute("SELECT * FROM expense_record ORDER BY date")
    myresult = mycursor.fetchall()

    global count
    for results in myresult:
        date =dt.datetime.strptime(str(results[3]), "%Y-%m-%d").strftime("%d %B %Y")
        tree_view.insert(parent='', index=0, iid=count,  values=(results[0], date, results[2], results[1]))
        count += 1
    tree_view.after(400, refreshData)



def select_record(event):
    global selected_rowid
    selected =tree_view.focus()
    val = tree_view.item(selected, 'values')

    try:
        selected_rowid = val[0]
        d = val[1]
        amtvar.set(val[3])
        namevar.set(val[2])
        dopvar.set(str(d))
        
    except:
        pass


def update_record():
    global selected_rowid

    selected = tree_view.focus()

    #update reccord
    try:
        sql = "UPDATE expense_record SET expenses = %s, description = %s, date = %s WHERE id  = %s"
        values=(amtvar.get(), namevar.get(), dt.datetime.strptime(dopvar.get(), '%d %B %Y'), selected_rowid)
        mycursor.execute(sql, values)
        mydb.commit()
        tree_view.item(selected, text='', values=(amtvar.get(), namevar.get(), dopvar.get()))

    except:
        messagebox.showerror('Error','Enter date in DD MONTH YYYY format')
        


    # clear entry boxes
    expense.delete(0, END)
    description.delete(0, END)
    transaction_date.delete(0, END)
    tree_view.after(400, refreshData)

    

def refreshData():
    for item in tree_view.get_children():
        tree_view.delete(item)
    fetch_records()



def delete_record():
    sql = "DELETE FROM expense_record WHERE id = %s"
    adr = (selected_rowid,)
    mycursor.execute(sql, adr)
    mydb.commit()

    # clear entry boxes
    expense.delete(0, END)
    description.delete(0, END)
    transaction_date.delete(0, END)
    tree_view.after(400, refreshData)


def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')


def clearEntries():
    expense.delete(0, 'end')
    description.delete(0, 'end')
    transaction_date.delete(0, 'end')

def totalBalance():
    balance = 0
    salary = 0
    total_expence = 0
    try:
        sql = "SELECT SUM(expenses) FROM expense_record WHERE description = 'salary'"
        mycursor.execute(sql)
        salary = mycursor.fetchall()

        sql = "SELECT SUM(expenses) FROM expense_record WHERE description != 'salary'"
        mycursor.execute(sql)
        total_expence = mycursor.fetchall()

        balance = salary[0][0] - total_expence[0][0]

        return messagebox.showinfo('Summary ',f'Salary: {salary[0][0]}\nExpenses: {total_expence[0][0]}\nBalance {balance}')
    except:
        messagebox.showwarning('Warning','Add Salary')

# setting canvas
canvas = tk.Tk()
canvas.geometry("700x400")  # 400, 700
canvas.title("Personal Finance Manager")

f = ('Times new roman', 12)
namevar = tk.StringVar()
amtvar = tk.IntVar()
dopvar = tk.StringVar()

# Frame widget
f2 = Frame(canvas)
f2.pack()

f1 = Frame(canvas, padx=10, pady=10)
f1.pack(expand=True, fill=BOTH)

# Label widget
Label(f1, text='Expense Amount :', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='Description :', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='Transaction Date :', font=f).grid(row=2, column=0, sticky=W)

# Entry Widget
expense = Entry(f1, font=f, textvariable=amtvar)
description = Entry(f1, font=f, textvariable=namevar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)
salary = Entry(f1, font=f, textvariable=amtvar)

# Entry grit placement
expense.grid(row=0, column=1, sticky=EW, padx=(10, 0))
description.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))

# Action Buttons
curr_button = Button(
    f1,
    text='Current Date',
    font=f,
    bg='#04c4d9',
    command=setDate,
    width=15
)

submit_btn = Button(
    f1,
    text='Save Record',
    font=f,
    bg='#42602D',
    fg='white',
    command=insert_record,
)

clear_btn = Button(
    f1,
    text='Reset Entry',
    font=f,
    bg='#D9B036',
    command=clearEntries,
)

quit_btn = Button(
    f1,
    text='Exit',
    font=f,
    bg='#D33532',
    command=lambda: canvas.destroy(),
)

total_balance = Button(
    f1,
    text='Check Balance',
    font=f,
    bg='#009900',
    command=totalBalance,
)


update_btn = Button(
    f1,
    text='Update',
    font=f,
    bg='#D9B056',
    command=update_record,
)

del_btn = Button(
    f1,
    text='Delete',
    font=f,
    bg='#BD2A2E',
    command=delete_record,
)

# Grid placement for buttons
curr_button.grid(row=2, column=2, sticky=EW, padx=(10,0))
submit_btn.grid(row=3, column=1, sticky=EW, padx=(10,0))
clear_btn.grid(row=0, column=2, sticky=EW, padx=(10,0))
update_btn.grid(row=1, column=2, sticky=EW, padx=(10,0))
quit_btn.grid(row=2, column=3, sticky=EW, padx=(10,0))
total_balance.grid(row=0, column=3, sticky=EW, padx=(10,0))
del_btn.grid(row=1, column=3, sticky=EW, padx=(10,0))

# Tree view
tree_view = ttk.Treeview(f2, columns=(1, 2, 3, 4), show='headings', height=8)
tree_view.pack(side='left')

# Adding Heading to tree view
tree_view.column(1, width=1, anchor=CENTER, stretch=NO)
tree_view.heading(1, text='')

tree_view.column(2, anchor=CENTER, stretch=NO)
tree_view.heading(2, text='Transaction Date')

tree_view.column(3, anchor=CENTER, stretch=NO)
tree_view.heading(3, text='Description')

tree_view.column(4, anchor=CENTER, stretch=NO)
tree_view.heading(4, text='Expense Amount.')

# tree_view.column(4,anchor=CENTER, stretch=NO)
# tree_view.heading(4, text='Balance')

# binding tree view
tree_view.bind('<ButtonRelease-1>', select_record)  # add select_record

# style for treeview
style= ttk.Style()
style.theme_use('default')
style.map('TreeView')

# Vertical Scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tree_view.yview)
scrollbar.pack(side='right', fill='y')
tree_view.config(yscrollcommand=scrollbar.set)

# Calling Functions:
fetch_records()

# Infinite loop
canvas.mainloop()

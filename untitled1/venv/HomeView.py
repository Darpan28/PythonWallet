import mysql.connector
from tkinter import *
import datetime as dt

phone = ""
transferPhone = ""

def dateTime():
    global today
    today = dt.datetime.today()

class customer:
    def __init__(self,name,phone,balance):
        self.name = name
        self.phone = phone
        self.balance = balance

class dbHelper():
    def saveCustomerInDB(self,cust1):
        sql = "insert into wallets values('{}','{}','{}')".format(cust1.name,cust1.phone,cust1.balance)
        con = mysql.connector.connect(user = "root",password ="",host = "localhost",database = "banking")
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()

    def saveCustomerInTransAdd(self,phone,amountEntered,today):
        sql1 = "insert into transaction values('{}','{}','Deposite','{}')".format(phone,amountEntered,today)
        con1 = mysql.connector.connect(user = "root",password ="",host = "localhost",database = "banking")
        cursor1 = con1.cursor()
        cursor1.execute(sql1)
        con1.commit()

    def saveCustomerInTransWithdraw(self,phone,amountEntered,today):
        sql1 = "insert into transaction values('{}','{}','Withdraw','{}')".format(phone,amountEntered,today)
        con1 = mysql.connector.connect(user = "root",password ="",host = "localhost",database = "banking")
        cursor1 = con1.cursor()
        cursor1.execute(sql1)
        con1.commit()

    def saveCustomerInTransTransfer(self,phone,amountEntered,transferPhone,today):
        sql1 = "insert into transaction values('{}','{}','transfer to''{}','{}')".format(phone,amountEntered,transferPhone,today)
        con1 = mysql.connector.connect(user = "root",password ="",host = "localhost",database = "banking")
        cursor1 = con1.cursor()
        cursor1.execute(sql1)
        con1.commit()

    def updateCustomerInDB(self,balance,phone):
        sql = "update wallets set balance = '{}' where phone = '{}'".format(balance,phone)
        con = mysql.connector.connect(user="root", password="", host="localhost", database="banking")
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()

def fetchAccount(phone):
    sql = "select * from wallets where phone = '{}'".format(phone)
    con = mysql.connector.connect(user="root", password="", host="localhost", database="banking")
    cursor = con.cursor()
    cursor.execute(sql)
    global row
    row = cursor.fetchone()

def fetchAccountTransfer(transferPhone):
    sql = "select * from wallets where phone = '{}'".format(transferPhone)
    con = mysql.connector.connect(user="root", password="", host="localhost", database="banking")
    cursor = con.cursor()
    cursor.execute(sql)
    global transferRow
    transferRow = cursor.fetchone()

def addCustomer(name,phone,balance):
    cust1 = customer(name,phone,balance)
    dbhelp = dbHelper()
    dbhelp.saveCustomerInDB(cust1)

def updateCustomerAdd(amount,phone):
    balance = row[2] + amount
    dbhelp = dbHelper()
    dbhelp.updateCustomerInDB(balance,phone)

def updateCustomerWithdraw(amount,phone):
    balance = row[2] - amount
    dbhelp = dbHelper()
    dbhelp.updateCustomerInDB(balance,phone)


def updateCustomerTransfer(amount,phone,transferPhone):
    balance = row[2] - amount
    balance2 = transferRow[2] + amount
    dbhelp = dbHelper()
    dbhelp.updateCustomerInDB(balance, phone)
    dbhelp.updateCustomerInDB(balance2, transferPhone)

def addTransactionAdd(phone, amount,today):
    dbhelper = dbHelper()
    dbhelper.saveCustomerInTransAdd(phone,amount,today)

def addTransactionWithdraw(phone, amount,today):
    dbhelper = dbHelper()
    dbhelper.saveCustomerInTransWithdraw(phone,amount,today)

def addTransactionTransfer(phone, amount, transferPhone,today):
    dbhelper = dbHelper()
    dbhelper.saveCustomerInTransTransfer(phone,amount,transferPhone,today)

def onClickSubmit():
    global phone
    phone = entryMobile.get()
    fetchAccount(phone)
    if row is not None:
        window.destroy()
        exists()

    elif row is None:
        window.destroy()
        notExist()

def onClickAddAccount():
    name = entryName.get()
    phn = entryPhone.get()
    bal = entryAmount.get()
    addCustomer(name,phn,bal)
    addTransactionAdd(phn,bal,today)
    window4.destroy()
    AddCustSucc()

def onClickAddMoney():
    window1.destroy()
    Add()

def onClickWithdrawMoney():
    window1.destroy()
    Withdraw()

def onClickTransferMoney():
    window1.destroy()
    Transfer()

def onClickAdd():
    amount = int(entryAdd.get())
    dateTime()
    updateCustomerAdd(amount,phone)
    addTransactionAdd(phone,amount,today)
    window2.destroy()
    AddSucc()

def onClickWithdraw():
    amount = int(entryWithdraw.get())
    dateTime()
    if amount < row[2] and row[2] >= 1000:
        updateCustomerWithdraw(amount,phone)
        addTransactionWithdraw(phone,amount,today)
        window3.destroy()
        WithDrawSucc()
    else:
        balLow()

def onClickTransfer():
    global transferPhone
    transferAmount = int(entryTransferAmt.get())
    transferPhone = entryTransferPhn.get()
    fetchAccountTransfer(transferPhone)
    if transferAmount < row[2] and row[2] >= 1000:
        if transferRow is not None:
            dateTime()
            updateCustomerTransfer(transferAmount,phone,transferPhone)
            addTransactionTransfer(phone,transferAmount,transferPhone,today)
            window5.destroy()
            TransferDone()

        elif transferRow is None:
            window5.destroy()
            TransferNotDone()
    else:
        balLow()

def homeView():
    global window
    window = Tk()

    lblTitle = Label(window, text="Wallet App")
    lblTitle.pack()

    global entryMobile
    lblMobile = Label(window, text="Enter Mobile No.")
    lblMobile.pack()

    entryMobile = Entry(window)
    entryMobile.pack()

    btnAddCustomer = Button(window, text="Submit", command=onClickSubmit)
    btnAddCustomer.pack()

    window.mainloop()

def exists():
    global window1
    window1 = Tk()

    lblExist = Label(window1, text="Account Exists!!")
    lblExist.pack()

    btnADD = Button(window1, text="Add Money", command=onClickAddMoney)
    btnADD.pack()

    btnWithdraw = Button(window1, text="Withdraw Money", command=onClickWithdrawMoney)
    btnWithdraw.pack()

    btnTransfer = Button(window1, text="Transfer Money", command = onClickTransferMoney)
    btnTransfer.pack()

    window1.mainloop()

def notExist():
    global window4
    window4 = Tk()

    lblnotExist = Label(window4, text="Account does not Exists!!")
    lblnotExist.pack()

    lblName = Label(window4, text="Enter Name")
    lblName.pack()

    global entryName
    entryName = Entry(window4)
    entryName.pack()

    lblPhone = Label(window4, text="Enter Mobile No.")
    lblPhone.pack()

    global entryPhone
    entryPhone = Entry(window4)
    entryPhone.pack()

    lblAmount = Label(window4, text="Enter Amount")
    lblAmount.pack()

    global entryAmount
    entryAmount = Entry(window4)
    entryAmount.pack()

    btnAddAccount = Button(window4,text ="Add Account",command = onClickAddAccount)
    btnAddAccount.pack()

    window4.mainloop()

def Add():
    global window2
    window2 = Tk()

    lblAdd = Label(window2, text="Enter Amount")
    lblAdd.pack()

    global entryAdd
    entryAdd = Entry(window2)
    entryAdd.pack()

    btnAdd = Button(window2, text="ADD", command=onClickAdd)
    btnAdd.pack()

    window2.mainloop()

def Withdraw():
    global window3
    window3 = Tk()

    lblWithdraw = Label(window3, text="Enter Amount")
    lblWithdraw.pack()

    global entryWithdraw
    entryWithdraw = Entry(window3)
    entryWithdraw.pack()

    btnWithdraw = Button(window3, text="Withdraw",command = onClickWithdraw)
    btnWithdraw.pack()

    window3.mainloop()

def Transfer():
    global window5
    window5 = Tk()

    lblTransferAmt = Label(window5, text="Enter Amount")
    lblTransferAmt.pack()

    global entryTransferAmt
    entryTransferAmt = Entry(window5)
    entryTransferAmt.pack()

    lblTransferPhn = Label(window5, text="Enter Mobile ")
    lblTransferPhn.pack()

    global entryTransferPhn
    entryTransferPhn = Entry(window5)
    entryTransferPhn.pack()

    btnTransfer = Button(window5, text="Transfer", command = onClickTransfer)
    btnTransfer.pack()

    window5.mainloop()

def TransferDone():
    def onClickOk():
        window6.destroy()

    window6 = Tk()

    lbltransferDone = Label(window6, text="Transfer Done!!")
    lbltransferDone.pack()

    btnOK = Button(window6, text = "OK !!", command = onClickOk)
    btnOK.pack()

    window6.mainloop()

def TransferNotDone():
    def onClickOk():
        window7.destroy()
        Transfer()

    global window7
    window7 = Tk()

    lbltransferNot = Label(window7, text="Please Enter Valid Mobile No.!!")
    lbltransferNot.pack()

    btnOK = Button(window7, text="OK !!", command = onClickOk)
    btnOK.pack()

    window7.mainloop()

def AddSucc():
    def onClickOK():
        window8.destroy()

    window8 = Tk()

    lblSucc = Label(window8,text="Money Added SuccessFully!!")
    lblSucc.pack()

    btnOk = Button(window8,text = "Ok",command = onClickOK)
    btnOk.pack()

    window8.mainloop()

def WithDrawSucc():
    def onClickOK():
        window9.destroy()

    window9 = Tk()

    lblSucc = Label(window9, text="Withdraw SuccessFully!!")
    lblSucc.pack()

    btnOk = Button(window9, text="Ok", command=onClickOK)
    btnOk.pack()

    window9.mainloop()

def AddCustSucc():
    def onClickOK():
        window10.destroy()

    window10 = Tk()
    lblSucc = Label(window10, text="Customer Added SuccessFully!!")
    lblSucc.pack()

    btnOk = Button(window10, text="Ok", command=onClickOK)
    btnOk.pack()

    window10.mainloop()

def balLow():

    def onClickOk():
        window11.destroy()
    window11 = Tk()
    lblLow = Label(window11, text = "Insufficient Balance!!")
    lblLow.pack()

    btnOk = Button(window11, text = "Ok",command = onClickOk)
    btnOk.pack()

    window11.mainloop()

homeView()





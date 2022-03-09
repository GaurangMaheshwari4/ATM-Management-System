from tkinter import * #module for creating GUI
from tkinter import messagebox #module for creating GUI
from PIL import Image, ImageTk #module to resize the image
import time #module to create delay
import re #module to check pattern matching
import SendOTP #user defined module to send randomly generated OTP to registered emails

list_Account = list()

def Account_info(): #Read Account details from file and store it in form of list
    global list_Account
    try:
        list_Account = list()
        file = open("Account.txt","r")
        print("File exists!")
        Content = file.read()
        sep_Account = (Content.strip()).split("$$")
        sep_Account.remove('')
        for i in range(len(sep_Account)):
            list_Account.append((sep_Account[i].strip()).splitlines())
    except:
        file = open("Account.txt","w")
        print("File created!")
    file.close()

def write(): #write account details in file from a list
    file = open("Account.txt","w")
    msg = ""
    for i in range(len(list_Account)):
        for j in range(len(list_Account[0])):
            msg=msg+list_Account[i][j]+"\n"
        msg=msg+"$$"+"\n"
    msg=msg[:-1]
    file.write(msg)
    file.close()

class Welcome(Tk): #Window for login or initial page
    def __init__(self):
        super().__init__()
        self.geometry("800x600+250+50")
        self.resizable(0,0)
        self.title("Nirma Bank")
        Bank_Logo = PhotoImage(file="Bank.png")
        self.iconphoto(True,Bank_Logo)
        self.configure(background="pink")

        my_canvas1 = Canvas(self, width=800, height=600,bg="pink")
        my_canvas1.pack(fill="both",expand=True)
        Account_Frame = LabelFrame(my_canvas1,text="Welcome to Nirma Bank",font=("Helvetica",15,"bold"),height=450,width=600,bd=5,bg="SkyBlue1",relief=SOLID)
        Nirma_logo = Image.open("Nirma_logo.png")
        Nirma_logo1 = Nirma_logo.resize((225,150))
        self.Nirma_logo2 = ImageTk.PhotoImage(Nirma_logo1)
        Label(Account_Frame,image=self.Nirma_logo2,bg="SkyBlue1").place(relx=0.1, rely=0.3)
        Bank_logo = Image.open("Bank.png")
        Bank_logo1 = Bank_logo.resize((100,100))
        self.Bank_logo2 = ImageTk.PhotoImage(Bank_logo1)

        User_logo = Image.open("Username.png")
        User_logo1 = User_logo.resize((25,25))
        self.User_logo2 = ImageTk.PhotoImage(User_logo1)

        Pass_logo = Image.open("Password.png")
        Pass_logo1 = Pass_logo.resize((25,25))
        self.Pass_logo2 = ImageTk.PhotoImage(Pass_logo1)
        User = Label(Account_Frame,bg="SkyBlue1")
        Label(User,image=self.User_logo2,bg="SkyBlue1").grid(row=0,column=0,sticky="w")
        self.Account_Number=Entry(User,font=("Helvetica",15),width=15,bg="LightSkyBlue1")
        self.Account_Number.grid(row=0,column=1,sticky="w",padx=5)
        User.place(relx=0.6, rely=0.4)

        Pass = Label(Account_Frame,bg="SkyBlue1")
        Label(Pass,image=self.Pass_logo2,bg="SkyBlue1").grid(row=0,column=0,sticky="w")
        self.PIN_Number=Entry(Pass,font=("Helvetica",15),width=15,show="*",bg="LightSkyBlue1")
        self.PIN_Number.grid(row=0,column=1,sticky="w",padx=5)
        Pass.place(relx=0.6, rely=0.6)

        Label(Account_Frame,image=self.Bank_logo2,bg="SkyBlue1").place(relx=0.7, rely=0.05)
        self.Proceed = Button(Account_Frame,text="Click here to Proceed",bg="blue",fg="yellow",font=("Helvetica",13,"bold"),relief=FLAT,activebackground="blue",activeforeground="yellow",command=self.validate)
        self.Proceed.place(relx=0.63, rely=0.8,height=30)

        my_canvas1.create_window(100,75,window=Account_Frame,anchor="nw")
    
    def validate(self): #checks if entered account number and PIN number are there in bank and proceed further
        global index
        index = -1
        for i in range(len(list_Account)):
            if list_Account[i][0] == self.Account_Number.get() and list_Account[i][1] == self.PIN_Number.get():
                index = i 
                break
        self.Account_Number.delete(0,"end")
        self.PIN_Number.delete(0,"end")
        if index != -1:
            self.withdraw()
            Services(self)
        else:
            messagebox.showerror("Nirma Bank","Invalid Account Number or PIN")

class Services(Toplevel): #Window that shows option available in ATM and displays process that are carried out
    def __init__(self,root):
        super().__init__(root)
        self.message=None
        self.geometry("800x600+250+50")
        self.resizable(0,0)
        self.title(f"Account Number - {list_Account[index][0]}")
        self.protocol("WM_DELETE_WINDOW",root.destroy)
        my_canvas1 = Canvas(self, width=800, height=600,bg="SpringGreen4")
        my_canvas1.pack(fill="both",expand=True)
        my_canvas2 = Canvas(self, width=640, height=250,bg="LightBlue1")
        my_canvas2.place(relx=0.1,rely=0.05)
        self.my_canvas3 = Canvas(self, width=640, height=250,bg="LightBlue1")
        self.my_canvas3.place(relx=0.1,rely=0.50)
        Withdraw = Button(self,text="Cash Withdrawal",font=("Helvetica",13,"bold"),bg="SpringGreen1",fg="black",height=1,width=25,activebackground="SpringGreen1",activeforeground="black",relief=SOLID,command = lambda:[self.withdraw()])

        Transfer = Button(self,text="Transfer",font=("Helvetica",13,"bold"),bg="SpringGreen1",fg="black",height=1,width=25,activebackground="SpringGreen1",activeforeground="black",relief=SOLID,command = lambda:[self.transfer()])

        exit = Button(self,text="Exit",font=("Helvetica",13,"bold"),bg="SpringGreen1",fg="black",height=1,width=25,activebackground="SpringGreen1",activeforeground="black",relief=SOLID,command=lambda: [self.destroy(),time.sleep(1), root.deiconify()])

        Check = Button(self,text="Balance Inquiry",font=("Helvetica",13,"bold"),bg="SpringGreen1",fg="black",height=1,width=25,activebackground="SpringGreen1",activeforeground="black",relief=SOLID,command = lambda:[self.check_balance()])

        Change = Button(self,text="Change or Create PIN",font=("Helvetica",13,"bold"),bg="SpringGreen1",fg="black",height=1,width=25,activebackground="SpringGreen1",activeforeground="black",relief=SOLID,command = lambda:[self.Change_PIN()])

        Deposit = Button(self,text="Deposit",font=("Helvetica",13,"bold"),bg="SpringGreen1",fg="black",height=1,width=25,activebackground="SpringGreen1",activeforeground="black",relief=SOLID,command = lambda:[self.deposit()])

        Option_frame = LabelFrame(my_canvas2,text="Select a Option",font=("Helvetica",15,"bold"),height=240,width=630,bd=2,bg="LightBlue1",relief=SOLID)
        my_canvas2.create_window(0,0,window=Option_frame,anchor="nw")
        my_canvas2.create_window(150,60,window=Withdraw)
        my_canvas2.create_window(150,130,window=Transfer)
        my_canvas2.create_window(150,200,window=Check)
        my_canvas2.create_window(490,60,window=Deposit)
        my_canvas2.create_window(490,130,window=Change)
        my_canvas2.create_window(490,200,window=exit)
    
    def withdraw(self): #this will be performed if withdrawal button is pressed
        if self.message:
            self.my_canvas3.delete(self.message)
            self.message=None
        choice = "withdraw"
        check(self,choice)

    def deposit(self): #this will be performed if deposit button is pressed
        if self.message:
            self.my_canvas3.delete(self.message)
            self.message=None
        choice = "deposit"
        check(self,choice)
    
    def check_balance(self): #this will be performed if  balance inquiry button is pressed
        if self.message:
            self.my_canvas3.delete(self.message)
            self.message=None
        choice = "check"
        check(self,choice)
    
    def transfer(self): #this will be performed if transfer button is pressed
        if self.message:
            self.my_canvas3.delete(self.message)
            self.message=None
        choice = "transfer"
        check(self,choice)

    def Change_PIN(self): #this will be performed if Change PIN button is pressed
        if self.message:
            self.my_canvas3.delete(self.message)
            self.message=None
        choice = "PIN"
        check(self,choice)


    def summary(self,message): #prints the process which was carried out
        self.message=self.my_canvas3.create_text(320,50,text=message,fill="black",font=("Helvetica",15,"bold"))
        

class check(Toplevel):#Window to check PIN number of current Account and proceed accordingly to the button pressed in service class
    def __init__(self,root,choice):
        super().__init__(root)
        self.geometry("400x300+450+150")
        self.resizable(0,0)
        self.configure(background="SpringGreen1")
        my_canvas1 = Canvas(self, width=360, height=270,bg="LightBlue1")
        my_canvas1.place(relx=0.05,rely=0.05)
        my_canvas1.create_text(180,70,text="Verification",fill="black",font=("Helvetica",20,"bold"))
        my_canvas1.create_text(100,150,text="Enter PIN",fill="black",font=("Helvetica",15,"bold"))
        self.PIN = Entry(my_canvas1,font=("Helvetica",15,"bold"),highlightcolor="black",highlightbackground="black",bg="LightBlue1",fg="black",show="*",highlightthickness=2)
        my_canvas1.create_window(260,150,window=self.PIN,height=34,width=150)
        Confirm = Button(self,text="Confirm",font=("Helvetica",15,"bold"),bg="SpringGreen1",fg="black",height=1,width=10,activebackground="SpringGreen1",activeforeground="black",relief=SOLID,command=lambda:[self.checkPIN(root,choice)])
        my_canvas1.create_window(180,230,window=Confirm)

    def checkPIN(self,root,choice): #display error pop-up if incorrect PIN is entered and displays different windows according to button pressed in service class 
        if self.PIN.get()!=list_Account[index][1]:
            self.PIN.delete(0,"end")
            messagebox.showerror("Nirma Bank","Invalid PIN")
        else:
            self.destroy()
            if choice == "withdraw":
                Withdraw(root)
            elif choice == "deposit":
                Deposit(root)
            elif choice == "check":
                msg = f"Account Number : {list_Account[index][0]}\nBalance : {list_Account[index][2]}\nEmail : {list_Account[index][3]}"
                root.summary(msg)
            elif choice == "transfer":
                Transfer(root)
            elif choice == "PIN":
                PIN(root)

        

class Withdraw(Toplevel): #Withdraw window to input amount to be withdrawed
    def __init__(self,root):
        super().__init__(root)
        self.geometry("400x300+450+150")
        self.resizable(0,0)
        self.configure(background="SpringGreen1")
        my_canvas1 = Canvas(self, width=360, height=270,bg="LightBlue1")
        my_canvas1.place(relx=0.05,rely=0.05)
        my_canvas1.create_text(180,70,text="Withdraw",fill="black",font=("Helvetica",20,"bold"))
        my_canvas1.create_text(100,150,text="Enter Amount:",fill="black",font=("Helvetica",15,"bold"))
        self.Amount = Entry(my_canvas1,font=("Helvetica",15,"bold"),highlightcolor="black",highlightbackground="black",bg="LightBlue1",fg="black",highlightthickness=2)
        my_canvas1.create_window(260,150,window=self.Amount,height=34,width=150)
        Confirm = Button(self,text="Confirm",font=("Helvetica",15,"bold"),bg="SpringGreen1",fg="black",height=1,width=10,activebackground="SpringGreen1",activeforeground="black",relief=SOLID,command=lambda:[self.confirm(root)])
        my_canvas1.create_window(180,230,window=Confirm)

    def confirm(self,root):
        try:
            amount = float(self.Amount.get())
            if amount > float(list_Account[index][2]):
                root.summary("Insufficient Balance")
            elif amount > 10000.00:
                root.summary("Withdraw Amount should be less than 10,000")
            else:
                list_Account[index][2] = "{:.2f}".format(float(list_Account[index][2])-amount)
                root.summary(f"{self.Amount.get()} withdrawed successfully\nUpdated balance: {list_Account[index][2]}")
                write()
            self.destroy()
        except:
            self.Amount.delete(0,"end")
            messagebox.showerror("Nirma Bank","Amount should be numeric only")

class Deposit(Toplevel): #Deposit window to input amount to be deposited
    def __init__(self,root):
        super().__init__(root)
        self.geometry("400x300+450+150")
        self.resizable(0,0)
        self.configure(background="SpringGreen1")
        my_canvas1 = Canvas(self, width=360, height=270,bg="LightBlue1")
        my_canvas1.place(relx=0.05,rely=0.05)
        my_canvas1.create_text(180,70,text="Deposit",fill="black",font=("Helvetica",20,"bold"))
        my_canvas1.create_text(100,150,text="Enter Amount:",fill="black",font=("Helvetica",15,"bold"))
        self.Amount = Entry(my_canvas1,font=("Helvetica",15,"bold"),highlightcolor="black",highlightbackground="black",bg="LightBlue1",fg="black",highlightthickness=2)
        my_canvas1.create_window(260,150,window=self.Amount,height=34,width=150)
        Confirm = Button(self,text="Confirm",font=("Helvetica",15,"bold"),bg="SpringGreen1",fg="black",height=1,width=10,activebackground="SpringGreen1",activeforeground="black",relief=SOLID,command=lambda:[self.confirm(root)])
        my_canvas1.create_window(180,230,window=Confirm)

    def confirm(self,root):
        try:
            amount = float(self.Amount.get())
            if amount > 10000.00:
                root.summary("You cant deposit more than 10,000 at a time")
            else:
                list_Account[index][2] = "{:.2f}".format(float(list_Account[index][2])+amount)
                root.summary(f"{self.Amount.get()} deposited successfully\nUpdated balance: {list_Account[index][2]}")
                write()
            self.destroy()
        except:
            self.Amount.delete(0,"end")
            messagebox.showerror("Nirma Bank","Amount should be numeric only")

class Transfer(Toplevel): #Transfer window to input amount to be transferred and input account number to be transferred to
    def __init__(self,root):
        super().__init__(root)
        self.geometry("400x300+450+150")
        self.resizable(0,0)
        self.configure(background="SpringGreen1")
        my_canvas1 = Canvas(self, width=360, height=270,bg="LightBlue1")
        my_canvas1.place(relx=0.05,rely=0.05)
        my_canvas1.create_text(180,70,text="Transfer",fill="black",font=("Helvetica",20,"bold"))
        my_canvas1.create_text(100,180,text="Enter Amount:",fill="black",font=("Helvetica",15,"bold"))
        self.Amount = Entry(my_canvas1,font=("Helvetica",15,"bold"),highlightcolor="black",highlightbackground="black",bg="LightBlue1",fg="black",highlightthickness=2)
        my_canvas1.create_window(260,180,window=self.Amount,height=34,width=150)
        my_canvas1.create_text(100,125,text="Transfer to:",fill="black",font=("Helvetica",15,"bold"))
        self.to = Entry(my_canvas1,font=("Helvetica",15,"bold"),highlightcolor="black",highlightbackground="black",bg="LightBlue1",fg="black",highlightthickness=2)
        my_canvas1.create_window(260,125,window=self.to,height=34,width=150)
        Confirm = Button(self,text="Confirm",font=("Helvetica",15,"bold"),bg="SpringGreen1",fg="black",height=1,width=10,activebackground="SpringGreen1",activeforeground="black",relief=SOLID,command=lambda:[self.confirm(root)])
        my_canvas1.create_window(180,230,window=Confirm)

    def confirm(self,root):
        try:
            receiver = -1
            amount = float(self.Amount.get())
            for i in range(len(list_Account)):
                if list_Account[i][0] == self.to.get():
                    receiver = i
                    break
            if receiver == index:
                root.summary("You cant transfer to your own account")
            elif receiver == -1:
                root.summary("Receiver Account is invalid")
            elif amount > float(list_Account[index][2]):
                root.summary("Insufficient Balance") 
            elif amount > 10000.00:
                root.summary("You cant transfer more than 10,000 at a time")
            else:
                list_Account[index][2] = "{:.2f}".format(float(list_Account[index][2])-amount)
                list_Account[receiver][2] = "{:.2f}".format(float(list_Account[receiver][2])+amount)
                root.summary(f"{self.Amount.get()} transferred to Account Number {self.to.get()} successfully\nUpdated balance: {list_Account[index][2]}")
                write()
            self.destroy()
        except:
            self.Amount.delete(0,"end")
            self.to.delete(0,"end")
            messagebox.showerror("Nirma Bank","Amount should be numeric only")

class PIN(Toplevel): #Window that checks if registered email ID is valid by sending OTP and validating
    def __init__(self,root):
        try:
            self.eOTP = SendOTP.send_otp(list_Account[index][3])
        except:
            pass
        super().__init__(root)
        self.geometry("400x300+450+150")
        self.resizable(0,0)
        self.configure(background="SpringGreen1")
        my_canvas1 = Canvas(self, width=360, height=270,bg="LightBlue1")
        my_canvas1.place(relx=0.05,rely=0.05)
        my_canvas1.create_text(180,70,text="Email Verification",fill="black",font=("Helvetica",20,"bold"))
        my_canvas1.create_text(100,150,text="Enter OTP:",fill="black",font=("Helvetica",15,"bold"))
        self.OTP = Entry(my_canvas1,font=("Helvetica",15,"bold"),highlightcolor="black",highlightbackground="black",bg="LightBlue1",fg="black",highlightthickness=2)
        my_canvas1.create_window(260,150,window=self.OTP,height=34,width=150)
        Confirm = Button(self,text="Confirm",font=("Helvetica",15,"bold"),bg="SpringGreen1",fg="black",height=1,width=10,activebackground="SpringGreen1",activeforeground="black",relief=SOLID,command=lambda:[self.confirm(root)])
        my_canvas1.create_window(180,230,window=Confirm)

    def confirm(self,root):
        if self.OTP.get() == self.eOTP:
            self.destroy()
            cPIN(root)
        else:
            self.OTP.delete(0,"end")
            messagebox.showerror("Nirma Bank","Wrong OTP")

class cPIN(Toplevel): #Window that takes new PIN and change PIN number of Account if it is valid
    def __init__(self,root):
        super().__init__(root)
        self.geometry("400x300+450+150")
        self.resizable(0,0)
        self.configure(background="SpringGreen1")
        my_canvas1 = Canvas(self, width=360, height=270,bg="LightBlue1")
        my_canvas1.place(relx=0.05,rely=0.05)
        my_canvas1.create_text(180,70,text="Change PIN",fill="black",font=("Helvetica",20,"bold"))
        my_canvas1.create_text(100,180,text="Confirm New PIN:",fill="black",font=("Helvetica",15,"bold"))
        self.confPIN = Entry(my_canvas1,font=("Helvetica",15,"bold"),highlightcolor="black",highlightbackground="black",bg="LightBlue1",fg="black",highlightthickness=2,show="*")
        my_canvas1.create_window(260,180,window=self.confPIN,height=34,width=150)
        my_canvas1.create_text(100,125,text="New PIN:",fill="black",font=("Helvetica",15,"bold"))
        self.PIN = Entry(my_canvas1,font=("Helvetica",15,"bold"),highlightcolor="black",highlightbackground="black",bg="LightBlue1",fg="black",highlightthickness=2,show="*")
        my_canvas1.create_window(260,125,window=self.PIN,height=34,width=150)
        Confirm = Button(self,text="Confirm",font=("Helvetica",15,"bold"),bg="SpringGreen1",fg="black",height=1,width=10,activebackground="SpringGreen1",activeforeground="black",relief=SOLID,command=lambda:[self.confirm(root)])
        my_canvas1.create_window(180,230,window=Confirm)

    def confirm(self,root):
        if re.search("^[0-9][0-9]{2}[0-9]$",self.PIN.get()) and re.search("^[0-9][0-9]{2}[0-9]$",self.confPIN.get()):
            if self.PIN.get() == self.confPIN.get():
                list_Account[index][1] = self.PIN.get()
                root.summary(f"PIN Changed Successfully")
                write()
                self.destroy()
                pass
            else:
                self.PIN.delete(0,"end")
                self.confPIN.delete(0,"end")
                messagebox.showerror("Nirma Bank","PIN and Confirm PIN are different")
        else:
            self.PIN.delete(0,"end")
            self.confPIN.delete(0,"end")
            messagebox.showerror("Nirma Bank","PIN should be of 4 digit and should be numeric")

if __name__=="__main__":
    Account_info() #Read account details in form of list
    root = Welcome() #creates object for Welcome class
    root.mainloop() #method in the main window to run infinite loop for events to occur
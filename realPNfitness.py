from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3
import re

def Database():
    global conn, cursor
    conn = sqlite3.connect("fitnesspn.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS MEM_REGISTRATION (MEM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,MEM_NAME TEXT, MEM_PHONE TEXT, MEM_EMAIL TEXT, MEM_GENDER TEXT, MEM_MEMBER TEXT)")

#ทำเลย์เอาท์ GUI หน้าต่าง
def DisplayForm():
    display_screen = Tk()
    display_screen.geometry("1120x500")
    display_screen.title("FITNESS PN.COM")
    global tree
    global SEARCH
    global mem_id,name,phone,email,gender,member,mem_id, nameent, phoneent, emailent
    mem_id = StringVar()
    SEARCH = StringVar()
    name = StringVar()
    phone = StringVar()
    email = StringVar()
    gender = StringVar()
    member = StringVar()
    
    TopViewForm = Frame(display_screen, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    #GUI ที่สมัครด้านซ้าย
    LFrom = Frame(display_screen, width="350")
    LFrom.pack(side=LEFT, fill=Y)
    #GUI ที่เสริชหาชื่อด้านขวา
    LeftViewForm = Frame(display_screen, width=500,bg="#F08080")
    LeftViewForm.pack(side=LEFT, fill=Y)
    #ตัวหน้าโชว์ เมื่อค้นหา
    MidViewForm = Frame(display_screen, width=600)
    MidViewForm.pack(side=RIGHT)
    #เลเบลเฮดเดอร์
    lbh_text = Label(TopViewForm, text="Member Management System", font=('verdana', 18), width=600,bg="#B03060",fg="white")
    lbh_text.pack(fill=X)
    #สร้าเลเบล
    Label(LFrom, text="Name  ", font=("Arial", 12)).pack(side=TOP)
    nameent = Entry(LFrom,font=("Arial",10,"bold"),textvariable=name).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Phone ", font=("Arial", 12)).pack(side=TOP)
    phoneent = Entry(LFrom, font=("Arial", 10, "bold"),textvariable=phone).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Email ", font=("Arial", 12)).pack(side=TOP)
    emailent = Entry(LFrom, font=("Arial", 10, "bold"),textvariable=email).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Gender ", font=("Arial", 12)).pack(side=TOP)
    gender = StringVar(value="Please select")
    OptionMenu(LFrom, gender,"Male", "Female").pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Member ", font=("Arial", 12)).pack(side=TOP)
    member = StringVar(value="Please select")
    OptionMenu(LFrom, member, "Day", "Month", "Year").pack(side=TOP, padx=10, fill=X)

    lbs_txtsearch = Label(LeftViewForm, text="Enter name to Search", font=('verdana', 10),bg="#F08080")
    lbs_txtsearch.pack()

    search = Entry(LeftViewForm, textvariable=SEARCH, font=('verdana', 15), width=10)
    search.pack(side=TOP, padx=10, fill=X)

    btn_search = Button(LeftViewForm, text="Search", command=SearchRecord)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    
    btn_view = Button(LeftViewForm, text="View All", command=DisplayData)
    btn_view.pack(side=TOP, padx=10, pady=10, fill=X)
   
    btn_reset = Button(LeftViewForm, text="Reset", command=Reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
   
    btn_delete = Button(LeftViewForm, text="Delete", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
   
    btn_edit = Button(LeftViewForm, text="Edit", command=edit)
    btn_edit.pack(side=TOP, padx=10, pady=10, fill=X)

    btn_update = Button(LeftViewForm, text="Update", command=Update)
    btn_update.pack(side=TOP, padx=10, pady=10, fill=X)

    btn_register = Button(LeftViewForm, text="Submit", command=register)
    btn_register.pack(side=TOP, padx=10, pady=10, fill=X)

    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm,columns=("Member Id", "Name", "Phone", "Email","Gender","Member"),
                        selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    #สร้าง heading บน คอลัมน์
    tree.heading('Member Id', text="Member Id", anchor=W)
    tree.heading('Name', text="Name", anchor=W)
    tree.heading('Phone', text="Phone", anchor=W)
    tree.heading('Email', text="Email", anchor=W)
    tree.heading('Gender', text="Gender", anchor=W)
    tree.heading('Member', text="Member", anchor=W)
    #setting width of the columns
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)
    tree.column('#2', stretch=NO, minwidth=0, width=150)
    tree.column('#3', stretch=NO, minwidth=0, width=80)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.pack()
    DisplayData()

#เพิ่มข้อมูล
def register():
    Database()
    name1=name.get()
    phone1=phone.get()
    email1=email.get()
    gender1=gender.get()
    member1=member.get()
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if (name1==''):
        tkMessageBox.showinfo("Warning","fill the empty field!!!")
    elif ( phone1==''):
        tkMessageBox.showinfo("Warning","fill the empty field!!!")
    elif ( email1=='' ):
        tkMessageBox.showinfo("Warning","fill the empty field!!!")
    elif ( gender1=='Please select'):
        tkMessageBox.showinfo("Warning","fill the empty field!!!")
    elif (member1=='Please select'):
        tkMessageBox.showinfo("Warning","fill the empty field!!!")
    elif not (name1.isalpha()):
        tkMessageBox.showinfo("Warning"," Name : Please enter only letters.")
    elif not (phone1.isdigit() and (len(phone1) == 10)):
        tkMessageBox.showinfo("Warning"," Phone : Please enter a valid phone number.")
    elif not (re.fullmatch(regex, email1)) :
        tkMessageBox.showinfo("Warning"," Email : Please enter a valid email address.")    
    else:
        conn.execute('INSERT INTO MEM_REGISTRATION (MEM_NAME,MEM_PHONE,MEM_EMAIL,MEM_GENDER,MEM_MEMBER) \
              VALUES (?,?,?,?,?)',(name1,phone1,email1,gender1,member1));
        conn.commit()
        tkMessageBox.showinfo("Message","Stored successfully")
        DisplayData()
        conn.close()

#reset
def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")
    name.set("")
    phone.set("")
    email.set("")
    gender.set("Please select")
    member.set("Please select")

#ลบข้อมูล
def Delete():
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("Warning","Select data to delete")
    else:
        result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            cursor=conn.execute("DELETE FROM MEM_REGISTRATION WHERE MEM_ID = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()

#อัพเดท
def Update():
    mem_id2=mem_id.get()
    name2=name.get()
    phone2=phone.get()
    email2=email.get()
    gender2=gender.get()
    member2=member.get()

    conn = sqlite3.connect("fitnesspn.db")
    cursor = conn.cursor()

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if (name2==''):
        tkMessageBox.showinfo("Warning","fill the empty field!!!")
    elif ( phone2==''):
        tkMessageBox.showinfo("Warning","fill the empty field!!!")
    elif ( email2=='' ):
        tkMessageBox.showinfo("Warning","fill the empty field!!!")
    elif ( gender2=='Please select'):
        tkMessageBox.showinfo("Warning","fill the empty field!!!")
    elif (member2=='Please select'):
        tkMessageBox.showinfo("Warning","fill the empty field!!!")
    elif not (name2.isalpha()):
        tkMessageBox.showinfo("Warning"," Name : Please enter only letters.")
    elif not (phone2.isdigit() and (len(phone2) == 10)):
        tkMessageBox.showinfo("Warning"," Phone : Please enter a valid phone number.")
    elif not (re.fullmatch(regex, email2)) :
        tkMessageBox.showinfo("Warning"," Email : Please enter a valid email address.")

    else :
        cursor.execute(' UPDATE MEM_REGISTRATION SET MEM_NAME = ?, MEM_PHONE = ?, MEM_EMAIL = ?, MEM_GENDER = ?, MEM_MEMBER = ? WHERE MEM_ID =? ', 
            (name2,phone2,email2,gender2,member2,mem_id2))
        tkMessageBox.showinfo("Message","Edit successfully")
        conn.commit()
        conn.close()
        
        DisplayData()

#แก้ไข
def edit():
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("Warning","Select data to delete")
    else:
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            cursor=conn.execute("SELECT * FROM MEM_REGISTRATION WHERE MEM_ID = %d" % selecteditem[0])
            for x in cursor :
                name.set(x[1])
                phone.set(x[2])
                email.set(x[3])
                gender.set(x[4])
                member.set(x[5]) 
                mem_id.set(x[0])
            conn.commit()
            cursor.close()
            conn.close()

#ค้นหา
def SearchRecord():
    Database()
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        cursor=conn.execute("SELECT * FROM MEM_REGISTRATION WHERE MEM_NAME LIKE ?", ('%' + str(SEARCH.get()) + '%',))
        fetch = cursor.fetchall()
        for data in fetch:
           tree.insert('', 'end', values=(data)) 
        cursor.close()
        conn.close()

#show
def DisplayData():
    Database()
    tree.delete(*tree.get_children())
    cursor=conn.execute("SELECT * FROM MEM_REGISTRATION")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

DisplayForm()
if __name__=='__main__':
 mainloop()
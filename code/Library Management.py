# library management
import mysql.connector
import datetime

# connection to my sql
mydbl=mysql.connector.connect(host="localhost", user="root", password="root",database="little_world")
cur=mydbl.cursor()
mydbl.commit()
mydbl.autocommit=True

# defining functions
def view_stock():
    cur.execute("select * from lib")
    fetch_data=cur.fetchall()
    print(fetch_data[0],"\n",fetch_data[1],"\n",fetch_data[2],"\n",fetch_data[3],"\n")

def view_subs():
    cur.execute("select * from subscription")
    fetch_data = cur.fetchall()
    for i in range(len(fetch_data)):
        i-=1
        if len(fetch_data)==0:
            print("No book issued by anyone!")
        else:
            print(f"{fetch_data[i][2]} Book issued by {fetch_data[i][1]} on {fetch_data[i][3]}")
    print("\n")
def view_stu():
    cur.execute("select * from student")
    fetch_data = cur.fetchall()
    for i in range(len(fetch_data)):
        i-=1
        if not fetch_data:
            print("[]")
        else:
            print(fetch_data[i])


def add_user():
    stu_rollno=int(input("Enter your roll_no :"))
    stu_name=input("Enter your name :")
    stu_card=int(input("Enter your card number :"))
    cur.execute(f'select Roll_no from student where Roll_no = {stu_rollno}')
    fetch=cur.fetchone()
    if fetch:
        cur.execute(f'insert into  student values({stu_rollno},"{stu_name}", {stu_card})\n')
    else:
        print("Your Name already exist in our database!!")
def add_user2():
    stu_rollno=int(input("Enter your roll_no :"))
    stu_name=input("Enter your name :")
    stu_card=int(input("Enter your card number :"))
    cur.execute(f'insert into student values({stu_rollno},"{stu_name}", {stu_card})\n')
    issue()


def remove_user():
    stu_rollno=int(input("Enter your roll_no :"))
    cur.execute("select Roll_no from student")
    datarollno=[]
    fetch=cur.fetchall()
    for i in range(len(fetch)):
        i=i-1
        datarollno.append(fetch[i][0])
    if stu_rollno in datarollno:
        cur.execute("select roll_no from subscription")
        fetch_rollno=cur.fetchall()
        data_rollno=[]
        for i in range(len(fetch_rollno)):
            i=i-1
            data_rollno.append(fetch_rollno[i][0])
        if stu_rollno in data_rollno:
            print("You already have a book issued!!\n")
        else:
            cur.execute(f"delete from student where Roll_no='{stu_rollno}'")
            print("User successfully removed.\n")
    else:
        print("This Roll no. doesn't exist in our database")
        yes=input("Do you want to add a new user? (Y/N) :")
        if yes.lower()=="y":
            add_user()
        else:
            return


def issue():
    global j
    option=input("Does your Name already exist? (Y/N) :")
    if option.lower()=="y":
        user_name=input("Enter your Name:")
        name_book=input("Enter name of book: ")

        cur.execute('select Name from student')
        stuname = cur.fetchall()
        stu_name = []
        for i in stuname:
            stu_name.append(i[0].lower())
        if user_name.lower() in stu_name:
            cur.execute('select * from student')
            studata = cur.fetchall()
            stu_rollno = []
            stu_name = []
            stu_nocard = []
            for i in studata:
                stu_rollno.append(i[0])
                stu_name.append(i[1].lower())
                stu_nocard.append(i[2])
            for i in range(len(stu_name)):
                i=i-1
                if user_name.lower() == stu_name[i]:
                    j = i
            if name_book.lower()=="maths":
                cur.execute('select * from lib where bookname="Maths"')
                x=cur.fetchall()[0][3]
                if x==0:
                    print("Stock Unavailable")
                else:
                    date_time=datetime.datetime.now()
                    year=date_time.year
                    month=date_time.month
                    day=date_time.day
                    date_final=f"{day}/{month}/{year}"
                    cur.execute(f'insert into subscription values({stu_rollno[j]},"{stu_name[j]}","Maths","{date_final}")')
                    print(f"Maths book Issued by {stu_name[j]}\n")

                    y=x-1
                    cur.execute(f'update lib set noofcopies = {y} where bookname="Maths"')

            elif name_book.lower()=="science":
                cur.execute('select * from lib where bookname="Science"')
                x=cur.fetchall()[0][3]
                if x==0:
                    print("Stock Unavailable")
                else:
                    y=x-1
                    cur.execute(f'update lib set noofcopies = {y} where bookname="Science"')
                    date_time=datetime.datetime.now()
                    year=date_time.year
                    month=date_time.month
                    day=date_time.day
                    date_final=f"{day}/{month}/{year}"
                    cur.execute(f'insert into subscription values({stu_rollno[j]},"{stu_name[j]}","Science","{date_final}")')
                    print(f"Science book Issued by {stu_name[j]}\n")


            elif name_book.lower()=="social studies" or name_book.lower()=="socialstudies":
                cur.execute('select * from lib where bookname="Social studies"')
                x=cur.fetchall()[0][3]
                if x==0:
                    print("Stock Unavailable")
                else:
                    y=x-1
                    cur.execute(f'update lib set noofcopies = {y} where bookname="Social studies"')
                    date_time=datetime.datetime.now()
                    year=date_time.year
                    month=date_time.month
                    day=date_time.day
                    date_final=f"{day}/{month}/{year}"
                    cur.execute(f'insert into subscription values({stu_rollno[j]},"{stu_name[j]}","Social studies","{date_final}")')
                    print(f"Social Studies book Issued by {stu_name[j]}\n")


            elif name_book.lower()== "computer sc." or name_book.lower()== "computer":
                cur.execute('select * from lib where bookname="Computer SC."')
                x=cur.fetchall()[0][3]
                if x==0:
                    print("Stock Unavailable\n")
                else:
                    y=x-1
                    cur.execute(f'update lib set noofcopies = {y} where bookname="computer sc."')
                    date_time=datetime.datetime.now()
                    year=date_time.year
                    month=date_time.month
                    day=date_time.day
                    date_final=f"{day}/{month}/{year}"
                    cur.execute(f'insert into subscription values({stu_rollno[j]},"{stu_name[j]}","computer sc.","{date_final}")')
                    print(f"Computer SC. book Issued by {stu_name[j]}\n")


            else:
                print("We don't have that book in our library!!")
        else:
            print("We don't have your name registered in our database\n")
            option=input("Do You want to add your name? (Y/N) :")
            if option.lower()=="y":
                add_user2()
            else:
                return
    else:
        add_user2()



def return_book():
    user_name = input("Enter your name: ")
    user_book = input("Enter your book: ")

    cur.execute("select Name from subscription")
    fetchname = cur.fetchall()
    fetch_name=[]
    for i in fetchname:
        fetch_name.append(i[0].lower())
    cur.execute(f'select Bookname from subscription where Name="{user_name}"')
    list2=[]
    for i in cur.fetchall():
        list2.append(i[0].lower())
    if user_name.lower() in fetch_name and user_book.lower() in list2:
        cur.execute(f'delete from subscription where Name="{user_name}" and Bookname="{user_book}" LIMIT 1')
        cur.execute(f'update lib set noofcopies=noofcopies+1 where bookname="{user_book}"')
        print(f"{user_book} Book returned by {user_name}\n")
    else:
        print("You don't have a subscription for that book!!\n")

# asking user's choice
while True:
    print("What operation you want to perform:\n1:Issue a book\n2:Return a book\n3:Show available books\n4:Show Subscriptions\n5:Add a new user\n6:Remove a user\n7:Quit")
    choice=int(input("-->"))
    if choice == 1:
        issue()
    elif choice == 2:
        return_book()
    elif choice == 3:
        view_stock()
        view_stu()
    elif choice==4:
        view_subs()
    elif choice==5:
        add_user()
    elif choice==6:
        remove_user()
    elif choice==7:
        break
    else:
        print("invalid option")

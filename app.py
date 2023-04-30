from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import mysql.connector
import pymysql
import datetime

# connecting mysql to this file
mydbl=pymysql.connect(host="localhost", user="root", password="root",database="database",cursorclass=pymysql.cursors.DictCursor)
cur=mydbl.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/available_books')
def available_books_():
    cur.execute("select * from lib")
    fetch_data1=cur.fetchall()
    # print(fetch_data[0],"\n",fetch_data[1],"\n",fetch_data[2],"\n",fetch_data[3],"\n")
    return render_template('available_books.html', fetch_data=fetch_data1)

@app.route('/issue',methods=['POST','GET'])
def issue_():
    if request.method == 'POST':    
        rollno=request.form.get('rollno')
        if rollno:
            cur.execute(f"select Roll_no from student where Roll_no='{rollno}'")
            fetch_data=cur.fetchall()
            check=()
            if fetch_data == check:
                message='Rollno. not found'
                return render_template('issue.html',message=message)
            else:
                user_choice=request.form["choosebooks"]
                if user_choice == '1':
                    user_book = 'Maths'
                elif user_choice == '2':
                    user_book = 'Science'
                elif user_choice == '3':
                    user_book = 'Social Studies'
                elif user_choice == '4':
                    user_book = 'Computer SC.'
                else:
                    message3='Choose a book!'
                    return render_template('issue.html', message=message3)
                
                cur.execute(f"select noofcopies from lib where bookname='{user_book}'")
                stock=cur.fetchone()
                if stock == 0:
                    message4='Stock not available!'
                    return render_template('issue.html', message=message4)
                else:
                    cur.execute(f"select * from student where Roll_no='{rollno}'")
                    date_time=datetime.datetime.now()
                    year=date_time.year
                    month=date_time.month
                    day=date_time.day
                    date_final=f"{day}/{month}/{year}"
                    cur.execute(f"select Name from student where Roll_no='{rollno}'")
                    fetch_name=cur.fetchone()
                    fetch_name=fetch_name['Name']
                    cur.execute(f'insert into subscription values({rollno},"{fetch_name}","{user_book}","{date_final}")')
                    mydbl.commit()
                    stock=stock['noofcopies']-1
                    cur.execute(f"update lib set noofcopies = {stock} where bookname='{user_book}'")
                    mydbl.commit()
                    message5='Subscription made!'
                    return render_template('issue.html', message=message5)

        else:
            message2='Enter Rollno.'
            return render_template('issue.html',message=message2)
    else:
        return render_template('issue.html')

@app.route('/return',methods=['POST','GET'])
def return_():
    if request.method == 'POST':
        rollno=request.form.get('rollno')
        if rollno:
            cur.execute(f"select Roll_no from subscription where Roll_no='{rollno}'")
            fetch_rollno=cur.fetchall()
            check=()
            if fetch_rollno == check:
                message='No book issued!!'
                return render_template('return.html',message=message)
            
            else:
                user_choice=request.form["choosebooks"]
                if user_choice == '1':
                    user_book = 'Maths'
                elif user_choice == '2':
                    user_book = 'Science'
                elif user_choice == '3':
                    user_book = 'Social Studies'
                elif user_choice == '4':
                    user_book = 'Computer SC.'
                else:
                    message2='Choose a book!'
                    return render_template('return.html', message=message2)
                cur.execute(f"select Roll_no from subscription where Roll_no='{rollno}' and bookname='{user_book}'")
                fetch_book=cur.fetchall()
                if fetch_book:
                    cur.execute(f"select noofcopies from lib where bookname='{user_book}'")
                    stock=cur.fetchone()
                    cur.execute(f"select Name from student where Roll_no='{rollno}'")
                    fetch_name=cur.fetchone()
                    fetch_name=fetch_name['Name']
                    stock=stock['noofcopies']+1
                    cur.execute(f'delete from subscription where Name="{fetch_name}" and Bookname="{user_book}" LIMIT 1')
                    mydbl.commit()
                    cur.execute(f'update lib set noofcopies=noofcopies+1 where bookname="{user_book}"')
                    mydbl.commit()
                    message3='Book Returned!!'
                    return render_template('return.html', message=message3)
                else:
                    message4='No book issued!!'
                    return render_template('return.html',message=message4)
        else:
            message5='Enter Rollno.'
            return render_template('return.html',message=message5)
    else:
        return render_template('return.html')


@app.route('/user')
def user_():
    return render_template('user.html')

@app.route('/user_details', methods=['POST','GET'])
def user_details():
    if request.method == 'POST':
        rollno = request.form.get('rollno3')
        rollno=[rollno]
        cur.execute(f"select Roll_no from subscription")
        fetch_all = cur.fetchall()
        print(rollno)
        data=[]
        for i in range(len(fetch_all)):
            data.append(f'{fetch_all[i]["Roll_no"]}')
        print(data)

        if rollno in data or rollno == data or rollno[0] in data:
            rollno=rollno[0]
            cur.execute(f"select bookname from subscription where Roll_no='{rollno}' and bookname='Maths'")
            maths_data=cur.fetchall()
            cur.execute(f"select bookname from subscription where Roll_no='{rollno}' and bookname='Science'")
            science_data=cur.fetchall()
            cur.execute(f"select bookname from subscription where Roll_no='{rollno}' and bookname='Social Studies'")
            ss_data=cur.fetchall()
            cur.execute(f"select bookname from subscription where Roll_no='{rollno}' and bookname='Computer SC.'")
            comp_data=cur.fetchall()
            cur.execute(f"select Name from student where Roll_no='{rollno}'")
            user_name=cur.fetchone()
            return render_template('user_details.html',rollno=rollno,name=user_name['Name'].capitalize(),maths_no=len(maths_data),science_no=len(science_data),ss_no=len(ss_data),comp_no=len(comp_data))
        elif rollno == ['']:
            message3='Enter Rollno!'
            return render_template('user.html', message2=message3)
        elif data == [] and rollno[0] != None:
            rollno=rollno[0]
            cur.execute(f"select Name from student where Roll_no='{rollno}'")
            user_name=cur.fetchone()
            maths_data=[]
            science_data=[]
            ss_data=[]
            comp_data=[]
            if user_name == None:
                message2='Rollno. not found in our database!'
                return render_template('user.html', message2=message2) 
            else:
                return render_template('user_details.html',rollno=rollno,name=user_name['Name'].capitalize(),maths_no=len(maths_data),science_no=len(science_data),ss_no=len(ss_data),comp_no=len(comp_data))
        else:
            message2='Contact dev'
            return render_template('user.html', message2=message2) 
    else:
        return index()

@app.route('/user/add_submit' , methods=['POST','GET'])
def user_addsubmit():
    if request.method == 'POST':
        name = request.form.get('name')
        rollno = request.form.get('rollno')
        cardno = request.form.get('cardno')
        if name and rollno and cardno:
            cur.execute(f"select Roll_no from student")
            fetch_one=cur.fetchall()
            fetch=[]
            for i in range(len(fetch_one)):
                fetch.append(fetch_one[i]['Roll_no'])
            if int(rollno) in fetch:
                message3='This Name/Rollno already exist!!'
                return render_template('user.html', message3=message3)
            else:
                cur.execute(f'insert into  student values({rollno},"{name}", {cardno})')
                mydbl.commit()
                status='user added'
                return render_template('user.html',message3=status)
        else:
            message3='Please enter all the details'
            return render_template('user.html', message3=message3)
    else:
        return render_template("index.html")

@app.route('/user/remsubmit', methods=['POST','GET'])
def user_remsubmit():
    stu_rollno = request.form.get('rollno2')
    cur.execute(f"SELECT * FROM student WHERE Roll_no = '{stu_rollno}'")
    result = cur.fetchone()
    if result:
        cur.execute(f"SELECT * FROM subscription WHERE Roll_no = '{stu_rollno}'")
        result1 = cur.fetchone()
        if result1:
            status="A book has already been issued by your end. Please return it first"
            return render_template("user.html", message=status)
        else:
            cur.execute(f"delete from student where Roll_no = '{stu_rollno}'")
            mydbl.commit()
            status='User Removed!!'
            return render_template("user.html", message=status)
    else:
        status="Your Roll no does not exist in our database"
        return render_template("user.html", message=status)

if __name__ == "__main__":
    app.run(debug=True)

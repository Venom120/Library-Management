# data to be entered in mysql database

import mysql.connector

mydb=mysql.connector.connect(host="localhost", user="root", password="root", database="little_world")
cur=mydb.cursor()

def commit():
    mydb.commit()

cur.execute("create table lib(bookname varchar(20), author varchar(20), publication varchar(20), noofcopies int(2))")
cur.execute("insert into lib values('Maths', 'RD_sharma', 'DhanpatRai', 5)")
cur.execute("insert into lib values('Science', 'Saxena', 'Arihant', 5)")
cur.execute("insert into lib values('Social studies', 'Oswald', 'Shukla', 5)")
cur.execute("insert into lib values('Computer SC.', 'Swati Arora', 'DhanpatRai', 5)")
commit()
cur.execute("create table student(Roll_no int(3), Name varchar(30), No_card int(3))")
commit()
cur.execute("create table subscription(Roll_no int(2), Name varchar(30), bookname varchar(20), Issue_date varchar(10))")
commit()

print("Tables created")
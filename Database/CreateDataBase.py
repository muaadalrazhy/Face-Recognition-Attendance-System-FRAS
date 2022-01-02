import mysql.connector

myDatabase = mysql.connector.connect (
    host="localhost",
    user="root",
    passwd="123456",
    database="FRAS"
)

mycursor = myDatabase.cursor()
# Create Database.
#mycursor.execute("CREATE DATABASE FRAS")

# Create HR "Admin" Table.
mycursor.execute("CREATE TABLE  HR (ID VARCHAR(255) PRIMARY KEY, Password VARCHAR(255), Name VARCHAR(255))")
# Create Attendance Table.
mycursor.execute("CREATE TABLE  Attendance (ID VARCHAR(255)  , Check_Date Date, Check_Time Time)")
# Create Employee Table.
mycursor.execute("CREATE TABLE  Employee (ID VARCHAR(255) PRIMARY KEY, Name VARCHAR(255) NOT NULL, Email VARCHAR(255) NOT NULL)")

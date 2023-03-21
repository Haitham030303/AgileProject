import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost", 
    user = "root",
    passwd = "password123",

)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE ")
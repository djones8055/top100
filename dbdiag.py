#!/usr/bin/env python3

import pymysql

print()
print("database diagnostic stuff...")
print()

dbusername = input("Username: ")
dbpassword = input("Password: ")
database = input("database: ")
dbhost = "djones8055.mysql.pythonanywhere-services.com"

print()
print("Connecting to: " , dbhost)
print("DB: " , database)
print("With username: " , dbusername , " and passowrd: ", dbpassword )
print()
print("..............")
print()

# open database connection 
db = pymysql.connect(dbhost, dbusername, dbpassword, database)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method
cursor.execute("SELECT VERSION()")

# fetch a single row using (fetchone() method
data = cursor.fetchone()
print("Database version : %s " % data)

# disconnect from server
db.close()
print()

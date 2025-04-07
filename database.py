import sqlite3

connection = sqlite3.connect('LoginData.db')
cursor = connection.cursor()

cmd1 = """CREATE TABLE IF NOT EXISTS USERS(
    first_name VARCHAR(50), 
    last_name VARCHAR(50),
    email VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50) NOT NULL
)"""

cursor.execute(cmd1)

cmd2 = """INSERT INTO USERS(first_name, last_name,email,password)values('tester', 'test', 'tester@gmail.com', 'tester')""" 
cursor.execute(cmd2)
connection.commit()

ans = cursor.execute("select * from USERS").fetchall()

for i in ans: 
    print(i)
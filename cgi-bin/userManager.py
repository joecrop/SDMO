import sqlite3 as lite
import sys
import datetime

SEX_M = 0
SEX_F = 1
db = 'data/meds.db'

def addUser(name, sex, weight, dob):
	con = None

	try:
		con = lite.connect(db)
		con.execute("INSERT INTO users(name, sex, weight, dob) values (?, ?, ?, ?)", (name ,sex, weight, dob))
		con.commit()

	except lite.Error:
		print("Error %s:" % e.args[0])
		sys.exit(1)
    
	finally:
		if con:
			con.close()

def updateUser(name, sex, weight, dob):
	con = None

	try:
		con = lite.connect(db)
		con.execute("UPDATE users SET name = ? AND sex = ? AND weight = ? AND dob = ? WHERE name = ?", (name ,sex, weight, dob, name))
		con.commit()

	except lite.Error:
		print("Error %s:" % e.args[0])
		sys.exit(1)
    
	finally:
		if con:
			con.close()



def getUsers():
	con = None
	rows = [] 
		
	try:
		con = lite.connect(db)
		cur = con.cursor()
		cur.execute("SELECT name, sex, weight, dob FROM users")
		rows = cur.fetchall()
		con.commit()
	
	except lite.Error:
		print("Error %s:" % e.args[0])
    	
	finally:
		if con:
			con.close()
			return rows



def createUserTable():
	con = None

	try:
		con = lite.connect(db)
    
		# id: 	unique id
		# sex: 0=male, 1=female
		# weight: integer in pounds
		# dob: unix date
		con.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, sex INT, weight INT, dob DATE)")
		con.commit()
    
	except lite.Error:
    
		print("Error %s:" % e.args[0])
		sys.exit(1)
    
	finally:
    
		if con:
			con.close()

#userM = userManager()
#userM.createUserTable()

#d = datetime.date(1982, 11, 23)
#userM.addUser("Amy", userM.SEX_F, 98, d)

#d = datetime.date(1985, 8, 13)
#userM.addUser("Joe", userM.SEX_M, 120, d)
	

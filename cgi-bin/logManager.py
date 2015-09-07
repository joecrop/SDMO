import sqlite3 as lite
import sys
import datetime

db = 'data/meds.db'

def addLog(dt, med_id, consumed, user):
	con = None

	try:
		con = lite.connect(db)
		con.execute("INSERT INTO log(datetime, med_id, consumed, user) values (?, ?, ?, ?)", (dt , med_id, consumed, user.strip()))
		con.commit()

	except lite.Error:
		print("Error %s:" % e.args[0])
		sys.exit(1)
    
	finally:
		if con:
			con.close()

def updateLog(dt, med_id, consumed, user, id):
	con = None

	try:
		con = lite.connect(db)
		con.execute("UPDATE log SET datetime = ? AND med_id = ? consumed = ? AND user = ? WHERE id = ?", (dt, med_id, consumed, user.strip(), id))
		con.commit()

	except lite.Error:
		print("Error %s:" % e.args[0])
		sys.exit(1)
    
	finally:
		if con:
			con.close()



def getLogs():
	con = None
	rows = [] 
		
	try:
		con = lite.connect(db)
		cur = con.cursor()
		cur.execute("SELECT id, datetime, med_id, user FROM log LIMIT 20 ORDER BY datetime DESC")
		rows = cur.fetchall()
		con.commit()
	
	except lite.Error:
		print("Error %s:" % e.args[0])
    	
	finally:
		if con:
			con.close()
			return rows

def getNewestLogById(med_id, user):
	con = None
	rows = [] 
		
	try:
		con = lite.connect(db)
		cur = con.cursor()
		cur.execute("SELECT id, datetime, med_id, user FROM log WHERE med_id = ? AND user LIKE ? ORDER BY datetime DESC LIMIT 1", (med_id, user.strip()))
		rows = cur.fetchall()
		con.commit()
	
	except lite.Error, e:
		print("Error %s:" % e.args[0])
    	
	finally:
		if con:
			con.close()
			return rows


def createLogTable():
	con = None

	try:
		con = lite.connect(db)
    
		# dob: unix date
		con.execute("CREATE TABLE log(id INTEGER PRIMARY KEY AUTOINCREMENT, datetime timestamp, med_id INT, consumed INT, user TEXT)")
		con.commit()
    
	except lite.Error, e:
    
		print("Error %s:" % e.args[0])
		sys.exit(1)
    
	finally:
    
		if con:
			con.close()

#createLogTable();	

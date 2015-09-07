import sqlite3 as lite
import sys
import datetime

db = 'data/meds.db'

def addSchedule(name, datetime, repeat, repeat_base, med, user, as_needed):
	con = None

	try:
		con = lite.connect(db)
		con.execute("INSERT INTO schedules(name, datetime, repeat, repeat_base, med, user, as_needed) values (?, ?, ?, ?, ?, ?, ?)", (name ,datetime, repeat, repeat_base, med, user, as_needed))
		con.commit()

	except lite.Error, e:
		print("Error in add")
		print "Error %s:" % e.args[0]
		sys.exit(1)
    
	finally:
		if con:
			con.close()

def updateSchedule(sid, name, datetime, repeat, repeat_base, med, user, as_needed):
	con = None

	try:
		con = lite.connect(db)
		con.execute("UPDATE schedules SET name = ? AND datetime = ? AND repeat = ? AND repeat_base = ? AND med = ? AND user = ? ANS as_needed = ? WHERE id = ?", (name ,datetime, repeat, repeat_base, med, user, as_needed, sid))
		con.commit()

	except lite.Error:
		print("Error in update")
		sys.exit(1)
    
	finally:
		if con:
			con.close()

def deleteSchedule(sid):
	con = None

	try:
		con = lite.connect(db)
		con.execute("DELETE FROM schedules WHERE id = ?", (sid,))
		con.commit()

	except lite.Error:
		print("Error in update")
		sys.exit(1)
    
	finally:
		if con:
			con.close()


def getSchedules():
	con = None
	rows = [] 
		
	try:
		con = lite.connect(db)
		cur = con.cursor()
		cur.execute("SELECT id, name, datetime, repeat, repeat_base, med, user, as_needed FROM schedules")
		rows = cur.fetchall()
		con.commit()
	
	except lite.Error:
		print("Error in get")
    	
	finally:
		if con:
			con.close()
			return rows



def createSchedulesTable():
	con = None

	try:
		con = lite.connect(db)
    
		# id: 	unique id
		# name: name of item (set by user)
		# datetime: unix timestamp for scheduled start time
		# repeat: number of times / base
		# repeat_base: 0=once, 1=hours, 2=days, 3=weeks, 4=months
		# med: med id
		# user: user name
		con.execute("CREATE TABLE schedules(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, datetime timestamp, repeat INT, repeat_base INT, med INT, user TEXT, as_needed INT)")
		con.commit()
    
	except lite.Error:
    
		print("Error in create")
		sys.exit(1)
    
	finally:
    
		if con:
			con.close()

#createSchedulesTable()

#d = datetime.datetime.now()
#addSchedule("Every 1 Hour Test", d, 1, 1, 2, "Amy")

#d = datetime.date(1985, 8, 13)
#userM.addUser("Joe", userM.SEX_M, 120, d)
	

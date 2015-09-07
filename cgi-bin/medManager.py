import sqlite3 as lite
import sys
import datetime

#class medManager:
db = 'data/meds.db'

def addMed(name, total):
	con = None

	try:
		con = lite.connect(db)
		cur = con.cursor()
		cur.execute("INSERT INTO meds(name, total) values (?, ?)", (name ,total))
		con.commit()
		lid = cur.lastrowid

	except lite.Error:
		print("Error %s:" % lite.Error.args[0])
    
	finally:
		if con:
			con.close()
			return lid

def deleteMed(id):
	con = None

	try:
		con = lite.connect(db)
		cur = con.cursor()
		cur.execute("DELETE FROM meds WHERE id = ?", (id,))
		con.commit()

	except lite.Error:
		print("Error %s:" % lite.Error.args[0])
    
	finally:
		if con:
			con.close()
			return 0



def getInventory(all):
	con = None
	rows = [] 
	
	try:
		con = lite.connect(db)
		cur = con.cursor()
		if(all):
			cur.execute("SELECT id, name, total FROM meds")
		else:
			cur.execute("SELECT id, name, total FROM meds WHERE total > 0")
		rows = cur.fetchall()
		con.commit()

	except lite.Error:
		print("Error %s:" % e.args[0])
    
	finally:
		if con:
			con.close()
			return rows


def addInventory(x, y, med, exp):
	con = None

	try:
		con = lite.connect(db)
		cur = con.cursor()
		#cur.execute("UPDATE inventory SET used = 1 AND med = ? AND exp = ? WHERE x = ? AND y = ?", (med, exp ,x, y))
		cur.execute("UPDATE inventory SET med = ? WHERE x = ? AND y = ?", (med, x, y))
		cur.execute("UPDATE inventory SET exp = ? WHERE x = ? AND y = ?", (exp, x, y))
		cur.execute("UPDATE inventory SET used = 1 WHERE x = ? AND y = ?", (x, y))
		cur.execute("UPDATE meds SET total = total+1 WHERE id = ?", (med,))
		con.commit()

	except lite.Error:
		print("Error %s:" % e.args[0])
    
	finally:
		if con:
			con.close()

def removeInventory(x, y):
	con = None

	try:
		con = lite.connect(db)
		cur = con.cursor()
		cur.execute("SELECT med FROM inventory WHERE x=? AND y=?", (x,y))
		con.commit()
		id = cur.fetchone()[0]
		print(id)
		#cur.execute("UPDATE inventory SET used = 0 AND med = 0 AND exp = 0 WHERE x = ? AND y = ?", (x, y))
		cur.execute("UPDATE inventory SET used = 0 WHERE x = ? AND y = ?", (x, y))
		cur.execute("UPDATE inventory SET med = 0 WHERE x = ? AND y = ?", (x, y))
		cur.execute("UPDATE inventory SET exp = 0 WHERE x = ? AND y = ?", (x, y))
		cur.execute("UPDATE meds SET total = total-1 WHERE id = ?", (id,))
		con.commit()

	except lite.Error:
		print("Error %s:" % e.args[0])
    
	finally:
		if con:
			con.close()

def getMedX(med):
	con = None

	try:
		con = lite.connect(db)
		cur = con.cursor()
		cur.execute("SELECT x FROM inventory WHERE med=?", (med,))
		con.commit()
		x = cur.fetchone()[0]

	except lite.Error:
		print("Error %s:" % e.args[0])
    
	finally:
		if con:
			con.close()
			return x

def getMedY(med):
	con = None

	try:
		con = lite.connect(db)
		cur = con.cursor()
		cur.execute("SELECT y FROM inventory WHERE med=?", (med,))
		con.commit()
		x = cur.fetchone()[0]

	except lite.Error:
		print("Error %s:" % e.args[0])
    
	finally:
		if con:
			con.close()
			return x



def getFreeSpaceX():
	con = None

	try:
		con = lite.connect(db)
		cur = con.cursor()
		cur.execute("SELECT x FROM inventory WHERE used=0")
		con.commit()
		x = cur.fetchone()[0]

	except lite.Error:
		print("Error %s:" % e.args[0])
    
	finally:
		if con:
			con.close()
			return x

def getFreeSpaceY():
	con = None

	try:
		con = lite.connect(db)
		cur = con.cursor()
		cur.execute("SELECT y FROM inventory WHERE used=0")
		con.commit()
		y = cur.fetchone()[0]

	except lite.Error:
		print("Error %s:" % e.args[0])
    
	finally:
		if con:
			con.close()
			return y



def createMedsTable():
	con = None

	try:
		con = lite.connect(db)
    
		# id: unique id (med ID)
		# mane: string for GUI
		# total: # of pills in machine
		con.execute("CREATE TABLE meds(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, total INT)")
		con.commit()
    
	except lite.Error:
		print("Error %s:" % e.args[0])
    
	finally:
		if con:
			con.close()



def createInventoryTable():
	con = None

	try:
		con = lite.connect(db)
   
		# x: which of 4 rings (0-3)
		# y: 16 positions per ring (0-15)
		# med: med ID
		# used: is it not empty?
		# exp: expiration date
		con.execute("CREATE TABLE inventory(x INT, y INT, med INT, used INT, exp DATE)")
		con.commit()
		for x in [0,1,2,3]:
			for y in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
				con.execute("INSERT INTO inventory(x, y, med, used) values (?, ?, ?, ?)", (x ,y, 0, 0))
		con.commit()
				
	except lite.Error:
		print("Error %s:" % lite.Error.args[0])
		sys.exit(1)
    
	finally:
		if con:
			con.close()


#createMedsTable()
#createInventoryTable()

#id = addMed("Tylenol", 0)
#id2 = addMed("Vitamin C", 0)
#print(id)
#print(id2)
#x = getFreeSpaceX()
#y = getFreeSpaceY()

#d = datetime.date(2016, 11, 23)
#addInventory(x, y, id, d)
#print("inserted into: ", x, y)

#x2 = getFreeSpaceX()
#y2 = getFreeSpaceY()
#addInventory(x2, y2, id2, d)
#print("inserted into: ", x2, y2)
#removeInventory(x, y)
#x = getFreeSpaceX()
#y = getFreeSpaceY()
#addInventory(x, y, id, d)
#print("inserted into: ", x, y)

#x = getFreeSpaceX()
#y = getFreeSpaceY()
#addInventory(x, y, id, d)
#print("inserted into: ", x, y)

#x = getFreeSpaceX()
#y = getFreeSpaceY()
#addInventory(x, y, id, d)
#print("inserted into: ", x, y)

#x = getFreeSpaceX()
#y = getFreeSpaceY()
#addInventory(x, y, id, d)
#print("inserted into: ", x, y)

	

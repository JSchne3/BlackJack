#!/usr/bin/env python3
#This Module is for reading and writing the Data from the wallet file.
import sys, traceback
import sqlite3
from contextlib import closing

dbfile = "bjgames.db"

class Session():
    def __init__(self, startTime, startMoney, addedMoney, stopTime, stopMoney):
        self.startTime = startTime
        self.startMoney = startMoney
        self.addedMoney = addedMoney
        self.stopTime = stopTime
        self.stopMoney = stopMoney

    def recordSession(self):
        try: 
            conn = sqlite3.connect(dbfile)
            with closing(conn.cursor()) as c:
                sql = '''INSERT INTO Session (startTime, startMoney, addedMoney, stopTime, stopMoney)
                         VALUES (?, ?, ?, ?, ?)'''
                c.execute(sql, (self.startTime, self.startMoney, self.addedMoney, self.stopTime, self.stopMoney))
                conn.commit()
            if conn:
                conn.close()
        except: 
            traceback.print_exc(file=sys.stdout)
            sys.exit("Failed to save Session Data, closing game.")

#loadWallet creates a loop after ordering the session data so that the last entry is always the starting point.
def loadWallet():
    startMoney = 0.0
    try: 
        conn = sqlite3.connect(dbfile)
        conn.row_factory = sqlite3.Row
        with closing(conn.cursor()) as c:
            sql = '''SELECT sessionID, stopMoney 
                     FROM Session 
                     ORDER BY sessionID ASC'''
            c.execute(sql)
            results = c.fetchall()
            for session in results:
                startMoney = session["stopMoney"]
        if conn:
            conn.close()
        return startMoney
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit("Fatal Error Loading Database, please restart the Program.")

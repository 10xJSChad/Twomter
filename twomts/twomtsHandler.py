from io import TextIOWrapper
import mysql.connector
from twomts import twomtsClass
from datetime import datetime

class twomtsHandler():
    def __init__(self, host, user, password, database, autocommit):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.autocommit = autocommit

        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            autocommit=self.autocommit 
        )
    
        self.cursor = self.db.cursor()

    def buildTwomt(self, twomt):
        builtTwomt = twomtsClass.twomt(twomt[0], twomt[1], twomt[2], twomt[3], twomt[4], twomt[5])
        return builtTwomt

    def getTwomts(self, filter=None, offset=0): #INCREASE LIMITS AND ADD 'SHOW MORE' BUTTONS
        if(filter == None):
            cmd = ("SELECT * FROM Twomts WHERE replyTo = -1 ORDER BY id DESC LIMIT 15 OFFSET %s")
            self.cursor.execute(cmd, (offset,))
        else:
            cmd = ("SELECT * FROM Twomts WHERE replyTo = -1 AND poster = %s ORDER BY id DESC LIMIT 15 OFFSET %s")
            self.cursor.execute(cmd, (filter, offset,))
            
        result = self.cursor.fetchall()
        twomtsToReturn = []
        for x in result: 
            builtTwomt = self.buildTwomt(x)
            cmd = ("SELECT * FROM Twomts WHERE replyTo = %s ORDER BY id DESC LIMIT 15")
            self.cursor.execute(cmd, (builtTwomt.id,))
            result = self.cursor.fetchall()
            for y in result: 
                builtTwomt.replies.append(self.buildTwomt(y))
            builtTwomt.replies.reverse()
            twomtsToReturn.append(builtTwomt)
        return twomtsToReturn

    def postTwomt(self, userID, content, replyTo, username):
        if(replyTo != -1):
            cmd = ("SELECT * FROM Twomts WHERE id = %s")
            self.cursor.execute(cmd, (replyTo, ))
            result = self.cursor.fetchall()
            if len(result) == 0: return

        cmd = "INSERT INTO twomts (poster, content, replyTo, username) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(cmd, (userID, content, replyTo, username))
    
    def deleteTwomt(self, id):
        cmd = "DELETE FROM twomts WHERE id=%s"
        self.cursor.execute(cmd, (id))
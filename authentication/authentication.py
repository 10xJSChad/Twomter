from io import TextIOWrapper
from authentication import userClass
import mysql.connector
import random

class auth():
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

  def getIpBan(self, ip):
    cmd = "SELECT * FROM ipbans WHERE ip=%s"
    self.cursor.execute(cmd, (ip,))
    result = self.cursor.fetchall()
    return len(result) > 0

  def updateUser(self, user):
    cmd = "UPDATE users SET username=%s, password=%s, ip=%s, token=%s, bio=%s WHERE username=%s"
    self.cursor.execute(cmd, (user.username, user.password, user.ip, user.token, user.bio, user.username, ))

  def generateToken(self):
      tokenChars = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
      rnd = random
      generatedToken = ""
      for x in range(0, 13):
          generatedToken += rnd.choice(tokenChars)
      return generatedToken

  def buildUser(self, result):
    if len(result) == 0: return None
    user = userClass.user(result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6])
    return user

  def getUserByName(self, username, returnUser=False):
    cmd = "SELECT * FROM users WHERE username=%s"
    self.cursor.execute(cmd, (username,))
    result = self.cursor.fetchall()
    if returnUser:
      user = self.buildUser(result)
      return user
    return(result)
    
  def getUserBySession(self, ip, token, returnUser=False):
    cmd = "SELECT * FROM users WHERE ip=%s AND token=%s"
    self.cursor.execute(cmd, (ip, token,))
    result = self.cursor.fetchall()
    if returnUser:
      user = self.buildUser(result)
      if user == None: return None
      if user.level == -1: return None
      if self.getIpBan(ip): return None
      if user.token == "NULL": return None
      return user
    return(result)

  def verifyLogin(self, username, password, ip):
    user = self.getUserByName(username, True)
    if user == None: return(False, "User does not exist")
    if user.level == -1: return(False, "User is banned")
    if self.getIpBan(ip): return(False, "User is banned")
    if user.username.lower() == username.lower() and user.password == password:
      user.ip = ip
      user.token = self.generateToken()
      self.updateUser(user)
      return(True, user)
    return(False, "Incorrect login information")

  def isUserLoggedIn(self, username, ip, token):
    user = self.getUserByName(username, True)
    if token == "NULL": return(False, "Token is null")
    if user == None: return(False, "User does not exist")
    if user.level == -1: return(False, "User is banned")
    if self.getIpBan(ip): return(False, "User is banned")
    if user.ip == ip and user.token == token: return(True, user)
    return(False, "No user found")

  def createUser(self, username, password, ip):
    if self.getIpBan(ip): return (False, 1)
    if self.getUserByName(username) == []:
      cmd = "INSERT INTO users (username, password, ip, token) VALUES (%s, %s, %s, %s)"
      self.cursor.execute(cmd, (username, password, "UNUSED", self.generateToken(),))
      return (True, 0)
    return (False, 0)
  
  def changeUserPassword(self, username, password, newPassword):
    user = self.getUserByName(username, True)
    if user != None:
      if user.password == password: user.password = newPassword; self.updateUser(user)
      
  def getIdFromUsername(self, username):
    cmd = "SELECT id FROM users WHERE username=%s"
    self.cursor.execute(cmd, (username,))
    result = self.cursor.fetchall()
    print(result)
    return int(result[0][0])

  def logUserOut(self, username):
    user = self.getUserByName(username, True)
    if user != None:
      user.token = "NULL"; self.updateUser(user)
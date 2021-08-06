import mysql.connector
import Config as config

db = mysql.connector.connect(
  host=config.host,
  user=config.user,
  password=config.password,
  database=config.database,
  autocommit=config.autocommit
)
cursor = db.cursor()
    
print("Connected to db  " + config.database)
print("Enter 'help' to see commands")
print("")

def printList(list):
    for x in list:
        print(x)

def lookup(user):
    cmd = "SELECT id, username, ip, bio FROM users WHERE username=%s"
    cursor.execute(cmd, (user,))
    result = cursor.fetchall()
    return result

def ban(user):
    cmd = "UPDATE users SET level=-1 WHERE username=%s"
    cursor.execute(cmd, (user,))
    result = cursor.fetchall()
    return "Command executed"

def unban(user):
    cmd = "UPDATE users SET level=0 WHERE username=%s"
    cursor.execute(cmd, (user,))
    result = cursor.fetchall()
    return "Command executed"

def banip(ip):
    cmd = "INSERT INTO ipbans (ip) VALUES (%s)"
    cursor.execute(cmd, (ip,))
    return "Command executed"

def unbanip(ip):
    cmd = "DELETE FROM ipbans WHERE ip=%s"
    cursor.execute(cmd, (ip,))
    return "Command executed"

def help():
    toReturn = ""
    for x in commands:
        toReturn += (x + ", ")
    return toReturn

#Commands
commands = {
  "lookup": lookup,
  "ban": ban,
  "unban": unban,
  "banip": banip,
  "unbanip": unbanip,
  "help": help,
}

def parseInput(command):
    command = command.split(" ")
    function = commands.get(command[0])
    if function != None:
        if len(command) > 1:
            return(function(command[1]))
        else: return(function())

while True:
    print(parseInput(input()))
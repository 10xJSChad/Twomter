import mysql.connector
from getpass import getpass

print("Twomter DB Creation")
print("-------------------")
print("This script will generate a ready-to-use Twomter SQL database")
print("You will need an SQL Server")
print("")
print("Enter 'Y' to Proceed")

userInput = ""
while userInput != "y":
    userInput = input().lower()
    if userInput == "n": exit()
    
host = input("Host: ")
user = input("User: ")
password = getpass("Password: ")

db = mysql.connector.connect(
  host=host,
  user=user,
  password=password
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE twomter")
db.database = 'twomter'

twomtsCreate = (
    "CREATE TABLE `twomts` ("
	"`id` INT(11) NOT NULL AUTO_INCREMENT,"
	"`poster` INT(11) NOT NULL,"
	"`content` VARCHAR(280) NOT NULL COLLATE 'utf8mb4_general_ci',"
	"`date` DATETIME NOT NULL DEFAULT current_timestamp(),"
	"`replyTo` INT(11) NULL DEFAULT NULL,"
	"`username` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',"
	"PRIMARY KEY (`id`) USING BTREE"
")"
)

usersCreate = (
    "CREATE TABLE `users` ("
	"`id` INT(11) NOT NULL AUTO_INCREMENT,"
	"`username` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',"
	"`password` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',"
	"`ip` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',"
	"`token` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',"
	"`bio` VARCHAR(150) NULL DEFAULT 'This user has not created a bio' COLLATE 'utf8mb4_general_ci',"
	"`level` INT(11) NULL DEFAULT '0',"
	"PRIMARY KEY (`id`) USING BTREE"
")"
)

ipbansCreate = (
	"CREATE TABLE `ipbans` ("
	"`ip` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci'"
")"
)
cursor.execute(twomtsCreate)
cursor.execute(usersCreate)
cursor.execute(ipbansCreate)

print("")
print("Twomter database successfully created")
input("")
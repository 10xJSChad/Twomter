<h2>Twomter</h2>
Twomter is a simple project made with the goal of creating a Twitter clone, but in the style of late-90s/early-2000s message and imageboards.
Unlike Twitter, you can not "re-tweet" posts, like posts, or follow other profiles.

Twomter is made with Flask and MariaDB on the backend, and vanilla HTML/CSS/JS on the frontend.

<h2>Features</h2>

* Finished posting system with timestamps & replies
* Profile page with customizable bio
* Client-side input validation for user convenience (server-side validation too, of course)
* Basic administrator console
* Basic password hashing & salting
* User and IP ban system
* Simple setup

<h2>Requirements</h2>

* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [mysql-connector](https://pypi.org/project/mysql-connector-python/)
* A MySQL Server (I used MariaDB)

<h2>Setting up Twomter</h2>

1. Clone this repository
2. Open Administration/Config.py and change the variables to match your SQL Server
3. Run and follow along with Administration/Create Database.py
4. Run app.py
5. Connect to localhost:5000 and you're good to go!

Once Twomter is set up, Administration/Console.py can be used to ban/unban users and IPs.

from flask import Flask, render_template, request, redirect, url_for, make_response
import sys
import mysql.connector
import Administration.Config as config
from authentication import authentication, simpleHashSalt, userClass
from twomts import twomtsHandler

app = Flask(__name__)
auth = authentication.auth(config.host, config.user, config.password, config.database, config.autocommit)
twomts = twomtsHandler.twomtsHandler(config.host, config.user, config.password, config.database, config.autocommit)

def verifyTwomt(twomt):
    if len(twomt.replace(" ", "")) == 0: return False
    if len(twomt) <= 140: return True
    return False

def verifyRegistration(username, password):
    if (len(username) < 4 or len(password) < 5):
        return(False, "Username or password too short!")
    if username == "None" or not username.isalnum(): return(False, "Invalid username") #Don't know if this is necessary, probably not
    if len(username) > 13: return(False, "Username is too long")
    return(True, "Registration success!")

def getUserCookies():
    username = request.cookies.get('username')
    ip = request.cookies.get('ip')
    token = request.cookies.get('token')
    return(username, ip, token)
    
def getUser():
    cookies = getUserCookies()
    return(auth.getUserBySession(cookies[1], cookies[2], True))

def isLoggedIn():
    userInfo = getUserCookies()
    if not auth.isUserLoggedIn(userInfo[0], userInfo[1], userInfo[2])[0]:
        return False
    return True

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/logout')
def logoutPage():
    if isLoggedIn():
        username = getUser().username
        auth.logUserOut(username)
    return index()

@app.route('/handle_login', methods=["POST"])
def handle_login(username=None, password=None):
    if(username==None): 
        username = request.values.get("username")
        password = simpleHashSalt.hash(request.values.get("password"))
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user = auth.verifyLogin(username, password, ip)
    if user[0] == True:
        user = user[1]
        resp = make_response(render_template('index.html', username=user.username, twomts=twomts.getTwomts(None, 0), offset=0))
        resp.set_cookie('username', user.username)
        resp.set_cookie('ip', user.ip)
        resp.set_cookie('token', user.token)
        return resp
    return render_template('login.html')

@app.route('/handle_twomt', methods=["POST"])
def handle_twomt():
    username = getUser().username
    content = request.values.get("twomt")
    replyTo = int(request.values.get("replyTo"))
    profileUsername = request.values.get("profileUsername")
    offset = 0
    if request.values.get('offset') != None:
        offset = int(request.values.get('offset'))
    if verifyTwomt(content): twomts.postTwomt(auth.getIdFromUsername(username), content, replyTo, username)
    if profileUsername != None:
        return(profile(profileUsername, offset))
    return index(offset)

@app.route('/get_more_twomts', methods=["POST"])
def get_more_twomts():
    offset = int(request.values.get('offset'))
    profileUsername = request.values.get('profileUsername')
    if profileUsername != None:
        return(profile(profileUsername, offset))
    return index(offset)

@app.route('/')
def index(offset=0):
    user = getUser()
    if user == None: username = None
    else: username = user.username
    twomtsToDisplay = twomts.getTwomts(None, offset)
    
    resp = make_response(render_template('index.html', username=username, twomts=twomtsToDisplay, offset=offset,))
    return resp

@app.route('/profile/<url>')
def profile(url, offset=0):
    if offset == None: offset = 0
    content = auth.getUserByName(url)

    user = getUser()
    if user == None: username = None
    else: username = user.username

    id = content[0][0]; profileUsername = content[0][1]; profileBio = content[0][5]
    twomtsToDisplay = twomts.getTwomts(id, offset)
    return render_template('/profile/profile.html', profileUsername=profileUsername, profileBio=profileBio, username=username, twomts=twomtsToDisplay, offset=offset)

@app.route('/profile/<url>/settings')
def profileSettings(url):
    user = getUser()
    if user == None or user.username != url: return(index())
    return render_template('/profile/profileSettings.html', username=user.username, bio=user.bio)

@app.route('/register')
def register():
    if isLoggedIn(): return index()
    return render_template('register.html', result=(True, "N/A"))

@app.route('/handle_registration', methods=["POST"])
def handle_registration():
    if isLoggedIn(): return index()
    username = request.values.get('username')
    password = request.values.get('password')
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    result = verifyRegistration(username, password)
    if result[0] == True: createUserResult = auth.createUser(username, simpleHashSalt.hash(password), ip)
    if not createUserResult[0]:
        failReasons = ["Username is already taken", "You are banned from Twomter"]
        print(createUserResult)
        result = (False, failReasons[createUserResult[1]])
    if result[0] == False:
        return render_template('register.html', result=result)
    else: return handle_login(username, simpleHashSalt.hash(password))

@app.route('/update_bio', methods=['POST'])
def update_bio():
    user = getUser()
    if user == None: return(index())
    newBio = request.values.get('twomt')
    user.bio = newBio
    auth.updateUser(user)
    return profile(user.username)

sys.path.append('/AnaAuth')
sys.path.append('/Twomts')
sys.path.append('/Administration')
app.run(),

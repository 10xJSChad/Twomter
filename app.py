from userClass import user
from flask import Flask, render_template, request, redirect, url_for, make_response
import sys
import mysql.connector
from AnaAuth import AnaAuth
from Twomts import twomtsHandler

app = Flask(__name__)
auth = AnaAuth.AnaAuthentication("localhost", "root", "", "twomter", True) 
twomts = twomtsHandler.twomtsHandler("localhost", "root", "", "twomter", True) 

def verifyTwomt(twomt):
    if len(twomt) <= 140: return True
    return False

def getUserCookies():
    username = request.cookies.get('username')
    ip = request.cookies.get('ip')
    token = request.cookies.get('token')
    return(username, ip, token)
    
def getUser():
    cookies = getUserCookies()
    return(auth.getUserBySession(cookies[1], cookies[2], True))

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/handle_login', methods=["POST"])
def handle_login():
    username = request.values.get("username")
    password = request.values.get("password")
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user = auth.verifyLogin(username, password, ip)
    if user[0] == True:
        resp = make_response(render_template('login_success.html'))
        user = user[1]
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
def index(offset=0): #ALLOW TO VIEW WITHOUT BEING LOGGED IN
    userInfo = getUserCookies()
    if not auth.isUserLoggedIn(userInfo[0], userInfo[1], userInfo[2])[0]:
        return render_template('login.html')

    user = getUser()
    twomtsToDisplay = twomts.getTwomts(None, offset)
    
    resp = make_response(render_template('index.html', username=user.username, twomts=twomtsToDisplay, offset=offset,))
    return resp

@app.route('/profile/<url>')
def profile(url, offset=0):
    if offset == None: offset = 0
    content = auth.getUserByName(url)
    userInfo = getUserCookies()
    if auth.isUserLoggedIn(userInfo[0], userInfo[1], userInfo[2])[0]:
        user = getUser()
        username = user.username
    id = content[0][0]; profileUsername = content[0][1]; profileBio = content[0][5]
    twomtsToDisplay = twomts.getTwomts(id, offset)
    return render_template('/profile/profile.html', profileUsername=profileUsername, profileBio=profileBio, username=username, twomts=twomtsToDisplay, offset=offset)
    
sys.path.append('/AnaAuth')
sys.path.append('/Twomts')
app.run(),

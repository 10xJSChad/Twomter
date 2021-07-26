import hashlib
import config

def hash(password):
    #This is very weak
    result = hashlib.md5(password.encode())
    result = result.hexdigest()
    result += config.passwordSalt
    result = hashlib.md5(result.encode())
    return(result.hexdigest())

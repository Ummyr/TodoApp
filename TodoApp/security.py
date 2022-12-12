''' flask_httpauth and werkzeug module '''
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

fernet = Fernet(b'YXQVEB5f_Pulby5C4LZ19R6GHqZby6DqRK9eBN779wg=')
auth = HTTPBasicAuth()

USER = {
    'admin': generate_password_hash('password')
}

@auth.verify_password
def verify_password(username, password):
    ''' verifies password and username'''
    if username in USER and check_password_hash(USER[username], password):
        return username
    return None

def encrypt_data(val):
    ''' encrypts data '''
    return fernet.encrypt(str(val).encode('utf-8')).decode('utf-8')

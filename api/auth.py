import sqlite3, flask, werkzeug.security, re, random, base64, uuid, time
from flask import request, make_response, Flask, Blueprint

from db.database import database

app=Blueprint('auth', __name__, url_prefix='/api/account')

def check_token(token):
    cursor = database.cursor()
    cursor.execute(f"SELECT * from DATA where AUTH = '{token}'")
    fetched = cursor.fetchone()
    return fetched

def decrypt(password):
    encryption = password[0]
    password = password[1]
    #if encryption == '0':
        ## do nothing
    return [encryption, password]

@app.route('signup', methods=['POST'])
def signup():
    if request.is_json:
        data = request.json
        if data.get('username') and data.get('password'):
            password = re.findall(r'(_\|)(.*)(\|)(.*)', data['password'])[0]
            username = data['username']
            if len(password) != 4:
                return 'Invalid password structure', 400
            else:
                password = decrypt([password[3], password[1]])
                if username.isalnum() == False:
                    return 'Username can only contain alphanumeric letters', 400
                if len(username) < 3 or len(username) > 24:
                    return 'Username either too short or too long. max 24, min 3', 400
                cursor = database.cursor()
                cursor.execute(f"SELECT COUNT(*) from DATA where USERNAME = '{username}'")
                if cursor.fetchone()[0] > 0:
                    return 'Username is already taken', 400
                password = werkzeug.security.generate_password_hash(password[1])
                cursor = database.cursor()
                userid = random.randint(int('1'+'1'*17),int('9'+'9'*17))
                while True:
                    cursor.execute(f"SELECT COUNT(*) from DATA where USERID == '{userid}'")
                    if cursor.fetchone()[0] > 0:
                        userid = random.randint(int('1'+'1'*17),int('9'+'9'*17))
                    else:
                        break
                cursor = database.cursor()
                token = base64.b64encode(str(userid).encode("ascii")).decode("ascii")+'.'+base64.b64encode(str(time.time()).encode("ascii")).decode("ascii")+'.'+base64.b64encode(str(uuid.uuid1()).encode("ascii")).decode("ascii")
                response = make_response('Account successfully created!')
                response.status_code = 201
                response.set_cookie('.SECURITY', token)
                cursor.execute(f'INSERT INTO DATA VALUES ({userid}, "{username}", NULL, NULL, "{password}", "{token}", "USER");')
                database.commit()
                return response
        else:
            return 'Invalid data', 406
    else:
        return 'Request is supposed to be JSON.', 400

@app.route('signin', methods=['POST'])
def login():
    if request.is_json:
        data = request.json
        if data.get('username') and data.get('password'):
            try:
                password = re.findall(r'(_\|)(.*)(\|)(.*)', data['password'])[0]
            except:
                return 'Invalid password structure', 400
            username = data['username']
            if len(password) != 4:
                return 'Invalid password structure', 400
            else:
                password = decrypt([password[3], password[1]])
                try:
                    if username.isalnum() == False:
                        return 'Invalid username or password', 400
                    if len(username) < 0:
                        return 'Invalid username or password', 400
                    cursor = database.cursor()
                    cursor.execute(f"SELECT COUNT(*) from DATA where USERNAME = '{username}'")
                    if cursor.fetchone()[0] == 0:
                        return 'Invalid username or password', 400
                    cursor = database.cursor()
                    cursor.execute(f"SELECT * from DATA where USERNAME = '{username}'")
                    fetched = cursor.fetchone()
                    if werkzeug.security.check_password_hash(fetched[4], password[1]):
                        response = make_response('Signed in')
                        response.status_code = 200
                        response.set_cookie('.SECURITY', fetched[5])
                        return response
                    else:
                        return 'Invalid username or password', 400
                except Exception as e:
                    print(e)
                    return 'Invalid username or password', 500
        else:
            return 'Invalid data', 406
    else:
        return 'Request is supposed to be JSON.', 400


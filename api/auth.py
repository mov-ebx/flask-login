import sqlite3, flask, werkzeug.security, re, random, base64, uuid, time
from flask import request, make_response, Flask, Blueprint

from utils.database import database
from utils.email import send_email

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

@app.route('emailverify', methods=['POST'])
def emailverify():
    if request.is_json:
        data = request.json
        check = check_token(request.cookies.get('.SECURITY'))
        if data.get('code') and check != None:
            if check[7] == data.get('code'):
                cursor = database.cursor()
                cursor.execute(f'UPDATE DATA SET VERIFIED = 1 WHERE AUTH = \'{request.cookies.get(".SECURITY")}\'')
                database.commit()
                return 'Verified', 200
            return 'Invalid code', 400
    return 'Forbidden', 403

@app.route('resendverify', methods=['POST'])
def resendverify():
    check = check_token(request.cookies.get('.SECURITY'))
    if check != None:
        send_email(check[3], 'Verification', f'If you aren\'t trying to verify, ignore this.\n\nVerification code: {check[7]}')
        return 'Resent', 200
    return 'Forbidden', 403

@app.route('resetpassword', methods=['POST'])
def resetpassword():
    if request.is_json:
        data = request.json
        if data.get('email'):
            cursor = database.cursor()
            cursor.execute(f"SELECT * from DATA where EMAIL = '{data['email']}'")
            check = cursor.fetchone()
            verify = 'http://0.0.0.0:5000/reset?id='+str(check[0])+'&token='+check[5].split('.')[2]
            send_email(check[3], 'Password reset', f'If you aren\'t trying to reset your password, ignore this.\n\nReset here: {verify}')
            return 'Reset sent', 200
    return 'Invalid reset request', 400

@app.route('resetconfirm', methods=['POST'])
def resetconfirm():
    if request.is_json:
        data = request.json
        if data.get('id') and data.get('token') and data.get('password'):
            try:
                password = re.findall(r'(_\|)(.*)(\|)(.*)', data['password'])[0]
                if len(password) != 4:
                    return 'Invalid password structure', 400
                else:
                    cursor = database.cursor()
                    cursor.execute(f"SELECT * from DATA where USERID = '{data['id']}'")
                    check = cursor.fetchone()
                    if check[5].split('.')[2] == data['token']:
                        password = decrypt([password[3], password[1]])
                        cursor = database.cursor()
                        token = base64.b64encode(str(data["id"]).encode("ascii")).decode("ascii")+'.'+base64.b64encode(str(time.time()).encode("ascii")).decode("ascii")+'.'+base64.b64encode(str(uuid.uuid1()).encode("ascii")).decode("ascii")
                        cursor.execute(f'UPDATE DATA SET AUTH = \'{token}\' WHERE USERID == \'{str(data["id"])}\'')
                        password = werkzeug.security.generate_password_hash(password[1])
                        cursor.execute(f'UPDATE DATA SET PASSWORD = \'{password}\' WHERE USERID == \'{str(data["id"])}\'')
                        database.commit()
                        response = make_response('Password reset!')
                        response.status_code = 201
                        response.set_cookie('.SECURITY', token)
                        return response
            except:
                pass
    return 'Invalid reset request', 403 

@app.route('signup', methods=['POST'])
def signup():
    if request.is_json:
        data = request.json
        if data.get('username') and data.get('password') and data.get('email'):
            password = re.findall(r'(_\|)(.*)(\|)(.*)', data['password'])[0]
            username = data['username']
            email = data['email']
            if len(password) != 4:
                return 'Invalid password structure', 400
            else:
                password = decrypt([password[3], password[1]])
                if username.isalnum() == False:
                    return 'Username can only contain alphanumeric letters', 400
                if len(username) < 3 or len(username) > 24:
                    return 'Username either too short or too long. max 24, min 3', 400
                if len(re.findall(r'[a-z,A-Z,0-9,.,@,+]', email)) != len(email):
                    return 'Invalid characters in email', 400
                if not ('@' and '.' in email):
                    return 'Invalid email', 400 
                cursor = database.cursor()
                cursor.execute(f"SELECT COUNT(*) from DATA where USERNAME = '{username}'")
                if cursor.fetchone()[0] > 0:
                    return 'Username is already taken', 400
                cursor = database.cursor()
                cursor.execute(f"SELECT COUNT(*) from DATA where EMAIL = '{email}'")
                if cursor.fetchone()[0] > 0:
                    return 'Email is already taken', 400
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
                code = str(random.randint(100000, 999999))
                cursor.execute(f'INSERT INTO DATA VALUES ({userid}, "{username}", NULL, "{email}", "{password}", "{token}", "USER", {code}, 0);')
                database.commit()
                send_email(email, 'Verification', f'If you aren\'t trying to verify, ignore this.\n\nVerification code: {code}')
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
                    if len(re.findall(r'[a-z,A-Z,0-9,.,@,+]', username)) != len(username):
                        return 'Invalid username or password', 400
                    if len(username) < 0:
                        return 'Invalid username or password', 400
                    cursor = database.cursor()
                    cursor.execute(f"SELECT * from DATA where USERNAME = '{username}'")
                    fetched = cursor.fetchone()
                    if fetched == None:
                        cursor = database.cursor()
                        cursor.execute(f"SELECT * from DATA where EMAIL = '{username}'")
                        fetched = cursor.fetchone()
                    if fetched != None and werkzeug.security.check_password_hash(fetched[4], password[1]):
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


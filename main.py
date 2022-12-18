import flask, os
from flask import request, Flask, Blueprint, redirect, render_template
from api.auth import check_token

app=Flask(__name__)
for file in os.listdir('api'):
    if file.endswith('.py'):
        app.register_blueprint(__import__('api.'+file[:-3], fromlist=[None]).app)
for file in os.listdir('dash'):
    if file.endswith('.py'):
        app.register_blueprint(__import__('dash.'+file[:-3], fromlist=[None]).app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/login')
@app.route('/signup')
@app.route('/access')
def register():
    if check_token(request.cookies.get('.SECURITY')) == None:
        return app.send_static_file('access.html')
    return redirect('/verify')

@app.route('/verify')
def verify():
    check = check_token(request.cookies.get('.SECURITY'))
    if check == None:
        return redirect('/access')
    if check[8] == 0:
        return app.send_static_file('verify.html')
    return redirect('/dashboard')

if __name__=='__main__':
    if not os.path.isdir('secrets'):
        os.mkdir('secrets')
    if not os.path.isfile('secrets/SendGridAPI'):
        open('secrets/SendGridAPI', 'w').write(input('Enter your SendGrid API key: '))
    if not os.path.isfile('secrets/SendGridEMAIL'):
        open('secrets/SendGridEMAIL', 'w').write(input('Enter your SendGrid Email: '))
    app.run(debug=True, port=5000)

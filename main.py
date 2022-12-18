import flask, os
from flask import request, Flask, Blueprint, redirect, render_template
from api.auth import check_token

app=Flask(__name__)
for file in os.listdir(os.path.dirname(__file__)+'/api'):
    if file.endswith('.py'):
        app.register_blueprint(__import__('api.'+file[:-3], fromlist=[None]).app)
for file in os.listdir(os.path.dirname(__file__)+'/dash'):
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
    return redirect('/dashboard')

if __name__=='__main__':
    app.run(debug=True, port=80)

from flask import request, render_template, redirect, Blueprint
from api.auth import check_token

app=Blueprint('dashboard', __name__,)

@app.route('/dashboard')
def dashboard():
    if check_token(request.cookies.get('.SECURITY')) == None:
        return redirect('access')
    return render_template('dashboard.html')

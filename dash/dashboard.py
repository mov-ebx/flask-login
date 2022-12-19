from flask import request, render_template, redirect, Blueprint
from api.auth import check_token

app=Blueprint('dashboard', __name__,)

@app.route('/dashboard')
def dashboard():
    check = check_token(request.cookies.get('.SECURITY'))
    if check == None:
        return redirect('access')
    return render_template('dashboard.html', username=check[1])

import utils.database
from flask import request, Blueprint

from api.auth import check_token

app=Blueprint('admin', __name__,)

@app.route('/api/admin/reset')
def reset():
    try:
        check = check_token(request.cookies.get('.SECURITY'))
        if check[6] == 'ADMIN':
            db.database.reset()
            return 'Reset database.', 201
    finally:
        return 'Insufficient perms', 403
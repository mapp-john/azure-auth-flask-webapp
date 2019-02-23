import os, json, uuid
from flask import *
from functools import wraps

##########################################
#
# Flask App Config
app = Flask(__name__)
app.debug = True
app.secret_key = str(uuid.uuid4())
app.url_map.strict_slashes = False # Disable redirecting on POST method from /star to /star/
#
#
###################################################
#
# Azure AD Roles
AllUsers = [
        'AppAdmin',
        'AppPrivUser',
        'AppUser',
        ]
#
# Login Decorators
def login_group_required(authlist):
    def decorated_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check for user against list
            ValidUser = any(role in request.headers['Oidc-Claim-Roles'] for role in authlist)
            # Check User Access
            if ValidUser:
                return f(*args, **kwargs)
            elif not ValidUser:
                return unauthorized()
            return f(*args, **kwargs)
        return wrapper
    return decorated_function
#
#
###################################################
# Routes
#
@app.route('/')
def hello_world():
    return 'Welcome anonymous<br><a href="/web/data">Data</a><br><a href="/web/private">Private</a><br><a href="/web/admin">Admin</a>'
#
#
@app.route('/data')
@login_group_required(AllUsers)
def hello_auth():
    return ('Hello! You are seeing Authorized data!<br><a href="/web/">Return</a>')
#
#
@app.route('/private')
@login_group_required(['AppAdmin','AppPrivUser'])
def hello_priv():
    return ('Hello! You are seeing Privileged data!<br><a href="/web/">Return</a>')
#
#
@app.route('/admin')
@login_group_required(['AppAdmin'])
def hello_admin():
    return ('Hello! You are seeing Admin data!<br><a href="/web/">Return</a>')
#
#

#
#
###################################################
# Run from all IPs
if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0', port=8080)

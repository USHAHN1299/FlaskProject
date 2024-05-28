# import json
# from flask import Flask, render_template, request, redirect, url_for, session
# import re

# app = Flask(__name__)


# # Load existing users from file
# def load_users():
#     try:
#         with open('users.json', 'r') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return {}

# # Save users to file
# def save_users(users):
#     with open('users.json', 'w') as f:
#         json.dump(users, f)
#     f.close()

# # Load users at the start of the server
# users = load_users()
# @app.route('/')
# def index():
#     return render_template('login.html')

# @app.route('/login', methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if len(users) > 0:
#             for i in range(1, len(users)+1):
#                 account = users.get(f"id_{i}")
#                 if account.get("username") == username:
#                     if account.get("username") and account.get("password") == password:
#                         # Valid credentials, redirect to success page or do something else
#                         # msg = "Login successful"
#                         session['username'] = username
#                         return redirect(url_for('data_app.data_upload'))
#                     else:
#                         # Invalid credentials, show error message
#                         return render_template('login.html', msg= "Invalid username or password")
#         else:
#             return render_template('login.html', msg = "User not present")
                
#     return render_template('login.html', msg = '')
        


# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))

# @app.route('/register', methods =['GET', 'POST'])
# def register():
#     msg = ''
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         account_exists = False
#         for i in range(1, len(users)+1):
#             account = users.get(f"id_{i}")
#             if account.get("email") == email or account.get("username") == username and account.get("password") == password:
#                 account_exists = True
#                 break
#         if account_exists:
#             msg = 'Account already exists !'
#         else:
#             if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#                 msg = 'Invalid email address !'
#             elif not re.match(r'[A-Za-z0-9]+', username):
#                 msg = 'Username must contain only characters and numbers !'
#             elif not username or not password or not email:
#                 msg = 'Please fill out the form !'
#             else:
#                 users.update({f"id_{len(users)+1}":{"username":username, "password":password,"email":email}})
#                 save_users(users)
#                 msg = 'You have successfully registered !'
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#     return render_template('register.html', msg = msg)

# # @app.route("/forgot_password", methods=['POST'])
# # def forgot_password():
# #     msg = ''
# #     if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
# #         email = request.form['email']
# #         password = request.form['password']
# #         new_password = request.form['new password']
# #         password = request.form['password-verfy']
# #         account_exists = False
# #         for i in range(1, len(users)+1):
# #             account = users.get(f"id_{i}")
# #             if account.get("email") == email:
# #                 users.update({f"id_{i}":{"username":account.get("username"), "password":new_password,"email":email}})
# #                 account_exists = True
# #                 break
    
    

# if __name__ == '__main__':
#     app.run()

# auth_app.py
import json
from flask import Blueprint, render_template, request, redirect, url_for, session
import re

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates', static_folder='static')

# Load existing users from file
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save users to file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

# Load users at the start of the server
users = load_users()

@auth_bp.route('/')
def index():
    return render_template('login.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if len(users) > 0:
            for i in range(1, len(users) + 1):
                account = users.get(f"id_{i}")
                if account.get("username") == username:
                    if account.get("username") and account.get("password") == password:
                        session['username'] = username
                        return redirect(url_for('data_app.data_upload'))  # Redirect to data upload page
                    else:
                        return render_template('login.html', msg="Invalid username or password")
        else:
            return render_template('login.html', msg="User not present")
    return render_template('login.html', msg='')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth_bp.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account_exists = False
        for i in range(1, len(users) + 1):
            account = users.get(f"id_{i}")
            if account.get("email") == email or (account.get("username") == username and account.get("password") == password):
                account_exists = True
                break
        if account_exists:
            msg = 'Account already exists!'
        else:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                users.update({f"id_{len(users) + 1}": {"username": username, "password": password, "email": email}})
                save_users(users)
                msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)



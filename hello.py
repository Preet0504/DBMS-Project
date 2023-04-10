from flask import Flask, render_template, request, redirect, url_for, session
import re
import cx_Oracle
con = cx_Oracle.connect('c##preet/oracle@DESKTOP-PEKHAL8:1521/orcl21c')
app = Flask(__name__,template_folder="template")
app.secret_key = ' key'
app.static_folder='static'
@app.route("/")
def first():
    return render_template('first.html')
@app.route("/login/", methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    session={}
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cursor = con.cursor()
        cursor.execute('SELECT * FROM form WHERE username = :username AND password = :password',{"username": username, "password": password})
        account = cursor.fetchone()
        
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            if 'loggedin' in session:
        # User is loggedin show them the home page
                return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
            return redirect(url_for('login'))
        else:
        # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template("login.html",msg=msg)
@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))
@app.route('/register/', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'age' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        dob = request.form['dob']
        # Check if account exists using MySQL
        cursor = con.cursor()
        cursor.execute('SELECT * FROM form WHERE username = :username OR email = :email',{"username": username,"email":email})
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'[0-120]+', dob):
            msg = 'Invalid age'
        elif not username or not password or not email or not dob:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO form VALUES (:username, :password, :email,:dob)', {"username":username,"password": password,"email": email,"dob":dob})
            con.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

app.debug = True
app.run()
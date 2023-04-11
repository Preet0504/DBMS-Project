from flask import Flask, render_template, request, redirect, url_for, session
import re
import cx_Oracle
# dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl')
con = cx_Oracle.connect('aagam123/aagam123@Aagam:1521/xe')
app = Flask(__name__,template_folder="templates")
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
                # return render_template('home.html', username=session['username'])
                return redirect(url_for('home'))
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
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'dob' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        d = request.form['dob']
        aa=d.split("-")
        month={1:"JAN",2:"FEB",3:"MAR",4:"APR",5:"MAY",6:"JUN",7:"JULY",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"}
        dob=month[int(aa[1])]+'-'+aa[2]+'-'+aa[0]
        
        print(dob)
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

@app.route("/home/")
def home():
    return render_template("home.html")
# Search Function
def getMovies(search):
    con = cx_Oracle.connect('aagam123/aagam123@Aagam:1521/xe')
    cursor = con.cursor()
    cursor.execute("Select * from movies where title ilike :search or genre ilike :search",('%'+search+'%','%'+search+'%',))
    results = cursor.fetchall()
    con.close()
    return results

@app.route("/search/", methods=['GET', 'POST'])
def search_result():
    if request.method=="POST":
        data = request.form['search']
        print(data)
        users = getMovies(data)
        print(users)
    else:
        users = []
    return render_template("search.html",usr=users)

app.debug = True
app.run()

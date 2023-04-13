from flask import Flask, render_template, request, redirect, url_for, session
import re
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
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
        elif not username or not password or not email or not dob:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO form VALUES (:username, :password, :email,:dob)', {"username":username,"password": password,"email": email,"dob":dob})
            con.commit()
            con.close()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
@app.route('/home/')
def home():
    return render_template("home.html")
def getMovies(search):
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    cursor = con.cursor()
    search = search.lower()
    cursor.execute("Select * from movies where lower(title) like :search or genre like :search",('%'+search+'%','%'+search+'%'))
    results = cursor.fetchall()
    print(results,"xyz")
    con.close()
    return results

@app.route("/search/", methods=['GET', 'POST'])
def search_result():
    col = ["Movie id:   ","Title:   ","Movie Description:   ","Duration:   ","Language:   ","Release Date:   ","Genre:   "]
    if request.method=="POST":
        data = request.form['search']
        print(data)
        users = getMovies(data)
        print(users)
        

    else:
        users = []
    return render_template("search.html",usr=users)
def filter(data):
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    cursor = con.cursor()
    data1=""
    for i in data:
        if(i==data[0] ):
            if (len(data)>1):
                data1="'"+i+"'"+","
            else:
                data1="'"+data[0]+"'"
        elif(i==data[-1]):
            data1=data1+"'"+i+"'"
        else:
            data1=data1+"'"+i+"'"+","
    print(data1)
    cursor.execute("Select * from movies where genre in ("+data1+")")
    results = cursor.fetchall()
    con.close()
    return results

@app.route("/filter/",methods=['GET','POST'])
def filter_result():
    if request.method=="POST":
        data = request.form.getlist('mycheckbox')
        print(data)
        users = filter(data)
    else:
        users = []
    return render_template("filter.html",usr=users)


def cinema(data):
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    cursor = con.cursor()
    cursor.execute('select * from shows where movie_id ='+ data)
    results = cursor.fetchall()
    con.close()
    print(results)
    return results
@app.route("/cinema/",methods=['GET','POST'])
def select_cinema():

    data= request.args.get('data')
    print(data)
    data1=cinema(data)
    return render_template('cinema.html',dt=data1)
        
app.debug = True
app.run()

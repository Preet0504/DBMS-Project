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
    print("hi")
    try:
        msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'dob' in request.form:
        # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            d = request.form['dob']
            print(d)
            aa=d.split("-")
            month={1:"JAN",2:"FEB",3:"MAR",4:"APR",5:"MAY",6:"JUN",7:"JULY",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"}
            dob=aa[2]+'-'+month[int(aa[1])]+'-'+aa[0]
            print(dob)
        # Check if account exists using MySQL
            cursor = con.cursor()
            cursor.execute('SELECT * FROM form WHERE username = :username OR email = :email',{"username": username,"email":email})
            account = cursor.fetchone()
        # If account exists show error and validation checks
            
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
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
    
    except Exception as e:
        
        return render_template('error.html',message=str(e))

@app.route('/error')  
def error(message):
    return render_template('error.html',message=message)
@app.route('/home/')
def home():
    return render_template("home.html")
def getMovies(search):
    con = cx_Oracle.connect('c##preet/oracle@DESKTOP-PEKHAL8:1521/orcl21c')
    cursor = con.cursor()
    search = search.lower()
    cursor.execute("Select * from movies where lower(title) like :search or genre like :search",('%'+search+'%','%'+search+'%'))
    results = cursor.fetchall()
    print(results)
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
def filter(data1,data2,data3=None):
    con = cx_Oracle.connect('c##preet/oracle@DESKTOP-PEKHAL8:1521/orcl21c')
    cursor = con.cursor()
    datax=""
    for i in data1:
        if(i==data1[0] ):
            if (len(data1)>1):
                datax="'"+i+"'"+","
            else:
                datax="'"+data1[0]+"'"
        elif(i==data1[-1]):
            datax=datax+"'"+i+"'"
        else:
            datax=datax+"'"+i+"'"+","
    print(datax)
    datay = ""
    for i in data2:
        if(i==data2[0] ):
            if (len(data2)>1):
                datay="'"+i+"'"+","
            else:
                datay="'"+data2[0]+"'"
        elif(i==data2[-1]):
            datay=datay+"'"+i+"'"
        else:
            datay=datay+"'"+i+"'"+","
    query = "SELECT * FROM movies WHERE "
    if datax:
        query += "genre IN ( " +datax +')'
        
    if datay:
        if data1:
            query +=' AND '
        query += "lower(lang) IN ('" + "','".join(data2) + "')"


        print(data2)
        
    if data3:
        if datax or datay:
            query += " AND "
        available_time = "SELECT movie_id  FROM shows WHERE show_time = '"+ data3 +"'"
        query += "movie_id IN ( " + available_time + ")"
    print("This is the query here:",query)
    cursor.execute(query)
    results = cursor.fetchall()
    con.close()
    return results

@app.route("/filter/",methods=['GET','POST'])
def filter_result():
    if 'time' in request.form:
        data3 = request.form['time']
        print(data3)
    else:
        data3 = None
    if request.method=="POST":
        data1,data2 = request.form.getlist('mycheckbox'),request.form.getlist('mycheckbox1')
        # print(data1,data2)
        users = filter(data1,data2,data3)
    else:
        users = []
    return render_template("search.html",usr=users)


def cinema(data):
    con = cx_Oracle.connect('c##preet/oracle@DESKTOP-PEKHAL8:1521/orcl21c')
    cursor = con.cursor()
    cursor.execute('select cinema_id from shows where movie_id = :data' ,(data,))
    results = cursor.fetchall()
    print(results)
    result=[]
    for i in results:
        cursor.execute('select city from cinema where cinema_id in :results',(i))
        res= cursor.fetchone()
        result.append(res)
    con.close()
    result=set(result)
    print(result)
    return result
@app.route("/cinema/",methods=['GET','POST'])
def select_cinema():

    data= request.args.get('data')
    print(data)
    data1=cinema(data)
    return render_template('cinema.html',dt=data1,dt2=data)

@app.route("/image/")
def image_result():
    image_id = request.args.get('data')
    print(image_id)
    print(type(image_id))
    con = cx_Oracle.connect('c##preet/oracle@DESKTOP-PEKHAL8:1521/orcl21c')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM movies WHERE title LIKE :image_id", ('%'+image_id+'%',))
    result = cursor.fetchall()
    print(result)
    return render_template("search.html",usr=result)
@app.route("/shows/",methods = ['GET','POST'])
def shows():
    city=request.form['mycity']
    city=city.split(",")
    print(city[0])
    print(city[1])
    con = cx_Oracle.connect('c##preet/oracle@DESKTOP-PEKHAL8:1521/orcl21c')

    cursor=con.cursor()
    query = """
        SELECT DISTINCT s.show_time, c.cinema_name
        FROM cinema c
        JOIN shows s ON s.cinema_id = c.cinema_id
        JOIN movies m ON m.movie_id = s.movie_id
        WHERE c.city = :city AND m.movie_id = :movie_id
    """
    cursor.execute(query, {'city': city[0], 'movie_id': city[1]})
    result = cursor.fetchall()
    print(result)
    return render_template('shows.html',ct=result)

app.debug = True
app.run()

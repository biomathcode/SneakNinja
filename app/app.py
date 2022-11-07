from flask import Flask, render_template, request, session, redirect, jsonify
from dbconnector import connectToS2MS
from flask_cors import CORS, cross_origin

from uuid import uuid4
app = Flask(__name__)
cors = CORS(app)
app.secret_key = 'keep it secret, keep it safe'

db = 'sneakninja'


@app.route('/')
def index():
    print("in the index method")
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    s2ms = connectToS2MS(db)
    # *** REGISTRATION 1 ***
    # Check Email To See If It Already Exists - Retrieve a User Using the Provided Email
    query = "SELECT * FROM users where email = %(email)s"
    data = {"email": request.form['Email']}
    UserExist = s2ms.query_db(query, data)

    if UserExist == ():
        print("NEW USER")
        if request.form['Password'] != request.form['PasswordConfirmation']:
            regerror = "Passwords do not match!"
            return render_template("index.html", regerror=regerror)
        else:
            # Validate for empty
            if request.form['Username'] == '' or request.form['Email'] == '' or request.form['Password'] == '':
                regerror = "Please complete all required fields"
                return render_template("index.html", regerror=regerror)
            else:
                # *** REGISTRATION 2 ***
                # Create the New User
                print("CREATING NEW USER!!!")
                s2ms = connectToS2MS(db)
                query = "INSERT INTO users (username, email, password) VALUES (%(username)s ,%(email)s ,%(password)s )"
                data = {
                    "username": request.form['Username'],
                    "email": request.form['Email'],
                    "password": request.form['Password'],
                }
                s2ms.query_db(query, data)

                # *** REGISTRATION 3 ***
                # Set this user's id in session before redirecting
                s2ms = connectToS2MS(db)
                query = "SELECT * from users WHERE email=%(email)s"
                data = {"email": request.form['Email']}
                currUser = s2ms.query_db(query, data)

                session['userId'] = currUser[0]['userId']
                print(session['userId'])

                return redirect("/dashboard")

    else:
        print("EXISTING USER")
        regerror = "This email currently exists!"
        return render_template("index.html", regerror=regerror)


@app.route('/dashboard')
def dashboard():

    CurrSessionId = str(session['userId'])

    # if (not CurrSessionId):
    #     return redirect('/login')

    # *** DASHBOARD 1 ***
    # Retrieve Current User
    print("retrieving user")
    s2ms = connectToS2MS(db)
    query = "SELECT * FROM users WHERE userId = %(curruserid)s"
    data = {"curruserid": CurrSessionId}
    CurrUser = s2ms.query_db(query, data)

    # *** DASHBOARD 2 ***
    # Retrieve Current User's ToDos
    print("retriving todos")
    s2ms = connectToS2MS(db)
    query = "SELECT * FROM toDos WHERE userId= %(userid)s"
    data = {"userid": CurrSessionId}
    AllToDos = s2ms.query_db(query, data)
    print(AllToDos)

    print("retring websites")
    s2ms = connectToS2MS(db)
    query = "SELECT * FROM websites WHERE userId= %(userid)s"
    data = {"userid": CurrSessionId}
    AllWebsites = s2ms.query_db(query, data)
    print(AllWebsites)

    return render_template('dashboard.html', CurrUser=CurrUser, AllToDos=AllToDos, AllWebsites=AllWebsites)


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@app.route('/login', methods=['POST'])
def login():
    # *** LOGIN ***
    # Retrieve user with email
    s2ms = connectToS2MS(db)
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = {"email": request.form['Email']}
    CurrUser = s2ms.query_db(query, data)
    if CurrUser == ():
        logerror = "This email has not been registered. Please register or try again!"
        return render_template('index.html', logerror=logerror)
    else:
        # check password
        if CurrUser[0]["password"] != request.form['PwToCheck']:
            logerror = "The password is incorrect - please try again!"
            return render_template('index.html', logerror=logerror)

        # Set this user's id in session before redirecting
        session['userId'] = CurrUser[0]['userId']
        print(session['userId'])
        return redirect("/dashboard")


@app.route('/addWebsite', methods=['POST'])
def AddWebsite():
    if request.form['website_name'] == '' or request.form['website_url'] == '':
        error = "Please include all required fields."
        return render_template('dashboard', logerror=error)
    else:
        s2ms = connectToS2MS(db)
        query = "INSERT INTO websites (websiteName, websiteUrl, websiteKey, userId) VALUES (%(websiteName)s, %(websiteUrl)s, %(websiteKey)s, %(userid)s);"
        data = {
            "websiteName": request.form['website_name'],
            "websiteUrl": request.form['website_url'],
            "websiteKey": str(uuid4()),
            "userid": session['userId'],
        }
        CurrUser = s2ms.query_db(query, data)
        print(CurrUser, session['userId'])

    return redirect("/dashboard")


@app.route('/addToDo', methods=['POST'])
def addToDo():
    if request.form['Title'] == '' or request.form['Description'] == '':
        todoerror = "Please include all required fields."
    else:
        # *** CREATE TODO ***
        # Create New ToDo
        s2ms = connectToS2MS(db)
        query = "INSERT INTO toDos (title, description, userId) VALUES (%(title)s, %(description)s, %(userid)s);"
        data = {
            "title": request.form['Title'],
            "description": request.form['Description'],
            "userid":  session['userId'],
        }
        print('tihs isthe user id at todo', session['userId'])
        CurrUser = s2ms.query_db(query, data)
        print(CurrUser, session['userId'])

    return redirect("/dashboard")


@app.route('/delete/<websitesId>')
def delete(websitesId):
    # *** DELETE TODO ***
    # Delete Todo
    s2ms = connectToS2MS(db)
    query = "DELETE FROM websites WHERE websitesId = %(websitesId)s"
    data = {"websitesId": websitesId}
    s2ms.query_db(query, data)

    return redirect("/dashboard")


@app.route('/edit/<websitesId>')
def edit(websitesId):
    # *** EDIT TODO 1 ***
    # Retreive ToDo Using TodoId
    s2ms = connectToS2MS(db)
    query = "SELECT * FROM websites WHERE websitesId = %(websitesId)s"
    data = {"websitesId": websitesId}
    CurrWebsite = s2ms.query_db(query, data)

    # # Retreive the data send to the website
    s2ms = connectToS2MS(db)
    query2 = "SELECT * FROM dt WHERE websitesId = %(websitesId)s"
    data2 = {"websitesId": websitesId}
    CurrData = s2ms.query_db(query2, data2)

    return render_template('edit.html', CurrWebsite=CurrWebsite, data=CurrData)


@app.route('/api/v1', methods=['POST'])
def apiCenter():
    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json = request.json
        s2ms = connectToS2MS(db)
        query2 = "INSERT INTO dt (websitesId, pageHref, countryId, ssTime) VALUES (%(websitesId)s, %(pageHref)s, %(countryId)s, %(ssTime)s );"
        data2 = {
            "websitesId": json['websiteId'],
            "pageHref": json['pageHref'],
            "countryId": json['countryId'],
            "ssTime": json['ssTime']
        }
        CurrUser = s2ms.query_db(query2, data2)
        return jsonify(CurrUser)
    else:
        return 'Please Post json request'


@app.route('/EditTodo', methods=['POST'])
def EditTodo():
    # *** EDIT TODO 2 ***
    # Update Todo
    s2ms = connectToS2MS(db)
    query = "UPDATE websites SET websiteName = %(websiteName)s, websiteUrl = %(websiteUrl)s WHERE websitesId = %(websitesId)s;"
    data = {
        "websiteName": request.form['websiteName'],
        "websiteUrl": request.form['websiteUrl'],
        "websitesId": request.form['websitesId']
    }
    s2ms.query_db(query, data)

    return redirect("/dashboard")


if __name__ == "__main__":
    app.run(debug=True)

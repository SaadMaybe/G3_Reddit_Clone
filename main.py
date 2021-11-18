from typing import SupportsRound
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from werkzeug.utils import redirect

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'SaadAkbar'
app.config['MYSQL_DB'] = 'reddit2'

mysql = MySQL(app)

def createSubreddit(inpname, inpdescription):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO reddit2.users VALUES(%s, %s, %s)", (inpname, 0, inpdescription))
        mysql.connection.commit()
    except Exception as lol_ho_gaya:
        print("Exception occured.")
        pass

def LoginFunc(inpUsername, inpPassword):
    cursor = mysql.connection.cursor()
    
    cursor.execute("Select username from reddit2.users where username=%s", (inpUsername,))
    if(cursor.fetchone() == None):
        print("User does not exist")
        return False
    
    # cursor.execute("SELECT name FROM reddit2.subreddits WHERE name=%s", (subreddit_name,))
    # if(cursor.fetchone() != None):
    #     print("Subreddit already exists")
    #     return False
    
    #Insert into the subreddit table
    cursor.execute("INSERT INTO reddit2.subreddits VALUES(%s, %s)", (subreddit_name, description))
    mysql.connection.commit()

    #Insertion into the Joined table, to show that the user has created the subreddit
    cursor.execute("INSERT INTO reddit2.joined VALUES(%s, %s, %s)", (username, subreddit_name, "Subreddit Owner"))
    mysql.connection.commit()
    
    return True    
    
    
def leave_subreddit_case(username ="saad", subreddit_name = "woosh"):
    cursor = mysql.connection.cursor()
    
    cursor.execute("Select username from reddit2.users where username=%s", (username,))
    if(cursor.fetchone() == None):
        print("User does not exist")
        return False

    cursor.execute("SELECT name FROM reddit2.subreddits WHERE name= %s", (subreddit_name,))
    if(cursor.fetchone() == None):
        print("Subreddit does not exist")
        return False
    
    #Check if the user is the owner of the subreddit
    cursor.execute("SELECT roles FROM reddit2.joined WHERE username=%s AND subreddit=%s", (username, subreddit_name))
    if(cursor.rowcount == 0):
        return False
    if(cursor.fetchone()[0] == "Subreddit Owner"):
        print("You are the owner of this subreddit, you cannot leave :>")
        return False
    #Remove from the joined table
    cursor.execute("DELETE FROM reddit2.joined WHERE username=%s AND name=%s", (username, subreddit_name))
    
    return True


def signup_case(username="rrreeewewewe", passwd= "223313131"):
    cursor = mysql.connection.cursor()
    success = 0
    
    try:
        success = cursor.execute("INSERT INTO reddit2.users VALUES(%s, %s, %s)", (username, 0, passwd))
        mysql.connection.commit()
    except Exception as it_is_what_it_is:
        print("excepion caught")
        pass
    
    if success == 1: #Successfully inserted
        print("Congratulations! Your account has been made")
        return True
    else:
        print("Error, the account already exists, please choose a different username")
        return False
        
#@app.route("/login.html")dsad
def login(input_user, input_password):
    cursor = mysql.connection.cursor()
    # input_user = request.values.get('username', 'bruh')
    # input_password = request.values.get('password', 'bruh')
    cursor.execute('''SELECT username, password FROM reddit2.users WHERE username=%s AND password=%s''', (input_user, input_password))
    
    if cursor.rowcount == 0:
        print("Incorrect username or password")
        return False
    else:
        return True


@app.route("/", methods = ["POST", "GET"])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if login(username, password):
            print(True)
        else:
            print(False)

    return render_template("login.html")



@app.route("/signup.html")
def signup(): 
    
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
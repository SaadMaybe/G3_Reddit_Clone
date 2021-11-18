curr_user = "guest" #Stores the username of the current username

from typing import SupportsRound
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '33e0a108'
app.config['MYSQL_DB'] = 'reddit2'

mysql = MySQL(app)


def joinSubreddit(subreddit_name):
    inpUsername = curr_user
    cursor = mysql.connection.cursor()
    
    #Check if the subreddit that the user wants to join exists or not
    cursor.execute("SELECT name FROM reddit2.subreddits WHERE name=%s", (subreddit_name,))
    if(cursor.rowcount == 0):
        print("Subreddit does not exist")
        return False
    
    #Check if the user is already a member of the subreddit
    cursor.execute("SELECT roles FROM reddit2.joined WHERE username=%s AND subreddit=%s", (inpUsername, subreddit_name))
    if(cursor.rowcount != 0):
        print("You are already a member of this subreddit")    
        #return leaveSubredditCase(subreddit_name)
        return False
    
    try:
        cursor.execute("INSERT INTO reddit2.joined VALUES(%s, %s, %s)", (inpUsername, subreddit_name, "Member"))    
        mysql.connection.commit()
    except Exception as rip:
        return False
        
    
    return True

def createSubreddit(subreddit_name, description):
    cursor = mysql.connection.cursor()
    
    inpUsername = curr_user
    
    cursor.execute("SELECT name FROM reddit2.subreddits WHERE name=%s", (subreddit_name,))
    if(cursor.fetchone() != None):
        print("Subreddit with this name already exists")
        return False
    
    #Insert into the subreddit table
    cursor.execute("INSERT INTO reddit2.subreddits VALUES(%s, %s)", (subreddit_name, description))
    mysql.connection.commit()

    #Insertion into the Joined table, to show that the user has created the subreddit
    cursor.execute("INSERT INTO reddit2.joined VALUES(%s, %s, %s)", (inpUsername, subreddit_name, "Subreddit Owner"))
    mysql.connection.commit()
    
    return True    
    
    
def leaveSubredditCase(subreddit_name):

    cursor = mysql.connection.cursor()
    
    username = curr_user    
    
    cursor.execute("SELECT name FROM reddit2.subreddits WHERE name= %s", (subreddit_name,))
    if(cursor.fetchone() == None):
        print("Subreddit does not exist")
        return False
    
    #Check if the user is the owner of the subreddit
    cursor.execute("SELECT roles FROM reddit2.joined WHERE username=%s AND subreddit=%s", (username, subreddit_name))
    
    if(cursor.rowcount == 0): #The user is not a member of the subreddit
        #If thr user is not a member of the subreddit, they're made to join the subreddit
        #return joinSubreddit(subreddit_name)
        return False
    if(cursor.fetchone()[0] == "Subreddit Owner"):
        print("You are the owner of this subreddit, you cannot leave :>")
        return False
    #Remove from the joined table
    cursor.execute("DELETE FROM reddit2.joined WHERE username=%s AND name=%s", (username, subreddit_name))
    
    return True


def signup_case(username, passwd):
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
        
#@app.route("/login.html")
def login(input_user, input_password):
    cursor = mysql.connection.cursor()

    # hashed_password = generate_password_hash(input_password)
    # print(input_user, hashed_password)
    cursor.execute("SELECT username, password FROM reddit2.users WHERE username=%s AND password=%s", (input_user, input_password))
    
    if cursor.rowcount == 0:
        print("Incorrect username or password")
        return False
    else:
        curr_user = input_user
        return True


@app.route("/", methods = ["POST", "GET"])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if login(username, password):
            curr_user = username
            
            print(True)
        else:
            print(False)

    return render_template("login.html")

@app.route("/signup.html", methods = ["POST", "GET"])
def signup(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password1')
        print(username, password)
        
        val = signup_case(username, password)
        if(val):
           return redirect(url_for('home'))
        
    #return render_template("signup.html")
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
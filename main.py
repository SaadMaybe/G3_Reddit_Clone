curr_user = "guest" #Stores the username of the current username

#You know the rules, and so do I
#A full commitment's what I'm thinking of
#You wouldn't get this from any other guy
from logging import currentframe
from typing import SupportsRound
from MySQLdb import cursors
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '33e0a108'
app.config['MYSQL_DB'] = 'reddit2'

mysql = MySQL(app)

#Below, we have our member/helper functions

def joinSubreddit(subreddit_name):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM reddit2.active_users")
        curr_user = cursor.fetchone()[0]
        inpUsername = curr_user
        
        #Check if the subreddit that the user wants to join exists or not
        cursor.execute("SELECT name FROM reddit2.subreddits WHERE name=%s", (subreddit_name,))
        if(cursor.rowcount == 0):
            print("Subreddit does not exist")
            return False
        
        #Check if the user is already a member of the subreddit
        cursor.execute("SELECT roles FROM reddit2.joined WHERE username=%s AND subreddit=%s", (inpUsername, subreddit_name))
        if(cursor.rowcount != 0):
            print("You are already a member of this subreddit")    
            return False
        
        try:
            cursor.execute("INSERT INTO reddit2.joined VALUES(%s, %s, %s)", (inpUsername, subreddit_name, "Member"))    
            mysql.connection.commit()
        except Exception as rip:
            return False
            
    
        return True
    except Exception as rip:
        return False

def createSubreddit(subreddit_name, description):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM reddit2.active_users")
        curr_user = cursor.fetchone()[0]
        
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
    except Exception as a:
        return False
    
def leaveSubredditCase(subreddit_name):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM reddit2.active_users")
        curr_user = cursor.fetchone()[0]
        
        username = curr_user
        print("subreddit ka naam is ", subreddit_name)
        
        cursor.execute("SELECT name FROM reddit2.subreddits WHERE name= %s", (subreddit_name,))
        if(cursor.fetchone() == None):
            print("Subreddit does not exist")
            return False
        
        #Check if the user is the owner of the subreddit
        cursor.execute("SELECT roles FROM reddit2.joined WHERE username=%s AND subreddit=%s", (username, subreddit_name))
        
        if(cursor.rowcount == 0): #The user is not a member of the subreddit
            #If thr user is not a member of the subreddit, they're made to join the subreddit
            print("you're not a member of the subreddit :p")
            return False
        if(cursor.fetchone()[0] == "Subreddit Owner"):
            print("You are the owner of this subreddit, you cannot leave :>")
            return False
        #Remove from the joined table
        print("username is ", username, "and subreddit name is", subreddit_name)
        cursor.execute("DELETE FROM reddit2.joined WHERE username=%s AND subreddit=%s", (username, subreddit_name))
        mysql.connection.commit()
        return True
    except Exception as rip:
        return False

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
    
def login(input_user, input_password):
    try:
        cursor = mysql.connection.cursor()
        
        cursor.execute("SELECT username, password FROM reddit2.users WHERE username=%s AND password=%s", (input_user, input_password))
        
        if cursor.rowcount == 0:
            print("Incorrect username or password")
            return False
        else:
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE reddit2.active_users SET username = %s WHERE username = %s", (input_user, "guest"))
            mysql.connection.commit()
            
            return True
    except Exception as rip:
        return False

def viewSubreddit(subreddit_name):
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT name FROM reddit2.subreddits WHERE name = %s", (subreddit_name))

        if cursor.rowcount == 0:
            return False
        else:
            return True
    except Exception as ded:
        return False


#Here, we implement the upvote/downvote features

# def upvote(postid):
#     try:
#         cursor = mysql.connection.cursor()
#         cursor.execute("SELECT username FROM reddit2.active_users")
#         curr_user = cursor.fetchone()[0]
#         if curr_user == "guest":
#             print("You must be logged in to upvote")
#             return render_template(url_for('home'))
#         else:
#             #Incrases the number of upvotes of the post
#             cursor.execute("SELECT upvotes from reddit2.posts WHERE postid=%s", (postid,))
#             upV = cursor.fetchone()[0]
#             upV += 1
#             cursor.execute("UPDATE reddit2.posts SET upvotes=%s WHERE postid=%s", (upV, postid))
#             mysql.connection.commit()
            
#             #Increases the karma of the user who posted the post
#             cursor.execute("SELECT karma from reddit2.users WHERE username=%s", (curr_user,))
#             k = cursor.fetchone()[0]
#             k += 1
#             cursor.execute("UPDATE reddit2.users SET karma=%s WHERE username=%s", (k, curr_user))
#             mysql.connection.commit()
            
#             return True
#     except Exception as rip:
#         return False 
    
    
#Below, we have our routes

#@app.route('/request/<string:username>/<string: subreddit>')
def request_promote(username, subreddit):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM reddit2.active_users")
        curr_user = cursor.fetchone()[0]
    
        if curr_user == "guest":
            print("You are not logged in")
            return render_template(url_for('home'))
        else:
            
            cursor.execute("SELECT requester, subreddit FROM reddit2.requests WHERE requester=%s AND subreddit=%s", (username, subreddit))
            if cursor.rowcount == 0: 
                cursor.execute("INSERT INTO reddit2.requests VALUES (%s, %s)", (username, subreddit))
                mysql.connection.commit()
            else:
                print("You have already requested to promote this subreddit")
                return render_template(url_for('dash'))
            
    except Exception as hmm:
        return render_template(url_for('home'))
    
    
#@app.route('/promote-accept/<string:username>/<string:subreddit>')
def promote_accept(username, subreddit):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM reddit.requests WHERE requester=%s AND subreddit=%s", (username, subreddit))
        mysql.connection.commit()
        
        cursor.execute("UPDATE reddit2.joined SET roles=%s WHERE username=%s AND subreddit=%s", ("Moderator", username, subreddit))
        mysql.connection.commit()
        
        return render_template(url_for('dash'))
    except Exception as hmm:
        return render_template(url_for('dash'))

#@app.route('/promote-decline/user')
def promote_decline(username, subreddit):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM reddit.requests WHERE requester=%s AND subreddit=%s", (username, subreddit))
        mysql.connection.commit()
    
        return render_template(url_for('dash'))
    except Exception as lol_rejected:
        return render_template(url_for('dash'))
    

@app.route("/user.html")
def user_profile():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username FROM reddit2.active_users")
    
    curr_user = cursor.fetchone()[0]
    if curr_user != "guest": #Meaning that the person is looking at their own profile
        cursor.execute("SELECT username, karma FROM reddit2.users WHERE username=%s", (curr_user,))
        if cursor.rowcount == 0:
            return render_template("home.html")
        
        user_details = cursor.fetchone()
        username = user_details[0]
        karma = user_details[1]
        cursor.execute("SELECT subreddit FROM reddit2.joined WHERE username=%s", (curr_user,))
        if cursor.rowcount != 0:
            subreddits = cursor.fetchall()
        else:
            subreddits = []
            
        
        return render_template("user.html", username=username, karma=karma, subreddits=subreddits)
        
    else: #Someone else is looking at a person's profile, which isn't allowed
        return render_template("home.html")        

@app.route("/unsucessful.html", methods=['GET', 'POST'])
def unsuc():
    return render_template("unsucessful.html")


@app.route("/sucessful.html", methods=['GET', 'POST'])
def suc():
    return render_template("sucessful.html")


#These routes are for creating, joining, and leaving a subreddit
@app.route("/create-reddit.html", methods=["GET", "POST"])
def create():
    
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM reddit2.active_users")
        curr_user = cursor.fetchone()[0]
        
        if curr_user != "guest":
            subreddit_name = request.form.get("subreddit_name1")
            description = request.form.get("description1")

            if(createSubreddit(subreddit_name, description)):
                return redirect("sucessful.html")
            else:
                return redirect("unsucessful.html")
        else:
            print("You must be logged in to create a subreddit")
            return redirect("login.html")
    return render_template("create-reddit.html")


@app.route("/join-reddit.html", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM reddit2.active_users")
        curr_user = cursor.fetchone()[0]
        
        if curr_user != "guest":
            subreddit_name = request.form.get("subreddit_name1")
            if joinSubreddit(subreddit_name):
                return redirect("sucessful.html")
            else:
                return redirect("unsucessful.html")
        else:
            print("You must be logged in to join a subreddit")
            return redirect("login.html")
    return render_template("join-reddit.html")

@app.route("/delete-reddit.html", methods=["GET", "POST"])
def leave():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM reddit2.active_users")
        curr_user = cursor.fetchone()[0]
        if curr_user != "guest":
            subreddit_name = request.form.get("subreddit_name1")
            if leaveSubredditCase(subreddit_name):
                return redirect("sucessful.html")
            else:
                return redirect("unsucessful.html")
        else:
            print("You must be logged in to leave a subreddit")
            return redirect("login.html")
    return render_template("delete-reddit.html")
    
    
    
'''This function is for the actions carried out on the dashboard '''
@app.route("/dashboard.html", methods=["GET", "POST"])
def dash():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username FROM reddit2.active_users")
    curr_user = cursor.fetchone()[0]
    
    if curr_user != "guest":
        cursor.execute("SELECT requester, subreddit FROM reddit2.requests WHERE subreddit IN (SELECT subreddit FROM reddit2.joined WHERE username=%s AND (roles=%s OR roles=%s))", (curr_user, "moderator", "Subreddit Owner"))
        if cursor.rowcount==0:
            requests = []
        else:
            requests = cursor.fetchall() 
        return render_template("dashboard.html", requests=requests)
            
    else:
        print("You must be logged in to view the dashboard")
        return redirect("login.html")
    
'''This function is for the homepage of our application. By default, it opens the login page for the user'''
@app.route("/", methods = ["POST", "GET"])
def home(): 
    
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM active_users",)
    mysql.connection.commit()
    try:
        cursor.execute("INSERT INTO active_users VALUES (%s)", ("guest",))
        mysql.connection.commit()
    except:
        pass

    
    
    if request.method == 'POST':        
        username = request.form.get('username')
        password = request.form.get('password')
        if login(username, password): #This function automatically updates curr_user as well
            print("True")
            return redirect(url_for('dash'))
        else:
            print(False)
            return redirect("sucessful.html")
        
    return render_template("login.html")

'''This function is to handle the "sign up" use case, when a user wishes to create an account'''
@app.route("/signup.html", methods = ["POST", "GET"])
def signup(): 
    if request.method == 'POST':
        if curr_user == "guest":
            username = request.form.get('username')
            password = request.form.get('password1')
            print(username, password)
            
            val = signup_case(username, password)
            if(val):
                return redirect(url_for('home'))
            else:
                return redirect("/unsucessful.html")
        else:
            print("You are already logged in!")
            return redirect("/dashboard.html")
            
    return render_template("signup.html")

@app.route("/logout.html")
def logout():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM reddit2.active_users",)
        mysql.connection.commit()
        cursor.execute("INSERT INTO reddit2.active_users VALUES (%s)", ("guest",))
        mysql.connection.commit()    
    except:
        pass
    return redirect(url_for('home'))

@app.route("/displaySubreddit", defaults={'subreddit_name' : 'all'})
@app.route("/")
def displaySubreddit(subreddit_name):
    if viewSubreddit(subreddit_name):
        cursor = mysql.connection.cursor()
        try:
            posts = cursor.execute("SELECT * FROM reddit2.posts WHERE postid IN (SELECT postid FROM reddit2.posted_in WHERE subreddit = %s))" , subreddit_name)
            return render_template("displaySubreddit.html", posts=posts)
        except:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))  

@app.route("/login.html")
def loginA():
    return redirect(url_for('home'))
    
if __name__ == "__main__":
    app.run(debug=True)
    
curr_user = "guest" #Stores the username of the current username

#You know the rules, and so do I
#A full commitment's what I'm thinking of
#You wouldn't get this from any other guy
from logging import currentframe
from re import sub
from typing import SupportsRound
from MySQLdb import cursors
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import ast
from Functions import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'us-cdbr-east-05.cleardb.net'
app.config['MYSQL_USER'] = 'bc581d899a9288'
app.config['MYSQL_PASSWORD'] = '019c7e40'
app.config['MYSQL_DB'] = 'heroku_0b525497a3fc037'

mysql = MySQL(app)

#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------Sorry---------------------------------------------------------


@app.route('/makePost.html/<uName>/<sName>', methods = ['GET','POST'])
def makePostRoute(uName, sName):
    print("In makePostRoute")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username FROM heroku_0b525497a3fc037.active_users")
    
    curr_user = cursor.fetchone()[0]
    sub_name = sName
    if request.method == 'POST':
        titletext = request.form.get('title')
        textText = request.form.get('text')
        if (PostInSubreddit(sub_name, titletext, textText)):
            print("successful Post")
            return redirect(url_for('dash'))
        else:
            return redirect(url_for('unsuc', ErrorMessage = "Post failed"))
    else:
        return render_template("makePost.html")


#@app.route('/request/<string:username>/<string: subreddit>')
def request_promote(username, subreddit):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM heroku_0b525497a3fc037.active_users")
        curr_user = cursor.fetchone()[0]
    
        if curr_user == "guest":
            print("You are not logged in")
            return render_template(url_for('home'))
        else:
            
            cursor.execute("SELECT requester, subreddit FROM heroku_0b525497a3fc037.requests WHERE requester=%s AND subreddit=%s", (username, subreddit))
            if cursor.rowcount == 0: 
                cursor.execute("INSERT INTO heroku_0b525497a3fc037.requests VALUES (%s, %s)", (username, subreddit))
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
        
        cursor.execute("UPDATE heroku_0b525497a3fc037.joined SET roles=%s WHERE username=%s AND subreddit=%s", ("Moderator", username, subreddit))
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


@app.route('/emptySub.html/<Dlist>/<uName>/<sName>', methods = ['GET','POST'])
def viewSubredditPage(Dlist, uName, sName):

    s2 = []
    s = ast.literal_eval(Dlist)
    print(Dlist[0])
    if Dlist[0] == '(':
        s2 = [("","","No Posts","","",0,0)]
        return render_template("subreddit_page.html", Dlist = s2, Username = uName, Subreddit = sName)
    return render_template("subreddit_page.html", Dlist = s, Username = uName, Subreddit = sName)


@app.route('/emptySub.html/<Dlist>/<uName>/<sName>', methods = ['GET','POST'])
def viewEmptySubredditPage(Dlist, uName, sName):
    s = ast.literal_eval(Dlist)
    return render_template("emptySub.html", Dlist = s, Username = uName, Subreddit = sName)

@app.route('/view_subreddit.html', methods=['GET', 'POST'])
def subredditLists():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username FROM heroku_0b525497a3fc037.active_users")
    
    curr_user = cursor.fetchone()[0]
    # cursor = mysql.connection.cursor()
    #If the method is POST, we are going to return the list of posts and redirect to the page
    if request.method == 'POST':
        #Get the name of the subreddit to be displayed
        sub_name = request.form.get('sub_name')
        cursor.execute('SELECT name FROM heroku_0b525497a3fc037.subreddits WHERE name =%s', (sub_name, ))
        if cursor.rowcount == 0:
            return redirect(url_for('unsuc', ErrorMessage = "Subreddit does not exist"))
            
        #Get the names of the posts
        cursor.execute('SELECT postid FROM heroku_0b525497a3fc037.posted_in WHERE subreddit=%s', (sub_name,))
        #No posts in this subreddit
        if cursor.rowcount == 0:
            return redirect(url_for('viewEmptySubredditPage', Dlist = [()], uName = curr_user, sName = sub_name))           
        if cursor.rowcount == 1:
            postsIDs = cursor.fetchall()
            postList = []
            jugar = "SamplePic"
            for everyElement in postsIDs:
                cursor.execute('SELECT postid,username,title, text, image, upvotes,downvotes FROM heroku_0b525497a3fc037.posts WHERE postid=%s', (everyElement[0],))
                
                if cursor.rowcount == 0:
                    continue #How even, this should never happen
                else:
                    postList.append(cursor.fetchone())
            return redirect(url_for('viewSubredditPage', Dlist = postList, uName = curr_user, sName = sub_name))
        else:
            #this tuple will be of the form: ((postID1,), (postID2,), ...)
            postsIDs = cursor.fetchall()
            postList = []
            jugar = "SamplePic"
            for everyElement in postsIDs:
                cursor.execute('SELECT postid,username,title, text, image, upvotes,downvotes FROM heroku_0b525497a3fc037.posts WHERE postid=%s', (everyElement[0],))
                
                if cursor.rowcount == 0:
                    continue #How even, this should never happen
                else:
                    postList.append(cursor.fetchone())
            return redirect(url_for('viewSubredditPage', Dlist = postList, uName = curr_user, sName = sub_name))
    else: 
        cursor.execute("SELECT subreddit FROM heroku_0b525497a3fc037.joined WHERE username = %s", (curr_user,))
        
        data = cursor.fetchall()
        return render_template('view_subreddit.html', subredditList=data)



@app.route("/user.html")
def user_profile():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username FROM heroku_0b525497a3fc037.active_users")
    
    curr_user = cursor.fetchone()[0]
    if curr_user != "guest": #Meaning that the person is looking at their own profile
        cursor.execute("SELECT username, karma FROM heroku_0b525497a3fc037.users WHERE username=%s", (curr_user,))
        if cursor.rowcount == 0:
            return render_template("home.html")
        

        user_details = cursor.fetchone()
        cursor.execute("SELECT Subreddit FROM heroku_0b525497a3fc037.joined WHERE username=%s", (curr_user,))
        SlistTemp = cursor.fetchall()
        Slist = []

        for i in SlistTemp:
            Slist.append(i[0])
        username = user_details[0]
        karma = user_details[1]
        cursor.execute("SELECT subreddit FROM heroku_0b525497a3fc037.joined WHERE username=%s", (curr_user,))
        if cursor.rowcount != 0:
            subreddits = cursor.fetchall()
        else:
            subreddits = []
            
        return render_template("user.html", username=username, karma=karma, subreddits=subreddits, Slist = Slist)
        
    else: #Someone else is looking at a person's profile, which isn't allowed
        return render_template("home.html")        

@app.route("/unsucessful.html/<ErrorMessage>", methods=['GET', 'POST'])
def unsuc(ErrorMessage):
    return render_template("unsucessful.html", message = ErrorMessage)

@app.route("/sucessful.html", methods=['GET', 'POST'])
def suc():
    return render_template("sucessful.html")

#These routes are for creating, joining, and leaving a subreddit
@app.route("/create-reddit.html", methods=["GET", "POST"])
def create():
    
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM heroku_0b525497a3fc037.active_users")
        curr_user = cursor.fetchone()[0]
        
        if curr_user != "guest":
            subreddit_name = request.form.get("subreddit_name1")
            description = request.form.get("description1")

            if createSubreddit(subreddit_name, description):
                return redirect("sucessful.html")
            else:
                return redirect(url_for("unsuc", ErrorMessage = "Create Subreddit Failed"))
        else:
            return redirect("login.html")
    return render_template("create-reddit.html")

@app.route("/join-reddit.html", methods=["GET", "POST"])
def join():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username FROM heroku_0b525497a3fc037.active_users")
    curr_user = cursor.fetchone()[0]
    
    if request.method == "POST":
        
        
        # cursor.execute("SELECT name FROM heroku_0b525497a3fc037.subreddits WHERE ")

        if curr_user != "guest":
            subreddit_name = request.form.get("subreddit_name1")
            if joinSubreddit(subreddit_name):
                return redirect("sucessful.html")
            else:
                return redirect(url_for("unsuc", ErrorMessage = "Joining Failed"))
        else:
            print("You must be logged in to join a subreddit")
            return redirect("login.html")
    
    # cursor.execute("SELECT t1.name FROM heroku_0b525497a3fc037.subreddits t1 LEFT JOIN joined t2 ON t2.subreddit = t1.name WHERE t2.username IS NULL")
    cursor.execute("SELECT name FROM subreddits WHERE NOT EXISTS (SELECT subreddit FROM joined WHERE username = %s)", (curr_user,))
    #   cursor.execute("SELECT name FROM heroku_0b525497a3fc037.subreddits EXCEPT SELECT subreddit FROM heroku_0b525497a3fc037.joined WHERE username = %s", (curr_user,))
    SlistTemp = cursor.fetchall()
    print(SlistTemp)
    Slist = []
    for i in SlistTemp:
        Slist = SlistTemp[0]
    return render_template("join-reddit.html", Slist = Slist)

@app.route("/delete-reddit.html", methods=["GET", "POST"])
def leave():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM heroku_0b525497a3fc037.active_users")
        curr_user = cursor.fetchone()[0]
        if curr_user != "guest":
            subreddit_name = request.form.get("subreddit_name1")
            if leaveSubredditCase(subreddit_name):
                return redirect("sucessful.html")
            else:
                return redirect(url_for("unsuc", ErrorMessage = "you are the owner of this subreddit"))
        else:
            print("You must be logged in to leave a subreddit")
            return redirect("login.html")
    return render_template("delete-reddit.html")
    
    
    
'''This function is for the actions carried out on the dashboard '''
@app.route("/dashboard.html", methods=["GET", "POST"])
def dash():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username FROM heroku_0b525497a3fc037.active_users")
    curr_user = cursor.fetchone()[0]
    
    if curr_user != "guest":
        cursor.execute("SELECT requester, subreddit FROM heroku_0b525497a3fc037.requests WHERE subreddit IN (SELECT subreddit FROM heroku_0b525497a3fc037.joined WHERE username=%s AND (roles=%s OR roles=%s))", (curr_user, "moderator", "Subreddit Owner"))
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
            # print("True")
            return redirect(url_for('dash'))
        else:
            # print(False)
            return redirect(url_for("unsuc", ErrorMessage = "Username or password wrong"))
        
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
                return redirect(url_for("unsuc",ErrorMessage = "Signup failed" ))
        else:
            return redirect("/dashboard.html")
            
    return render_template("signup.html")

@app.route("/logout.html")
def logout():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM heroku_0b525497a3fc037.active_users",)
        mysql.connection.commit()
        cursor.execute("INSERT INTO heroku_0b525497a3fc037.active_users VALUES (%s)", ("guest",))
        mysql.connection.commit()    
    except:
        pass
    return redirect(url_for('home'))

# @app.route("/displaySubreddit/", defaults={'subreddit_name' : 'all'})
# @app.route("/displaySubreddit/<name>")
# def displaySubreddit(subreddit_name):
#     if viewSubreddit(subreddit_name):
#         cursor = mysql.connection.cursor()
#         try:
#             posts = cursor.execute("SELECT * FROM heroku_0b525497a3fc037.posts WHERE postid IN (SELECT postid FROM heroku_0b525497a3fc037.posted_in WHERE subreddit = %s))" , subreddit_name)
#             return render_template("displaySubreddit.html", posts=posts)
#         except:
#             return redirect(url_for('home'))
#     else:
#         return redirect(url_for('home'))  

@app.route("/login.html")
def loginA():
    return redirect(url_for('home'))
    
if __name__ == "__main__":
    app.run(debug=True)
    
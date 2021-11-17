from typing import SupportsRound
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '<]^7f[R2<n'
app.config['MYSQL_DB'] = 'reddit2'

mysql = MySQL(app)

def create_subreddit_case(username = "sad", subreddit_name= "woosh", description = "woosh brotha"):
    cursor = mysql.connection.cursor()
    
    cursor.execute("Select username from reddit2.users where username=%s", (username,))
    if(cursor.fetchone() == None):
        print("User does not exist")
        return False
    
    cursor.execute("Select subreddit_name from reddit2.subreddits where subreddit_name=%s", (subreddit_name,))
    if(cursor.fetchone() != None):
        print("Subreddit already exists")
        return False
    
    #Insert into the subreddit table
    cursor.execute("INSERT INTO reddit2.subreddits VALUES(%s, %s, %s)", (subreddit_name, description, username))
    mysql.connection.commit()

    #Insertion into the Joined table, to show that the user has created the subreddit
    cursor.execute("INSERT INTO reddit2.joined VALUES(%s, %s. %s)", (username, subreddit_name, "Subreddit Owner"))
    mysql.connection.commit()
    
    return True    
    
    
def leave_subreddit_case(username ="sad", subreddit_name = "rip", ):
    cursor = mysql.connection.cursor()
    
    cursor.execute("Select username from reddit2.users where username=%s", (username,))
    if(cursor.fetchone() == None):
        print("User does not exist")
        return False
    
    cursor.execute("Select subreddit_name from reddit2.subreddits where subreddit_name=%s", (subreddit_name,))
    if(cursor.fetchone() == None):
        print("Subreddit does not exist")
        return False
    
    
    #Remove from the joined table
    cursor.execute("DELETE FROM reddit2.joined WHERE username=%s AND subreddit_name=%s", (username, subreddit_name))
    
    return True
    

    

def signup_case(username="rrreeewewewe", passwd= "223313131"):
    cursor = mysql.connection.cursor()
    
    
    success = False
    
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
def login():
    cursor = mysql.connection.cursor()
    input_user = request.values.get('username', 'bruh')
    input_password = request.values.get('password', 'bruh')
    cursor.execute('''SELECT username, password FROM reddit2.users WHERE username=%s AND password=%s''', (input_user, input_password))
    
    if cursor.rowcount == 0:
        print("Incorrect username or password")
    else:
        return True

@app.route("/")
def home():
    cursor = mysql.connection.cursor()
    #cursor.execute('''INSERT INTO reddit2.users VALUES('saad', 1234, 0)''')
    # cursor1 = mysql.connection.cursor()
    # cursor1.execute('select * from reddit2.users')
    # mysql.connection.commit()
    
    # for x in cursor1:
    #     print(x)
    login()
    return render_template("login.html")

@app.route("/signup.html")
def signup(): 
    
    return render_template("signup.html")

@app.route("/create-subreddit")
def create_subreddit():
    create_subreddit_case()
    return render_template("signup.html")



if __name__ == "__main__":
    app.run(debug=True)
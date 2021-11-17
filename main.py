from typing import SupportsRound
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '<]^7f[R2<n'
app.config['MYSQL_DB'] = 'reddit2'

mysql = MySQL(app)

def signup_case(username="rrreeewewewe", passwd= "223313131"):
    cursor = mysql.connection.cursor()
    username = "user_name"
    passwd = "blady"
    
    success = False
    
    try:
        success = cursor.execute("INSERT INTO reddit2.users VALUES(%s, %s, %s)", (username, 0, passwd))
        mysql.connection.commit()
    except Exception as it_is_what_it_is:
        print("excepion caught")
        pass
    
    if success == 1: #Successfully inserted
        print("Congratulations! Your account has been made")
    else:
        print("Error, the account already exists, please choose a different username")
        
    # cursor1 = mysql.connection.cursor()
    # cursor1.execute('select * from reddit2.users')
    mysql.connection.commit()
    
    # for x in cursor1:
    #     print(x)
    
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
    signup_case("random name", "random pwd")
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
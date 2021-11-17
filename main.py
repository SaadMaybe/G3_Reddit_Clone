from typing import SupportsRound
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '33e0a108'
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
    
    

@app.route("/")
def home():
    cursor = mysql.connection.cursor()
    #cursor.execute('''INSERT INTO reddit2.users VALUES('saad', 1234, 0)''')
    # cursor1 = mysql.connection.cursor()
    # cursor1.execute('select * from reddit2.users')
    # mysql.connection.commit()
    
    # for x in cursor1:
    #     print(x)
    return render_template("login.html")

@app.route("/signup.html")
def signup():
    signup_case("random name", "random pwd")
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
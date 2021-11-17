from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'SaadAkbar'
app.config['MYSQL_DB'] = 'reddit2'

mysql = MySQL(app)

@app.route("/")
def home():
    cursor = mysql.connection.cursor()
    cursor.execute('SHOW DATABASES')
    for x in cursor:
        print(x)
    return render_template("login.html")
    
@app.route("/signup.html")
def signup():
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
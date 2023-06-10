import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
# app.config["MYSQL_DATABASE_USER"] = "root"
# app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password")
# app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")
# app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
# app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
MYSQL_DATABASE_USER = os.getenv('MYSQL_DATABASE_USER', 'root')
MYSQL_DATABASE_PASSWORD = os.getenv('MYSQL_DATABASE_PASSWORD', 'admin')
MYSQL_DATABASE_DB = os.getenv('MYSQL_DATABASE_DB', 'mysql')
MYSQL_DATABASE_HOST = os.getenv('MYSQL_DATABASE_HOST', 'localhost')
MYSQL_DATABASE_PORT = os.getenv('MYSQL_DATABASE_PORT', '3306')
mysql.init_app(app)


"""Function to test the functionality of the API"""
@app.route("/")
def index():
    return "Home Page"


"""Function to create a user to the MySQL database"""
@app.route("/create", methods=["POST"])
def add_user():
    json = request.json
    name = json["name"]
    email = json["email"]
    pwd = json["pwd"]
    if name and email and pwd and request.method == "POST":
        sql = "INSERT INTO users(user_name, user_email, user_password) " \
              "VALUES(%s, %s, %s)"
        data = (name, email, pwd)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            resp = jsonify("User created successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide name, email and pwd")


"""Function to retrieve all users from the MySQL database"""
@app.route("/users", methods=["GET"])
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

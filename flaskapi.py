import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = os.getenv('MYSQL_DATABASE_USER')
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config["MYSQL_DATABASE_DB"] = os.getenv('MYSQL_DATABASE_DB')
app.config["MYSQL_DATABASE_HOST"] = os.getenv('MYSQL_DATABASE_HOST')
app.config["MYSQL_DATABASE_PORT"] = int(os.getenv('MYSQL_DATABASE_PORT'))
mysql.init_app(app)

"""Function to test the functionality of the API"""
@app.route("/")
def index():
    return "Home Page"

"""Function to retrieve all users from the MySQL database"""
@app.route("/users", methods=["GET"])
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")
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

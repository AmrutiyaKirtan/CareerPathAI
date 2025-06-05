from flask import Flask
from flask_mysqldb import MySQL
from auth import auth
from home import home
from resume import resume

app = Flask(__name__)
app.secret_key = 'Kirtan95109'  # Change this to a random secret key
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Kirtan95109'
app.config['MYSQL_DB'] = 'user_info'

mysql = MySQL(app)

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(home)
app.register_blueprint(resume, url_prefix='/resume')  # Add url_prefix for resume routes

if __name__ == '__main__':
    print("Starting Flask application...")  # Debugging line
    with app.app_context():  # Create an application context
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT 1")
            print("MySQL connection successful!")
        except Exception as e:
            print("MySQL connection failed:", e)
    app.run(debug=True, port=3000)  # Changed port to 3000
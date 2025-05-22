from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

auth = Blueprint('auth', __name__)
mysql = MySQL()

@auth.route('/')
def index():
    return render_template('auth.html')

@auth.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE name = %s AND password = %s", (name, password))
    user = cur.fetchone()
    cur.close()
    if user:
        print("User found:", user)  # Debugging line
        session['name'] = name  # Set the name from the form input
        print("Session:", session)  # Debugging line
        return redirect(url_for('home.home_page'))
    else:
        print("Login failed for:", name)  # Debugging line
    return redirect(url_for('auth.index'))

@auth.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('auth.index'))

from flask import Blueprint, render_template, session, redirect, url_for

home = Blueprint('home', __name__)

@home.route('/home')
def home_page():
    if 'user_id' in session:
        return render_template('home.html', name=session['name'])
    return redirect(url_for('auth.index'))

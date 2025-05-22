from flask import Blueprint, render_template, session, redirect, url_for

resume = Blueprint('resume', __name__)

@resume.route('/resume')
def home_page():
    if 'user_id' in session:
        return render_template('resume.html', name=session['name'])
    return redirect(url_for('auth.index'))
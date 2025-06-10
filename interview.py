from flask import Blueprint, render_template, session, redirect, url_for

interview = Blueprint('interview', __name__)

@interview.route('/mock-interview')
def mock_interview():
    if 'name' not in session:
        return redirect(url_for('auth.index'))
    return render_template('interview.html', name=session['name'])

@interview.route('/start-interview', methods=['POST'])
def start_interview():
    if 'name' not in session:
        return redirect(url_for('auth.index'))
    # TODO: Add interview logic here
    return render_template('interview.html', name=session['name'])

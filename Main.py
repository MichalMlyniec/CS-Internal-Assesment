from flask import Flask, render_template, request, redirect, url_for, session, flash
from Login_Signup import init_db, register_teacher, login_teacher

app = Flask(__name__)
app.secret_key = 'f3a9b2c7e1d4f6a8b0c2e5d7f9a1b3c5'

init_db()


class Student:
    def __init__(self, student_id, username, class_id):
        self.student_id = student_id
        self.username   = username
        self.class_id   = class_id

    def submit_feedback(self, _lesson_id, _answers):
        pass

    def get_answers(self, _lesson_id):
        pass

    def get_all_answers(self):
        pass


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username         = request.form['username'].strip()
        password         = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not password:
            flash('Username and password cannot be empty.', 'error')
            return render_template('signup.html')

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return render_template('signup.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('signup.html')

        success, message = register_teacher(username, password)
        if success:
            flash(message, 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        success, teacher_id = login_teacher(username, password)
        if success:
            session['teacher_id'] = teacher_id
            session['username']   = username
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect username or password.', 'error')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'teacher_id' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
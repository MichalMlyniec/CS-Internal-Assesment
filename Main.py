from flask import Flask, render_template, request, redirect, url_for, session, flash
from Login_Signup import DB_PATH, register_teacher, login_teacher
from Year import current_school_year, make_year_string, parse_start_year
from Class import create_class, get_classes
import sqlite3

app = Flask(__name__)
app.secret_key = 'f3a9b2c7e1d4f6a8b0c2e5d7f9a1b3c5'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            class_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT    NOT NULL,
            year_id    TEXT    NOT NULL,
            teacher_id INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

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
    year      = request.args.get('year', current_school_year())
    start     = parse_start_year(year)
    prev_year = make_year_string(start - 1)
    next_year = make_year_string(start + 1)
    classes   = get_classes(session['teacher_id'], year)
    return render_template('dashboard.html',
        username=session['username'],
        classes=classes,
        year=year,
        prev_year=prev_year,
        next_year=next_year
    )


@app.route('/create_class', methods=['GET', 'POST'])
def create_class_route():
    if 'teacher_id' not in session:
        return redirect(url_for('login'))

    current = current_school_year()
    start   = parse_start_year(current)
    years   = [make_year_string(start + i) for i in range(-2, 2)]

    if request.method == 'POST':
        class_name = request.form['class_name'].strip()
        year_id    = request.form['year_id']

        if not class_name:
            flash('Class name cannot be empty.', 'error')
            return render_template('create_class.html', years=years, current=current)

        create_class(session['teacher_id'], class_name, year_id)
        flash('Class created successfully.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_class.html', years=years, current=current)


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

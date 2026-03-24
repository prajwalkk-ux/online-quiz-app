from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

# -------------------- DATABASE INIT --------------------
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT
        )
    ''')

    # Scores table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            score INTEGER
        )
    ''')

    conn.commit()
    conn.close()

# Initialize DB
init_db()


# -------------------- HOME --------------------
@app.route('/')
def home():
    return render_template("login.html")


# -------------------- REGISTER --------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, password))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("register.html")


# -------------------- LOGIN --------------------
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        session['username'] = username
        return redirect('/dashboard')
    else:
        return "Invalid Username or Password"


# -------------------- DASHBOARD --------------------
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template("dashboard.html")
    return redirect('/')


# -------------------- QUIZ --------------------
@app.route('/quiz')
def quiz():
    return render_template("quiz.html")


# -------------------- RESULT --------------------
@app.route('/result', methods=['POST'])
def result():
    score = 0

    q1 = request.form.get('q1')
    q2 = request.form.get('q2')

    if q1 == "Python":
        score += 1

    if q2 == "SQLite":
        score += 1

    username = session.get('username')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO scores (username, score) VALUES (?, ?)", (username, score))

    conn.commit()
    conn.close()

    return render_template("result.html", score=score)


# -------------------- HISTORY --------------------
@app.route('/history')
def history():
    username = session.get('username')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT score FROM scores WHERE username=?", (username,))
    data = cursor.fetchall()

    conn.close()

    return render_template("history.html", data=data)


# -------------------- LOGOUT --------------------
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
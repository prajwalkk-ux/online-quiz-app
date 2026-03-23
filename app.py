from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

# 🔥 STATIC PATH FIX
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder=os.path.join(base_dir, 'static'))

app.secret_key = "secret123"

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

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )

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

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
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

    cursor.execute(
        "INSERT INTO scores (username, score) VALUES (?, ?)",
        (username, score)
    )

    conn.commit()
    conn.close()

    return render_template("result.html", score=score)


# -------------------- HISTORY --------------------
@app.route('/history')
def history():
    username = session.get('username')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT score FROM scores WHERE username=?",
        (username,)
    )
    data = cursor.fetchall()

    conn.close()

    return render_template("history.html", data=data)


# -------------------- LOGOUT --------------------
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


# -------------------- TEST LOGO ROUTE 🔥 --------------------
@app.route('/test-logo')
def test_logo():
    return '<img src="/static/logo.jpg" width="200">'


# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, session
import sqlite3
import json

app = Flask(__name__)
app.secret_key = "mockinterview123"

# -----------------------------
# Database Connection
# -----------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# Create Tables
# -----------------------------
def create_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        answer TEXT
    )
    """)

    conn.commit()
    conn.close()

create_tables()


# -----------------------------
# Questions JSON 
# -----------------------------
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data["questions"]
        
# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------
# Register
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        if user:
            conn.close()
            return "Email already exists!"

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]  # name
            return redirect("/dashboard")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")

# -----------------------------
# Quiz Page
# -----------------------------
@app.route("/quiz")
def quiz():
    if "user" not in session:
        return redirect("/login")

    questions = load_questions()
    return render_template("quiz.html", questions=questions)
# -----------------------------
# Result Page
# -----------------------------
@app.route("/result", methods=["POST"])
def result():
    questions = load_questions()
    score = 0

    for q in questions:
        user_answer = request.form.get(str(q["id"]))
        if user_answer == q["answer"]:
            score += 1

    return render_template(
        "result.html",
        score=score,
        total=len(questions)
    )
# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

DB_NAME = "fitness.db"

# -----------------------------
# Database initialization
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    height REAL,
                    weight REAL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    workout_type TEXT,
                    duration INTEGER,
                    calories INTEGER,
                    date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )''')
    conn.commit()
    conn.close()


# -----------------------------
# Helper functions
# -----------------------------
def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 2) if height > 0 else 0

def calculate_calories(duration, workout):
    workout = workout.lower()
    factors = {"cardio": 8, "strength": 6, "yoga": 4}
    return duration * factors.get(workout, 5)


# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users", methods=["POST"])
def register_user():
    data = request.form
    name = data["name"]
    age = int(data["age"])
    gender = data["gender"]
    height = float(data["height"])
    weight = float(data["weight"])

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users (name, age, gender, height, weight) VALUES (?, ?, ?, ?, ?)",
              (name, age, gender, height, weight))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/workouts", methods=["POST"])
def log_workout():
    data = request.form
    name = data["name"]
    workout_type = data["workout_type"]
    duration = int(data["duration"])

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, height, weight FROM users WHERE name=?", (name,))
    user = c.fetchone()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_id, height, weight = user
    calories = calculate_calories(duration, workout_type)
    date = datetime.date.today().strftime("%Y-%m-%d")

    c.execute("INSERT INTO workouts (user_id, workout_type, duration, calories, date) VALUES (?, ?, ?, ?, ?)",
              (user_id, workout_type, duration, calories, date))
    conn.commit()
    conn.close()
    return redirect(url_for("get_user_workouts", name=name))

@app.route("/workouts/<name>")
def get_user_workouts(name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT w.date, w.workout_type, w.duration, w.calories
                 FROM workouts w JOIN users u ON w.user_id = u.id
                 WHERE u.name=?""", (name,))
    workouts = c.fetchall()
    conn.close()
    return render_template("workouts.html", name=name, workouts=workouts)

@app.route("/api/users")
def api_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

@app.route("/api/workouts")
def api_workouts():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM workouts")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

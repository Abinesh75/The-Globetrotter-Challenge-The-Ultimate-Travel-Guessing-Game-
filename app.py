from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import random
import json,os

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin@123",
        database="globetrotter_db"
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    username = data["username"]

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, score) VALUES (%s, 0)", (username,))
        conn.commit()
        response = {"message": "User registered successfully"}
    except mysql.connector.IntegrityError:
        response = {"message": "Username already exists"}
    
    cursor.close()
    conn.close()
    return jsonify(response)

@app.route('/question', methods=['GET'])
def get_question():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT city, country, clues, fun_fact FROM destinations ORDER BY RAND() LIMIT 1;")
    destination = cursor.fetchone()

    if not destination:
        return jsonify({"error": "No questions found"}), 404

    destination["clues"] = json.loads(destination["clues"])
    destination["fun_fact"] = json.loads(destination["fun_fact"])

    cursor.execute("SELECT city FROM destinations ORDER BY RAND() LIMIT 3;")
    choices = [row["city"] for row in cursor.fetchall()]
    if destination["city"] not in choices:
        choices[random.randint(0, 2)] = destination["city"]

    cursor.close()
    conn.close()

    return jsonify({
        "clues": random.sample(destination["clues"], min(2, len(destination["clues"]))),
        "correct_answer": destination["city"],
        "choices": choices,
        "fun_fact": random.choice(destination["fun_fact"])
    })

@app.route("/answer", methods=["POST"])
def check_answer():
    data = request.json
    user_answer = data["answer"]
    username = data["username"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT city, fun_fact FROM destinations WHERE city = %s;", (user_answer,))
    destination = cursor.fetchone()

    if destination:
        correct = user_answer == destination["city"]

        if correct:
            cursor.execute("UPDATE users SET score = score + 1 WHERE username = %s", (username,))
            conn.commit()

        cursor.execute("SELECT score FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        user_score = user_data["score"] if user_data else 0  

        message = {
            "correct": correct,
            "fun_fact": random.choice(json.loads(destination["fun_fact"])),
            "score": user_score
        }
    else:
        message = {
            "correct": False,
            "fun_fact": "Better luck next time!",
            "score": 0
        }

    cursor.close()
    conn.close()
    return jsonify(message)

@app.route("/score/<username>", methods=["GET"])
def get_score(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT score FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({"score": user["score"]})
    return jsonify({"error": "User not found"}), 404

@app.route("/challenge/<username>", methods=["GET"])
def generate_challenge(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT score FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if user:
        score = user["score"]
        link = f"http://127.0.0.1:5000/?challenge={username}&score={score}"
        return jsonify({"link": link})
    
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



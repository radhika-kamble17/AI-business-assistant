import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv

from services.email_service import send_lead_notification
from services.gemini_service import ask_gemini


# LOAD ENV VARIABLES

load_dotenv()


# FLASK APP

app = Flask(__name__)

app.config["DATABASE"] = os.getenv(
    "DATABASE_PATH",
    "database.db"
)


# DATABASE CONNECTION

def get_db_connection():

    connection = sqlite3.connect(
        app.config["DATABASE"]
    )

    connection.row_factory = sqlite3.Row

    return connection


# DATABASE INIT

def init_db():

    with get_db_connection() as conn:

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                email TEXT NOT NULL,

                phone TEXT NOT NULL,

                course TEXT NOT NULL,

                message TEXT,

                created_at TEXT DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        conn.commit()


# INITIALIZE DATABASE

init_db()


# HOME PAGE

@app.route("/")
def home():

    return render_template("index.html")


# CHATBOT PAGE

@app.route("/chatbot")
def chatbot_page():

    return render_template("chatbot.html")


# CHATBOT API

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    user_message = data.get(
        "message",
        ""
    ).strip()

    if not user_message:

        return jsonify({
            "reply": "Please enter a question."
        }), 400

    try:

        reply = ask_gemini(user_message)

        return jsonify({
            "reply": reply
        })

    except Exception as error:

        return jsonify({
            "reply": f"Chatbot error: {error}"
        }), 500


# SUBMIT LEAD

@app.route("/submit_lead", methods=["POST"])
def submit_lead():

    payload = request.get_json(
        silent=True
    ) or request.form

    name = payload.get(
        "name",
        ""
    ).strip()

    email = payload.get(
        "email",
        ""
    ).strip()

    phone = payload.get(
        "phone",
        ""
    ).strip()

    course = payload.get(
        "course",
        ""
    ).strip()

    message = payload.get(
        "message",
        ""
    ).strip()

    if not name or not email or not phone or not course:

        return jsonify({
            "success": False,
            "message": "Please fill all required fields."
        }), 400

    try:

        with get_db_connection() as conn:

            conn.execute(
                """
                INSERT INTO leads
                (name, email, phone, course, message)

                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    phone,
                    course,
                    message
                )
            )

            conn.commit()

        # EMAIL AUTOMATION

        try:

            send_lead_notification(
                name,
                email,
                phone,
                course,
                message
            )

        except Exception as email_error:

            app.logger.warning(
                "Email notification failed: %s",
                email_error
            )

        return jsonify({
            "success": True,
            "message": "Lead submitted successfully."
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": f"Lead submission error: {error}"
        }), 500


# DELETE LEAD

@app.route("/delete_lead", methods=["POST"])
def delete_lead():

    data = request.get_json(
        silent=True
    ) or {}

    lead_id = data.get("id")

    if not lead_id:

        return jsonify({
            "success": False,
            "message": "Lead ID required."
        }), 400

    try:

        with get_db_connection() as conn:

            conn.execute(
                "DELETE FROM leads WHERE id = ?",
                (lead_id,)
            )

            conn.commit()

        return jsonify({
            "success": True,
            "message": "Lead deleted successfully."
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": f"Delete failed: {error}"
        }), 500


# DASHBOARD

@app.route("/dashboard")
def dashboard():

    try:

        with get_db_connection() as conn:

            leads = conn.execute(
                """
                SELECT *
                FROM leads
                ORDER BY created_at DESC
                """
            ).fetchall()

    except sqlite3.Error as error:

        app.logger.error(
            "Database error: %s",
            error
        )

        leads = []

    return render_template(
        "dashboard.html",
        leads=leads
    )


# HEALTH CHECK

@app.route("/health")
def health():

    return jsonify({
        "status": "ok"
    })


# RUN APP

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=False
    )

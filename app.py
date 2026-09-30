from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db_connection
from email.message import EmailMessage
import smtplib
SENDER_EMAIL = "trex50586@gmail.com"
SENDER_APP_PASSWORD = "ucnatdsfnbrgyxjq"

app = Flask(__name__)
app.secret_key = "cyberhelpdesk_secret_key_2026"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
def send_email(to_email, subject, body):

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        smtp.send_message(msg)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask-expert", methods=["GET", "POST"])
def ask_expert():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        category = request.form["category"]
        question = request.form["question"]

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO expert_queries
        (name, email, category, question)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (name, email, category, question)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("ask_expert"))

    return render_template("ask_expert.html")


@app.route("/report-fraud")
def report_fraud():
    return render_template("report_fraud.html")


@app.route("/scam-alerts")
def scam_alerts():
    return render_template("scam_alerts.html")


@app.route("/knowledge")
def knowledge():
    return render_template("knowledge.html")


@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))

        return render_template(
            "admin_login.html",
            error="Invalid username or password"
        )

    return render_template("admin_login.html")


@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM expert_queries
        ORDER BY created_at DESC
    """)

    queries = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("admin.html", queries=queries)


@app.route("/admin/answer/<int:query_id>", methods=["POST"])
def admin_answer(query_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    answer = request.form["answer"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT email FROM expert_queries WHERE id = %s",
        (query_id,)
    )

    result = cursor.fetchone()

    if not result:
        cursor.close()
        connection.close()
        return redirect(url_for("admin"))

    query_email = result[0]

    cursor.execute("""
        UPDATE expert_queries
        SET answer = %s,
            status = 'Answered'
        WHERE id = %s
    """, (answer, query_id))

    connection.commit()

    cursor.close()
    connection.close()

    try:
        send_email(
            query_email,
            "CyberHelpdesk | Expert Response to Your Cyber Safety Query",
            f"""Hello,

Thank you for contacting CyberHelpdesk Community Helpdesk.

Your cyber safety query has been reviewed by our expert team.

Expert Response:
{answer}

Stay Safe Online!

CyberHelpdesk Community Helpdesk
"""
        )

        print("Email sent successfully!")

    except Exception as e:
        print("Email sending failed:", e)

    return redirect(url_for("admin"))

@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

@app.route("/my-query", methods=["GET", "POST"])
def my_query():

    queries = []

    if request.method == "POST":

        email = request.form["email"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM expert_queries
            WHERE email = %s
            ORDER BY created_at DESC
        """, (email,))

        queries = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template("my_query.html", queries=queries)

if __name__ == "__main__":
    app.run(debug=True)
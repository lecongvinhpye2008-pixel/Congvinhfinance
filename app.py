from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "congvinh_secret"

def get_db():
    return sqlite3.connect("users.db")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()
        db.close()

        if user:
            session["user"] = username
            session["role"] = user[0]
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        phone = request.form["phone"]
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO users (username, password, phone, role) VALUES (?,?,?,?)",
            (username, password, phone, "staff")
        )
        db.commit()
        db.close()

        return redirect("/")

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template(
        "dashboard.html",
        user=session["user"],
        role=session["role"]
    )


@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/")

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT username, phone, role FROM users")
    users = cur.fetchall()
    db.close()

    return render_template("admin.html", users=users)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from db import create_tables, create_user, get_user_by_email, get_user_by_username

app = Flask(__name__)

create_tables()


# Welcome page
@app.route("/")
def home():
    return render_template("index.html")


# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user_by_email = get_user_by_email(email)
        existing_user_by_username = get_user_by_username(username)

        if existing_user_by_email:
            return "Email already exists"

        if existing_user_by_username:
            return "Username already exists"

        password_hash = generate_password_hash(password)
        create_user(username, email, password_hash)

        return redirect(url_for("home"))

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
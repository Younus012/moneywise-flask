from flask import Flask, render_template, request,session,redirect,flash
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash,generate_password_hash
import sqlite3
from datetime import date

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"]="filesystem"
Session(app)
app.secret_key = "super_secret_key"

db = SQL("sqlite:///budget.db")


def get_db_connection():
    conn = sqlite3.connect("budget.db")
    conn.row_factory = sqlite3.Row
    return conn






@app.route("/")
def index():
    budget = []
    if "user_email" in session:
        nusername_result = db.execute("SELECT username FROM users WHERE email = ?", session["user_email"])
        if nusername_result:
            nusername = nusername_result[0]["username"]
            budget = db.execute("SELECT * FROM budgetss WHERE nusername = ? ORDER BY id DESC", nusername)
    else:
            budget = db.execute("SELECT * FROM b ORDER BY id DESC")
            print("hi")

    return render_template("index.html",email=session.get("email"),budget=budget)

@app.route("/login",methods=["GET","POST"])
def login():

    if request.method == "POST":
        session["user_email"] = request.form.get("email")
        password= request.form.get("pasword")

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users where email = ?",(session["user_email"],)).fetchone()
        conn.close()
        if user and password==user["password_hash"]:
            session["user_id"]=user["id"]
            session["email"]=user["username"]
            flash("Log in Succesful!")
            return redirect("/")
        else:
            flash("Invalid Username or password!")
            return redirect("/login")
    return render_template("login.html")


@app.route("/income",methods=["GET", "POST"])
def income():

    type= request.form.get("t_type")
    category = request.form.get("category")
    amount = request.form.get("amount")
    today = date.today().isoformat()
    if type=="Income":
        budget = db.execute("INSERt INTO budgetss (nusername,date,type,category,amount)   VALUES(?);",(session["email"],today,type,category,amount))
        return redirect("/")
    elif type=="Expense":
        budget = db.execute("INSERt INTO budgetss (nusername,date,type,category,amount)   VALUES(?);",(session["email"],today,type,category,amount))
        return redirect("/")

    return render_template("income.html")

@app.route("/expense",methods=["GET", "POST"])
def expense():
    return render_template("expense.html")





@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

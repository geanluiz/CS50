import os
import sys
import time

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute(
        "SELECT * FROM portfolio WHERE user = ?", session["user_id"]
    )

    s_total = 0

    for stock in stocks:
        s_price = lookup(stock['symbol'])['price']
        stock['price'] = usd(s_price)
        stock['total'] = usd(s_price * stock['qty'])
        s_total += s_price * stock['qty']

    user_cash = db.execute(
        "SELECT cash FROM users WHERE id = ?", session["user_id"]
    )[0]['cash']

    cash = usd(user_cash)
    user_total = usd(user_cash + s_total)

    return render_template("index.html", stocks=stocks, cash=cash, user_total=user_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        """error handling for user input"""
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol")

        stock = lookup(symbol)
        if stock == None:
            return apology("invalid symbol")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("invalid number of shares")

        if shares < 0:
            return apology("invalid number of shares")

        """perform buy"""
        total_value = stock['price'] * shares
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )[0]['cash']

        if user_cash < total_value:
            return apology("can't afford")

        """updates user cash avaliable according to transaction"""
        update_user_cash = db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", (user_cash - total_value), session["user_id"]
        )

        update_transaction_table = db.execute(
            """INSERT INTO transactions (user, t_type, price, qty, symbol, t_timestamp)
            VALUES(?, ?, ?, ?, ?, ?)""", session["user_id"], "BUY", stock['price'],
            shares, stock['symbol'], int(time.time())
        )

        update_user_portfolio = db.execute(
            """INSERT INTO portfolio (user, symbol, qty) VALUES (?, ?, ?)
            ON CONFLICT (symbol) DO UPDATE SET qty = (qty + ?)""",
            session["user_id"], stock['symbol'], shares, shares
        )

        flash("Bought!")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks = db.execute(
        "SELECT * FROM transactions WHERE user = ?", session["user_id"]
    )

    for stock in stocks:
        db_timestamp = time.localtime(stock['t_timestamp'])
        stock['t_timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', db_timestamp)
        stock['price'] = usd(stock['price'])
        if stock['t_type'] == "SELL":
            stock['qty'] = -stock['qty']

    return render_template("history.html", stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        stock_id = lookup(request.form.get("symbol"))
        if not stock_id or stock_id == None:
            return apology("invalid symbol")

        name = stock_id["name"]
        symbol = stock_id["symbol"]
        price = usd(stock_id["price"])
        return render_template("quoted.html", name=name, symbol=symbol, price=price)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        hash1 = generate_password_hash(request.form.get("password"))
        hash2 = request.form.get("confirmation")

        if not check_password_hash(hash1, hash2):
            return apology("passwords do not match", 400)

        # Query database for username
        try:
            id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
                    "username"), hash1
            )
        except ValueError:
            return apology("user already registered")

        session["user_id"] = id

        # Redirect user to login page
        flash("Registered!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password_change():
    """lets user change their password"""
    if request.method == "POST":
        # Ensure password was submitted
        current = request.form.get("current")
        if not current:
            return apology("must provide password", 403)

        user_pass = db.execute(
            "SELECT hash FROM users WHERE id = ?", session['user_id']
        )[0]['hash']

        if not check_password_hash(user_pass, current):
            return apology("wrong password", 403)

        if not request.form.get("password"):
            return apology("must provide password", 403)

        hash1 = generate_password_hash(request.form.get("password"))
        hash2 = request.form.get("confirmation")

        if not check_password_hash(hash1, hash2):
            return apology("passwords do not match", 403)

        id = db.execute(
            "UPDATE users SET hash = ? WHERE id = ?", hash1, session['user_id']
        )

        return redirect("/")

    else:
        return render_template("/password.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        """Error handling for user inputs"""
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol")

        stock = lookup(symbol)
        if stock == None:
            return apology("invalid symbol")

        shares = int(request.form.get("shares"))
        if not shares:
            return apology("missing shares")

        if shares < 0:
            return apology("invalid number of shares")

        user_shares_qty = db.execute(
            "SELECT qty FROM portfolio WHERE user = ? AND symbol = ?", session["user_id"], symbol
        )[0]['qty']

        if user_shares_qty < shares:
            return apology("too many shares")

        """Perform sell"""
        total_value = stock['price'] * shares
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )[0]['cash']

        update_user_cash = db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", (user_cash + total_value), session["user_id"]
        )

        update_transaction_table = db.execute(
            """INSERT INTO transactions (user, t_type, price, qty, symbol, t_timestamp)
            VALUES(?, ?, ?, ?, ?, ?)""", session["user_id"], "SELL", stock['price'],
            shares, stock['symbol'], int(time.time())
        )

        update_user_portfolio = db.execute(
            """UPDATE portfolio SET qty = (qty - ?) WHERE user = ? AND symbol = ?""",
            shares, session["user_id"], stock['symbol']
        )

        """Excludes entry from portfolio if qty == 0"""
        user_shares_qty = db.execute(
            "SELECT qty FROM portfolio WHERE user = ? AND symbol = ?", session["user_id"], stock['symbol']
        )[0]['qty']

        if user_shares_qty == 0:
            delete_from_user_portfolio = db.execute(
                """DELETE FROM portfolio WHERE user = ? AND symbol = ?""",
                session["user_id"], stock['symbol']
            )

        flash("Sold!")
        return redirect("/")

    else:
        stocks = db.execute(
            "SELECT symbol FROM portfolio WHERE user = ?", session["user_id"]
        )
        return render_template("sell.html", stocks=stocks)

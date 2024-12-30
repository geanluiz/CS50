import time
from functools import wraps
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from math import floor
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("sqlite:///products.db")
db = scoped_session(sessionmaker(bind=engine))


# Formatting functions
def usd(value):
    """Format value as BRL."""
    return f"${value:,.2f}"

def date_format(pattern, value):
    """Formats dates."""
    return time.strftime(pattern, time.localtime(value))

app.jinja_env.globals.update(usd=usd, date_format=date_format)



# Routes
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", error="must provide username")

        # Ensure password was submitted
        if not request.form.get("password"):
            return render_template("apology.html", error="must provide password")

        # Query database for username
        rows = db.execute(text(
            "SELECT * FROM users WHERE username = :user",
        ), {"user": request.form.get("username")}).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0].pwd, request.form.get("password")
        ):
            return render_template("apology.html", error="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0].id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")


def login_required(f):
    """Decorate routes to require login."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()


    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", error="must provide username")

        name = db.execute(text(
            "SELECT username FROM users WHERE username = :name"
        ), {"name": request.form.get("username")}).fetchall()

        if name:
            return render_template("apology.html", error=f"'{name[0].username}' is already taken")


        # Ensure password was submitted
        if not request.form.get("password"):
            return render_template("apology.html", error="must provide password")

        hash1 = generate_password_hash(request.form.get("password"))
        hash2 = request.form.get("confirmation")

        if not check_password_hash(hash1, hash2):
            return render_template("apology.html", error="passwords do not match")


        # Tries to add new user
        try:
            id = db.execute(text(
                "INSERT OR IGNORE INTO users (username, pwd) VALUES (:user, :pwd)"
            ), {"user" : request.form.get("username"), "pwd": hash1}).lastrowid
            db.commit()
        except ValueError:
            return render_template("apology.html", error="user already registered")

        # Logs new user
        session["user_id"] = id


        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/", methods=["GET"])
@login_required
def index():
    """Render the index page"""

    # Loads all categories and products from the database
    categories = db.execute(text(
        "SELECT id, cat_name AS name FROM categories"
    )).fetchall()
    db.commit()

    products = db.execute(text(
        """SELECT history.id AS hist_id, items.id, item_name AS name, cat_name AS category, price, t_date, username FROM history
            JOIN users ON user_id = users.id
            JOIN items ON item_id = items.id
            JOIN categories ON items.cat_id = categories.id
            WHERE user_id = :user
            ORDER BY t_date DESC"""
    ), {"user": session["user_id"]}).fetchall()
    db.commit()


    # Checks if user is logged and returns its username to the sidebar
    try:
        username = db.execute(text(
            "SELECT username FROM users WHERE id = :id"
        ), {"id": session['user_id']}).fetchone().username
    except:
        session.clear()
        return redirect("/")


    return render_template("index.html", products=products, categories=categories, username=username)


@app.route("/add_product", methods=["POST"])
@login_required
def add_product():
    """Adding a product to the database"""

    # Loads all categories and products from the database
    products = db.execute(text(
        """SELECT history.id AS hist_id, items.id AS item_id, item_name AS name, cat_name AS category, price FROM history
            JOIN users ON user_id = users.id
            JOIN items ON item_id = items.id
            JOIN categories ON items.cat_id = categories.id
            WHERE user_id = :user
            ORDER BY t_date DESC"""
    ), {"user": session["user_id"]}).fetchall()
    db.commit()


    # Check if the category and product already exists
    name = None
    id = None
    category = None

    for product in products:
        if product.name == request.form.get("name").lower():
            name = product.name
            id = product.item_id

    for product in products:
        if product.category == request.form.get("category").lower():
            category = product.category

    # Creates new category/product if it doesn't exists
    if category == None:
        db.execute(text(
            "INSERT OR IGNORE INTO categories (cat_name) VALUES (:category)"
        ), {"category": request.form.get("category").lower()})
        db.commit()

    if name == None:
        db.execute(text(
            """INSERT OR IGNORE INTO items (item_name, cat_id) VALUES (:item,
            (SELECT id FROM categories WHERE cat_name = :cat))"""
        ), {"item": request.form.get("name").lower(), "cat": request.form.get("category").lower()})
        db.commit()

    id = db.execute(text(
        "SELECT id FROM items WHERE item_name = :name"
    ), {"name": request.form.get("name").lower()}).fetchone().id


    # Stores date and price
    if request.form.get("date") == None:
        date = ""
    else:
        date = int(time.mktime(time.strptime(request.form.get("date"), "%Y-%m-%d")))

    price = float(request.form.get("price"))


    # Inserts item to user history
    db.execute(text(
        """INSERT OR IGNORE INTO history (user_id, item_id, t_date, price) VALUES (:user, :item, :date, :price)"""
        ), {"user": session["user_id"], "item": id, "date": date, "price": price})
    db.commit()
    return redirect("/")

@app.route("/delete/<id>")
@login_required
def delete_product(id):
    """Delete a product from the database"""

    # Loads all categories and products from the database
    products = db.execute(text(
        """SELECT history.id AS hist_id
            FROM history
            JOIN users ON user_id = users.id
            JOIN items ON item_id = items.id
            JOIN categories ON items.cat_id = categories.id
            WHERE user_id = :user
            ORDER BY t_date DESC"""
    ), {"user": session["user_id"]}).fetchall()


    # Deletes the selected product from db
    selected = None
    for product in products:
        if product.hist_id == int(id):
            selected = product

    db.execute(text(
        "DELETE FROM history WHERE id = :id"
    ), {"id": selected.hist_id})
    db.commit()

    return redirect("/")


@app.route("/product", methods=["GET"])
@login_required
def product():
    """render the product details in the index page"""

    # Loads all categories and products from the database
    categories = db.execute(text(
        "SELECT id, cat_name AS name FROM categories"
    )).fetchall()

    products = db.execute(text(
        """SELECT history.id AS hist_id, items.id, item_name AS name, cat_name AS category, price, t_date, username FROM history
            JOIN users ON user_id = users.id
            JOIN items ON item_id = items.id
            JOIN categories ON items.cat_id = categories.id
            WHERE user_id = :user
            ORDER BY t_date DESC"""
    ), {"user": session["user_id"]}).fetchall()


    # Calculates average days between each buy
    selected = None
    dt_diff = []

    for product in products:
        if product.hist_id == int(request.args.get("id")):
            selected = product

    for product in products:
        if product.name == selected.name:
            dt_diff.append(floor(int(product.t_date) / 86400))


    dt_sum = 0
    count = 0
    for i in range(len(dt_diff)):
        if i + 1 < len(dt_diff):
            dt_sum += dt_diff[i] - dt_diff[i + 1]
            count += 1

    try:
        avg_days = int(dt_sum / count)
    except ZeroDivisionError:
        avg_days = 0

    # TODO: change username return logic ####################

    return render_template("index.html", selected_product=selected, products=products, categories=categories, avg_days=avg_days, username=products[0].username)


@app.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_product(id):
    """Edit a product in the database"""

    # Loads all products from the database
    products = db.execute(text(
        """SELECT history.id AS hist_id, items.id AS item_id, item_name AS name, cat_name AS category, price, t_date FROM history
            JOIN users ON user_id = users.id
            JOIN items ON item_id = items.id
            JOIN categories ON items.cat_id = categories.id
            WHERE user_id = :user
            ORDER BY t_date DESC"""
    ), {"user": session["user_id"]}).fetchall()

    categories = db.execute(text(
        "SELECT id, cat_name AS name FROM categories"
    )).fetchall()

    # Selects the product user has chose to edit
    selected = None
    for product in products:
        if product.hist_id == int(id):
            selected = product

    # Returns the modal with the selected product's data
    if request.method == "GET":
        return render_template("modal.html", selected_product=selected, categories=categories)

    # If request method is POST
    else:
        # Checks if the category and/or product already exists
        if request.form.get("name") != selected.name:

            category = None

            for product in products:
                if product.category == request.form.get("category").lower():
                    category = product.category

            if category == None:
                db.execute(text(
                    "INSERT OR IGNORE INTO categories (cat_name) VALUES (:category)"
                ), {"category": request.form.get("category").lower()})
                db.commit()

            db.execute(text(
                """INSERT OR IGNORE INTO items (item_name, cat_id) VALUES (:item,
                (SELECT id FROM categories WHERE cat_name = :cat))"""
            ), {"item": request.form.get("name").lower(), "cat": request.form.get("category").lower()})
            db.commit()

        item_id = db.execute(text(
            "SELECT id FROM items WHERE item_name = :name"
        ), {"name": request.form.get("name").lower()}).fetchone().id


        # Stores date and price according to user input
        if request.form.get("date") == None:
            date = ""
        else:
            date = int(time.mktime(time.strptime(request.form.get("date"), "%Y-%m-%d")))

        price = float(request.form.get("price"))

        # Tries to update current history entry if item is the same
        try:
            db.execute(text(
                """UPDATE history (item_id, t_date, price) VALUES (:user, :item, :date, :price)
                WHERE id = :id"""
                ),{"item": item_id, "date": date, "price": price, "id": id})
            db.commit()

        # Inserts new history entry and deletes current, as user has changed the item name/category
        except:
            db.execute(text(
                """INSERT OR IGNORE INTO history (user_id, item_id, t_date, price) VALUES (:user, :item, :date, :price)"""
                ), {"user": session["user_id"], "item": item_id, "date": date, "price": price})
            db.execute(text(
                "DELETE FROM history WHERE id = :id"
                ), {"id": id})
            db.commit()

    return redirect("/")

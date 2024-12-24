from flask import Flask, redirect, render_template, request
from flask_session import Session
import time
import math

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker


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
def brl(value):
    """Format value as BRL."""
    return f"R${value:,.2f}"

def date_format(value):
    """Format value as time."""
    return time.strftime("%d/%m/%Y", time.localtime(value))

app.jinja_env.globals.update(brl=brl, date_format=date_format)


# Routes
@app.route("/", methods=["GET"])
def index():
    """render the index page"""
    
    # Loads all categories and products from the database
    categories = db.execute(text(
        "SELECT id, cat_name AS name FROM categories"
    )).fetchall()



    products = db.execute(text(
        """SELECT history.id AS hist_id, items.id, item_name AS name, cat_name AS category, price, t_date FROM history 
            JOIN users ON user_id = users.id 
            JOIN items ON item_id = items.id 
            JOIN categories ON items.cat_id = categories.id
            WHERE user_id = :user"""
    ), {"user": 1}).fetchall() 

    return render_template("index.html", products=products, categories=categories)


@app.route("/add_product", methods=["POST"])
def add_product():
    """Add a product to the database""" 

    # Loads all categories and products from the database
    products = db.execute(text(
        """SELECT history.id AS hist_id, items.id, item_name AS name, cat_name AS category, price FROM history 
            JOIN users ON user_id = users.id 
            JOIN items ON item_id = items.id 
            JOIN categories ON items.cat_id = categories.id
            WHERE user_id = :user"""
    ), {"user": 1}).fetchall() 

    # Check if the category and product already exists
    name = None

    for product in products:
        if product.name == request.form.get("name"):
            name = product.name
            id = product.id
        if product.category == request.form.get("category"):
            category = product.category
    
    if not category:
        db.execute(text(
            "INSERT INTO categories (cat_name) VALUES (:category)"
        ), {"category": request.form.get("category")})
        db.commit()
    
    if name == None:
        name_query = db.execute(text(
            """INSERT INTO items (item_name, cat_id) VALUES (:item, 
            (SELECT id FROM categories WHERE cat_name = :cat))"""
        ), {"item": request.form.get("name"), "cat": request.form.get("category")})
        db.commit()
        id = name_query.lastrowid


    if request.form.get("date") == None:
        date = ""
    else:
        date = int(time.mktime(time.strptime(request.form.get("date"), "%Y-%m-%d")))

    price = float(request.form.get("price"))

    db.execute(text(
        """INSERT INTO history (user_id, item_id, t_date, price) VALUES (:user, :item, :date, :price)"""
        ), {"user": 1, "item": id, "date": date, "price": price})
    db.commit()
    return redirect("/")


@app.route("/product", methods=["GET"])
def product():
    """render the product details in the index page"""
  
    # Loads all categories and products from the database
    categories = db.execute(text(
        "SELECT id, cat_name AS name FROM categories"
    )).fetchall()

    products = db.execute(text(
        """SELECT history.id AS hist_id, items.id, item_name AS name, cat_name AS category, price, t_date FROM history 
            JOIN users ON user_id = users.id 
            JOIN items ON item_id = items.id 
            JOIN categories ON items.cat_id = categories.id
            WHERE user_id = :user
            ORDER BY t_date"""
    ), {"user": 1}).fetchall() 
    
    selected = None
    dt_diff = []

    for product in products:
        if product.hist_id == int(request.args.get("id")):
            selected = product

    for product in products:
        if product.name == selected.name:
            dt_diff.append(math.floor(int(product.t_date) / 86400))


    dt_sum = 0
    count = 0
    for i in range(len(dt_diff)):
        if i + 1 < len(dt_diff):
            dt_sum += dt_diff[i + 1] - dt_diff[i]
            count += 1

    try:
        avg_days = int(dt_sum / count)
    except ZeroDivisionError:
        avg_days = 0
    
    return render_template("index.html", selected_product=selected, products=products, categories=categories, avg_days=avg_days)
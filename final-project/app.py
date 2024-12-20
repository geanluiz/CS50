from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import time
import os
import sys

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


def brl(value):
    """Format value as BRL."""
    return f"R${value:,.2f}"

app.jinja_env.globals.update(brl=brl)


@app.route("/", methods=["GET", "POST"])
def index():
    products = db.execute(text(
        """SELECT items.id AS id, item_name AS name, cat_name AS category, price FROM history 
            JOIN users ON user_id = users.id 
            JOIN items ON item_id = items.id 
            JOIN categories ON items.cat_id = categories.id
            WHERE user_id = :user"""
    ), {"user": 1}).fetchall()
    
    categories = db.execute(text(
        "SELECT id, cat_name AS name FROM categories"
    )).fetchall()
    
    return render_template("index.html", products=products, categories=categories)


@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form.get("name")

    item_query = db.execute(text(
        "SELECT id FROM items WHERE item_name = :item"
    ), {"item": name}).fetchone()
    
    category = request.form.get("category")

    cat_query = db.execute(text(
        "SELECT id FROM categories WHERE cat_name = :cat"
    ), {"cat": category}).fetchone()

    if item_query == None:
        db.execute(text(
            "INSERT INTO categories (cat_name) VALUES (:category)"
        ), {"category": category})
        db.execute(text(
            """INSERT INTO items (item_name, cat_id) VALUES (:item, 
            (SELECT id FROM categories WHERE cat_name = :cat))"""
        ), {"item": name, "cat": category})
        db.commit()
    
    id = 1
    date = request.form.get("date")
    price = float(request.form.get("price"))

    db.execute(text(
        """INSERT INTO history (user_id, item_id, t_date, price) VALUES (:user, :item, :date, :price)"""
        ), {"user": 1, "item": id, "date": date, "price": price})
    db.commit()
    return redirect("/")


@app.route("/product", methods=["GET", "POST"])
def product():
    products = db.execute(text(
        """SELECT items.id AS id, item_name AS name, cat_name AS category, price FROM history 
            JOIN users ON user_id = users.id 
            JOIN items ON item_id = items.id 
            JOIN categories ON items.cat_id = categories.id
            WHERE user_id = :user"""
    ), {"user": 1}).fetchall()

    for product in products:
        if product.id == int(request.args.get("id")):
            selected = product

    return render_template("index.html", selected_product=selected, products=products)
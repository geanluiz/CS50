from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sys

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

products = [
    {
        "id": 0,
        "name": "arroz",
        "category": 1,
        "price": 4,
        "date": "12/12/2024",
    },
    {
        "id": 1,
        "name": "arroz",
        "category": 1,
        "price": 4,
        "date": "12/11/2024",
    }
]

def brl(value):
    """Format value as BRL."""
    return f"R${value:,.2f}"

@app.route("/", methods=["GET", "POST"])
def index():
    # print(products[0], file=sys.stderr)
    index = int(request.args.get("id"))
    return render_template("index.html", selected_product=products[index], products=products)

new_product = {}

@app.route("/add_product", methods=["POST"])
def add_product():
    price = brl(float(request.form.get("price")))
    new_product = {
        "id": len(products),
        "name": request.form.get("name"),
        "category": request.form.get("category"),
        "price": price,
        "date": request.form.get("date")
    }
    products.append(new_product)
    return redirect("/")
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import statistics
import time

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
        "price": "R$4.00",
        "date":  time.strptime("12/12/2024", "%d/%m/%Y")
    },
    {
        "id": 0,
        "name": "arroz",
        "category": 1,
        "price": "R$10.00",
        "date": time.strptime("12/11/2024", "%d/%m/%Y")
    }
]

def brl(value):
    """Format value as BRL."""
    return f"R${value:,.2f}"

@app.route("/", methods=["GET", "POST"])
def index():
    # print(products[0], file=sys.stderr)
    return render_template("index.html", products=products)

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


@app.route("/product", methods=["GET", "POST"])
def product():
    selected = products[int(request.args.get("id"))]
    """ avg = []
    for product in products:
        avg += product['date']
    average_days = avg / len(products) """
    return render_template("index.html", selected_product=selected, products=products)
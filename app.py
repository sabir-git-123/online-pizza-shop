import json
import os
import sqlite3

from flask import Flask, render_template, request

def save_order(order):
    con = sqlite3.connect("orders.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO orders(name,drink,flavor,topping,topping,topping,topping) VALUES(?,?,?,?,?,?,?);",
        (order["name"], order["filling"], order["sauce"], order["size1"], order["size2"], order["acute"], order["drink"]),
    )
    con.commit()
    return

def get_orders():
    con = sqlite3.connect("orders.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM orders;")
    rows = cur.fetchall()

    return rows



def read_menu(filename):
    try:
        with open(filename) as f:
            result = [item.strip() for ite in f.readlines()]
    except FileNotFoundError:
        print(
        f"Error: The file '{filename}' could not be found.")
        result = []
    except PermissionError:
        print(f"Error: You do not have permission to read \
        the file '{filename}'.")
        result = []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        result = []

    return result

filling = read_menu("filling.txt")
sauce = read_menu("sauce.txt")
size1 = read_menu("size1.txt")
size2 = read_menu("size2.txt")
acute = read_menu("acute.txt")
drink = read_menu("drink.txt")

con = sqlite3.connect("orders.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS orders(name, filling, sauce, size1, size2, acute, drink);")
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/hello/<name>')
def greet(name='Stranger'):
    return render_template("greeting.html", name=name)

@app.route('/order', methods=('GET', 'POST'))
def order():
    if request.method == 'POST':
        new_order = {"name": request.form["name"],
                     "filling": request.form["filling"],
                     "sauce": request.form["sauce"],
                     "size1": request.form["size1"],
                     "size2": request.form["size2"],
                     "acute": request.form["acute"],
                     "drink": request.form["drink"],
                     }
        save_order(new_order)
        return render_template(
            "print.html", new_order=new_order
          )
    return render_template("order.html", filling=filling, sauce=sauce, size1=size1, size2=size2, acute=acute, drink=drink )


@app.route("/list", methods=["GET"])
def list():
    orders = get_orders()

    return render_template("list.html", orders=orders)



def read_menu(filename):
    f = open(filename)
    temp = f.readlines()
    result = []
    for item in temp:
        new_item = item.strip()
        result.append(new_item)

    return result



from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

import urllib.parse
from combo_operations import fetch_products_for_combo, generate_combos, rank_combos

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MongoDB connection setup
username = "shriraamsj21"
password = "Sharan@123"
encoded_password = urllib.parse.quote_plus(password)
uri = f"mongodb+srv://{username}:{encoded_password}@cluster21.jhxmf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

# Configure MongoDB in Flask
app.config["MONGO_DB"] = client.get_database("vishaal_de_mall")
users_collection = app.config["MONGO_DB"]["users"]
products_collection = app.config["MONGO_DB"]["products"]

# Routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/payment")
def payment():
    return render_template("payment.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        # Query the database for user credentials
        user = users_collection.find_one({"email": email, "password": password})
        if user:
            session["user_id"] = str(user["_id"])  # Store user session
            return redirect(url_for("home"))
        else:
            return "Invalid credentials. Please try again.", 401

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        
        # Check if email already exists in the database
        if users_collection.find_one({"email": email}):
            return "Email already registered.", 400

        # Insert new user into the database
        users_collection.insert_one({"name": name, "email": email, "password": password})
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/combos", methods=["GET", "POST"])
def combos():
    # Get budget and category from the user input (query parameters)
    budget = int(request.args.get("budget", 1000))  # Default budget is 1000
    category = request.args.get("category", "")  # Default category is empty
    
    # Fetch products based on the budget and category
    products = fetch_products_for_combo(budget, category)
    
    if not products:
        return "No products found for the given budget and category.", 404
    
    # Generate all valid combos based on the products
    combos_list = generate_combos(products, budget)
    
    # Rank the combos (if needed)
    ranked_combos = rank_combos(combos_list)
    
    # Return the ranked combos in the response
    return render_template("combo_view.html", combos=ranked_combos, budget=budget, category=category)



@app.route("/logout")
def logout():
    session.pop("user_id", None)  # Clear session
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

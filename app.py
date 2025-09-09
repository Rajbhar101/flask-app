from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import json, os

app = Flask(__name__)

MONGO_URI = "mongodb://localhost:27017/flaskdb"

client = MongoClient(MONGO_URI)
db = client.get_database()

# ✅ Load JSON data from file
@app.route('/api')
def get_data():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        return jsonify(data)   # ✅ FIXED
    except Exception as e:
        return jsonify({"error": str(e)})

# ✅ MongoDB Atlas Connection (Update with your credentials)
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["flaskDB"]
collection = db["users"]

# ✅ Homepage with form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]

            # Insert into MongoDB Atlas
            collection.insert_one({"name": name, "email": email})
            return redirect(url_for("success"))
        except Exception as e:
            return render_template("error.html", error=str(e))
    return render_template("index.html")

# ✅ Success page
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)


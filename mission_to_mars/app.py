from flask import Flask 
from flask import render_template
from flask import redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    destination_data = mongo.db.collection.find_one()
    return render_template("index.html", mars=destination_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    final_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, final_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

# import necessary libraries
from flask import Flask, render_template, redirect
import mission_to_mars
#from flask_cors import CORS
from flask_pymongo import PyMongo

# create instance of Flask app
app = Flask(__name__)

# initialize the Flask-Cors extension with 
# default arguments in order to allow CORS for all domains on all routes.
#CORS(app)

# The default port used by MongoDB is 27017
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_mars")

@app.route("/")
def index():
    # Find one record of data from the mongo database
    mars = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html", mars=mars)


# create route that renders index.html template
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = mission_to_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

# Create a route called /scrape and store value in 
# Mongo as Python Dict

# Dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
mars_db = mongo.db.mars

# root route that queries Mongo DB and pass in Mars Data as HTML
@app.route("/")
def index():
    scraped_data_from_db = mars_db.find_one()
    return render_template("index.html", mars=scraped_data_from_db)

# /scrape route with Mongo storage.  
@app.route("/scrape")
def scrape():
    scraped_data = scrape_mars.scrape_all()
    mars_db.update({}, scraped_data, upsert=True)
    return redirect('/')

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True) # set to false if deploying to a live website server (such as Google Cloud, Heroku, or AWS Elastic Beanstaulk)
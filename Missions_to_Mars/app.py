from flask import Flask, render_template, redirect
# Import the pymongo library, which lets us connect our Flask app to the Mongo Database
import pymongo
from flask_pymongo import PyMongo

# From the separate python file in this directory, we'll import the code that is
# used to scrape craigslist
import scrape_mars_test

# Create and instance of the Flask app
app = Flask(__name__)

#######################################################
# Create variable for the connection string
conn = "mongodb://localhost:27017"

# Pass connection string to the pymongo instance
client = pymongo.MongoClient(conn)


# Connect to a database.
# If the database doesn't already exist, our code will create it automatically as
# soon as we insert a record.
db = client.web_scraping_hw_12_mission_to_mars

# Drop collection if avaiable to remove duplicates
# NOTE: This is only for demo purposes.
db.mars_info.drop()
#######################################################

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/web_scraping_hw_12_mission_to_mars"
mongo = PyMongo(app)

# Identify the collection and drop any existing data for this demonstration
listings = mongo.db.planet_info
listings.drop()

# Render the index.html page.
# If there are no listings, the table will be empty.


@app.route("/")
def index():
    news_title = "From the NASA Mars Webpage:"
    # list_of_dicts = scrape_mars_test.scrape()

    # listing_results = listings.find()
    return render_template("index.html", news_title_html=news_title)
    # return redirect("/")


# This route will trigger the webscraping, but it will then send us back to the
# index route to render the results
@app.route("/scrape")
def scraper():

    # scrape_mars_test.scrape() is a custom function that we've defined in the
    # scrape_mars_test.py file within this directory
    #
    #
    # scrape_mars_test.scrape()
    listings_data = scrape_mars_test.scrape()
    listings.insert_one(listings_data)
    #
    #
    # Use Flask's redirect function to send us to a different route once this
    # task has completed.
    # db.mars_info.drop()

    #######################################################
    # db.mars_info.insert_many(scrape_mars_test.scrape())
    #######################################################
    # news_title = "From the NASA Mars Webpage:"
    # list_of_dicts = scrape_mars_test.scrape()

    return render_template("scrape.html", list_of_dicts_html=listings_data)


if __name__ == "__main__":
    app.run(debug=True)

# import dependencies
import scrape_mars
from flask import Flask, render_template, redirect
import pymongo

# initialize the flask app
app = Flask(__name__)

# set up the MongoDB client
connStr = "mongodb://localhost:27017"
client = pymongo.MongoClient(connStr)

# connect to the database (create if doesn't exist)
db = client.mission_to_mars

# connect to the collection (create if doesn't exist)
collection = db.planet_data

# home
@app.route("/")
def index():
    
    # retrieve data from the database
    data = collection.find()
    
    # pass the information to render_template
    return render_template("index.html", mars_data = data)

# command to reacquire data
@app.route("/scrape")
def scrape():
    
    # acquire scraped data
    scraped_data = scrape_mars.scrape()
    
    # update the data
    collection.insert_many(scraped_data)
    
    # return the success message to our page
    return redirect("/", code = 302)

# run the flask app
if __name__ == "__main__":
    app.run(debug = True)
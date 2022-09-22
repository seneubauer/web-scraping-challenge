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
    data = collection.find_one()
    
    # check if the returned data is null
    if data is None:
        data = {"nasa_mars_news": {"title": "news_title", "paragraph": "news_paragraph"},
                "jpl_mars_space_images": "https://picsum.photos/400/400",
                "mars_facts": "<p>table_html</p>",
                "mars_hemispheres": [{"title": "img_title0", "img_url": "https://picsum.photos/400/400"},
                                     {"title": "img_title1", "img_url": "https://picsum.photos/400/400"},
                                     {"title": "img_title2", "img_url": "https://picsum.photos/400/400"},
                                     {"title": "img_title3", "img_url": "https://picsum.photos/400/400"}]}
    
    # pass the information to render_template
    return render_template("index.html", mars_data = data)

# command to reacquire data
@app.route("/scrape")
def scraper():
    
    # acquire scraped data
    scraped_data = scrape_mars.scrape()
    
    # update the data
    collection.update_one({}, {"$set": scraped_data}, upsert = True)
    
    # return the success message to our page
    return redirect("/", code = 302)

# run the flask app
if __name__ == "__main__":
    app.run(debug = True)
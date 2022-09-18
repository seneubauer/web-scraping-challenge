# import dependencies
import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# # initialize the flask app
# app = Flask(__name__)

# # set up a connection to MongoDB
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
# mongo = PyMongo(app)

returned_data = scrape_mars.scrape()
print(returned_data[0])
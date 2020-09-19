from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars
import os 

#Creating a Flask instance 
app = Flask(__name__)

#Using flask_pymongo to set up mongo connect
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# set database 
db=client.mars_app

#Route to configure index.html template with Mongo data
@app.route("/")
def index():
    #Finding one record from mongodb
    mars = mongo.db.mars_dict.find_one()
    
    #Return template with data
    return render_template("index.html", mars_dict = mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    
    #Updating Mongodb using update and upsert
    mars.update({}, mars_data, upsert=True)
    
    return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug=True)
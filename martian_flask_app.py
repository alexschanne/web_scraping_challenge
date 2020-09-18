  
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import martian_scrape

#Creating a Flask instance 
app = Flask(__name__)

#Using flask_pymongo to set up mongo connect
app.config["MONGO_URI"] = "mongodb://localhost:8805/martian_flask_app"
mongo = PyMongo(app)

#Route to configure index.html template with Mongo data
@app.route("/")
def index():
    #Finding one record from mongodb
    mars_dict = mongo.db.mars_dict.find_one()
    
    #Return template with data
    return render_template("index.html", mars = mars_dict)

@app.route("/scrape")
def scrape():
    mars_dict = mongo.db.mars_dict
    mars_data = martian_scrape.scrape()
    
    #Updating Mongodb using update and upsert
    mars_dict.update({}, mars_data, upsert=True)
    
    return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug=True)
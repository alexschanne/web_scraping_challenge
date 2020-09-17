  
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import martian_scrape

#Creating a Flask instance 
app = Flask(__name__)

#Using flask_pymongo to set up mongo connect
app.config["MONGO_URI"] = "mongodb://localhost:8805/mars_app"
mongo = PyMongo(app)

#Route to configure index.html template with Mongo data
@app.route("/")
def index():
    #Finding one record from mongodb
    martian_dict = mongo.db.martian_dict.find_one()
    #Return template with data
    return render_template("index.html", mars = martian_dict)

@app.route("/scrape")
def scrape():
    martian_dict = mongo.db.martian_dict
    martian_data = martian_scrape.scrape()
    #Updating Mongodb using update and upsert
    martian_dic.update({}, martian_data, upsert=True)
    return redirect("/", code = 302)

if __name__ == "__main__"
    app.run(debug=True)
#the concept of this application is to make a flask app that takes in your data and stores it in mongodb and you can see the details you have mentioned and edit it accd to your needs


from flask import Flask, redirect, render_template, request
from bson.objectid import ObjectId
import pymongo




app = Flask(__name__)

#setting up connection with mongodb
client = pymongo.MongoClient()
db = client["test-database"]
collection = db["flask-data-collection-from-user"]



@app.route("/", methods=["GET", "POST"])
def index():
    
    if request.method=="POST":
        name = request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        country = request.form["country"]
        job_role = request.form["job_role"]
        data_dict = {
            "Name": name,
            "Age": age,
            "City": city,
            "Country": country,
            "Job Role": job_role
        }


        collection.insert_one(data_dict)
    all_data = list(collection.find())
    
    return render_template("index.html", data=all_data[::-1])

@app.route("/delete/<id>")
def delete_item(id):
    collection.delete_one({"_id": ObjectId(id)})
    all_data = list(collection.find())
    return render_template("index.html", data=all_data)

@app.route("/update/<id>", methods=["GET", "POST"])
def update_item(id):
    if request.method=="POST":
        name = request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        country = request.form["country"]
        job_role = request.form["job_role"]

        data_to_be_updated = list(collection.find({"_id": ObjectId(id)}))
        print(data_to_be_updated)
        for i in data_to_be_updated:
            collection.update_one(
                {"_id": i["_id"]},
                {"$set": {"Name": name, "Age": age, "City": city, "Country": country, "Job Role": job_role}}
            )
        
        return redirect("/")
    
    data = list(collection.find({"_id": ObjectId(id)}))
    return render_template("update.html", data=data[0])


if __name__ == "__main__":
    app.run()

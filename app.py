import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
# We also said that MongoDB stores its data in a JSON-like format called BSON
# In order to find documents from MongoDB later, we need to be able to render the ObjectId,
# so: "from bson.objectid import ObjectId" with a capital 'O' and 'I'.
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

# Now that those imports are done, we need to add some additional configuration to our app.
# The first configuration will be used to grab the database name: app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME").
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
# Next, we need to configure the actual connection string, also called the MONGO_URI, which is
# done in the same exact way: app.config["MONGO_URI"] = os.environ.get("MONGO_URI").
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# this is where we go back to env.py and get the URI connection string for MONGO_URI
app.secret_key = os.environ.get("SECRET_KEY")

# We need to setup an instance of PyMongo, and add the app into that using something called
# This is the Flask 'app' object we've defined above, and is the final step to ensure our Flask app is properly communicating with the Mongo database.
mongo = PyMongo(app)


@app.route("/")
# Let's demonstrate this by creating a function with a decorator that includes a route to that function.
# Remember the routing is a string that, when we attach it to a URL, will redirect to a particular function in our Flask app.
# In our case, we're going to use a string called '/get_tasks', using the @app.route decorator.
# I'm going to add it directly beneath our existing default root here, so that either URL will direct the user to the same page.
@app.route("/get_tasks")
# The function name will also be changed to 'get_tasks' in order to match the route decorator.
# Before we proceed, there are some additional functionality from Flask that we need to import "at the top"
# In addition to the Flask function, we'll import flash, render_template, redirect, request, session, and url_for, look at the top of this page.
# ---------------------------------
# The template we're going to render will be called 'tasks.html', which we'll create shortly.
# On this tasks template, we want to be able to generate data from our tasks collection on MongoDB, visible to our users.
# tasks = mongo.db.tasks.find().
# This will find all documents from the tasks collection, and assign them to our new 'tasks' variable.
# Along with the rendering of the template, we'll pass that tasks variable through to the template: tasks=tasks.
# The first 'tasks' is what the template will use, and that's equal to the second 'tasks', which is our variable defined above.
def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
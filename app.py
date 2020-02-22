import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ["MONGO_DBNAME"]
app.config["MONGO_URI"] = os.environ["MONGO_URI"]

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    _recipes=mongo.db.recipes.find()
    recipe_list = [recipe for recipe in _recipes ]
    return render_template("recipes_list.html", recipes=recipe_list )

@app.route('/add_recipes')
def add_recipes():
    _categories=mongo.db.categories.find()
    category_list = [category for category in _categories]
    return render_template("addrecipe.html", categories = category_list)

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))


@app.route('/get_categories')
def get_categories():
    _categories=mongo.db.categories.find()
    category_list = [category for category in _categories]
    return render_template("categories.html", categories = category_list)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
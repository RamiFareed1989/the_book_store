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

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editrecipe.html', recipe=the_recipe, categories=all_categories)

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update(
        {'_id': ObjectId(recipe_id)},
        {
            'recipe_name': request.form.get('recipe_name'),
            'category_name': request.form.get('category_name'),
            'recipe_description': request.form.get('recipe_description'),
            'recipe_ingredients': request.form.get('recipe_ingredients'),
            'recipe_directions': request.form.get('recipe_directions'),
            'recipe_image': request.form.get('recipe_image')
        })
    return redirect(url_for('get_recipes'))

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
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

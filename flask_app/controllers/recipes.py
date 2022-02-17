from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session
#import model that you need below
from flask_app.models import user, recipe

@app.route('/create/recipe/form')
def create_recipe_form():
    if 'user_id' in session:
        person = user.User.get_user_by_id(session['user_id'])
        return render_template('create_recipe.html', user=person)
    return redirect('/')

@app.route('/create/recipe/submit', methods=['POST'])
def create_recipe():
    if 'user_id' in session:
        if recipe.Recipe.create_recipe(request.form):
            return redirect('/dashboard')
    return redirect('/create/recipe/form')


@app.route('/show/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' in session:
        person = user.User.get_user_by_id(session['user_id'])
        food = recipe.Recipe.get_one_by_id(id)
        return render_template('show.html',recipe=food, user=person)
    return redirect('/')


@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' in session:
        food=recipe.Recipe.get_one_by_id(id)
        person = user.User.get_user_by_id(session['user_id'])
        return render_template('edit_recipe.html', recipe=food, user=person)
    return redirect('/')

@app.route('/edit/recipe/submit', methods=['POST'])
def edit_recipe_submit():
    if recipe.Recipe.update_recipe_by_id(request.form):
        return redirect('/dashboard')
    id=request.form['id']
    return redirect(f'/edit/recipe/{id}')

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    if 'user_id' in session:
        recipe.Recipe.delete_recipe(id)
        return redirect('/dashboard')
    return redirect('/')
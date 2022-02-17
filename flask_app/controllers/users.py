from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session
#import model that you need below
from flask_app.models import user, recipe


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    user_id = user.User.save(request.form)
    if 'user_id' in session:
        return redirect('/dashboard')
    # ... do other things
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login_user():
    if user.User.login_user(request.form):
        return redirect('/dashboard')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        person = user.User.get_user_by_id(session['user_id'])
        items = recipe.Recipe.get_all_recipes_by_user(session['user_id'])
        return render_template('dashboard.html', user=person, recipes=items)
    else:
        return redirect('/')


@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')





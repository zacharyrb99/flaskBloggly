"""Bloggly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bloggly' # Where is your database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Needs to be set to false
app.config['SQLALCHEMY_ECHO'] = True # Prints SQL statements to terminal (good for debugging)
app.config['SECRET_KEY'] = 'password'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user():
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    first_name = request.form['first']
    last_name = request.form['last']
    image_url = request.form['img']
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()
    return redirect('/')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def submit_edit(user_id):
    user = User.query.get(user_id)
    fname = request.form['first']
    lname = request.form['last']
    img = request.form['img']

    user.first_name = fname
    user.last_name = lname
    user.image_url = img
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/')
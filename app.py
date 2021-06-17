"""Bloggly application."""
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bloggly' # Where is your database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Needs to be set to false
app.config['SQLALCHEMY_ECHO'] = True # Prints SQL statements to terminal (good for debugging)
app.config['SECRET_KEY'] = 'password'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

####USERS ROUTES####
@app.route('/')
def home():
    return render_template('home.html')

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
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('user_details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('user_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def submit_edit_user(user_id):
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

####POSTS ROUTES####
@app.route('/users/<int:user_id>/posts/<int:post_id>')
def show_posts(user_id, post_id):
    user = User.query.get(user_id)
    post = Post.query.get(post_id)
    length_tags = len(post.tags)
    return render_template('posts.html', user=user, post=post, length_tags=length_tags)

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    user = User.query.get_or_404(user_id) 
    tags = Tag.query.all()
    return render_template('post_form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    title = request.form['title']
    content = request.form['content']

    tag_ids=request.form.getlist('tags')
    for id in tag_ids:
        id = int(id)

    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}/posts/{new_post.id}')

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit')
def edit_post(user_id, post_id):
    user = User.query.get(user_id)
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    post_tags = post.tags
    
    return render_template('post_edit.html', user=user, post=post, tags=tags, post_tags=post_tags)

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit', methods=['POST'])
def submit_edit_post(user_id, post_id):
    post = Post.query.get(post_id)
    title = request.form['title']
    content = request.form['content']

    tag_ids=request.form.getlist('tags')
    for id in tag_ids:
        id = int(id)

    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post.title = title
    post.content = content
    post.tags = tags
    db.session.commit()

    return redirect(f'/users/{user_id}/posts/{post_id}')

@app.route('/users/<int:user_id>/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(user_id, post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/users/{user_id}')

####TAGS ROUTES####
@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('tags_details.html', tag=tag)

@app.route('/tags/new')
def add_tag():
    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def submit_new_tag():
    name = request.form['name']
    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def submit_edit_tag(tag_id):
    name = request.form['name']
    
    tag = Tag.query.get(tag_id)
    tag.name = name
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect('/tags')
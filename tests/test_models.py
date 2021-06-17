from unittest import TestCase
from app import app
from models import db, User, Post, DEFAULT_IMG

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bloggly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BlogglyModelTestCase(TestCase):
    """Tests for User model"""
    def test_full_name(self):
        user = User(first_name='Zach', last_name='Boudreaux')
        self.assertEqual(user.get_full_name(), 'Zach Boudreaux')
    def test_user1(self):
        user = User(first_name='Zach', last_name='Boudreaux')
        self.assertEqual(user.first_name, 'Zach')
        self.assertEqual(user.last_name, 'Boudreaux')
        self.assertIsNone(user.image_url)
    def test_user2(self):
        user = User(first_name='Zach', last_name='Boudreaux', image_url=DEFAULT_IMG)
        self.assertEqual(user.first_name, 'Zach')
        self.assertEqual(user.last_name, 'Boudreaux')
        self.assertEqual(user.image_url, DEFAULT_IMG)
    
    def test_post(self):
        post = Post(title='TestPost', content='Hello')
        self.assertEqual(post.title, 'TestPost')
        self.assertEqual(post.content, 'Hello')
    
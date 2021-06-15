from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bloggly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        
        user = User(first_name='Zach', last_name='Boudreaux')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()

    def test_users_redirect(self):
        with app.test_client() as client:
            response = client.get('/')

            self.assertEqual(response.status_code, 302)

    def test_users(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text = True)

            self.assertIn('<h1>Users</h1>', html)
            self.assertIn(f'''
            <li>
                <a href='/users/{self.user_id}'>Zach Boudreaux</a>
            </li>''', html)
    
    def test_user_details(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}')
            html = response.get_data(as_text = True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Zach Boudreaux</h1>', html)

    def test_edit_user(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}/edit')
            html = response.get_data(as_text = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Edit a User</h1>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            response = client.post(f'/users/{self.user_id}/delete')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(User.query.count(), 0)
from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

zach = User(first_name='Zach', last_name='Boudreaux', image_url='https://images.unsplash.com/photo-1527980965255-d3b416303d12?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80')
mariah = User(first_name='Mariah', last_name='Rick', image_url='https://images.unsplash.com/photo-1499887142886-791eca5918cd?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80')
emilie = User(first_name='Emilie', last_name='Boudreaux', image_url='https://images.unsplash.com/photo-1497340525489-441e8427c980?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80')
john = User(first_name='John', last_name='Doe')

zpost = Post(title='Post', content='Hello I am Zach', user_id=1)
mpost = Post(title='Post', content='Hello I am Mariah', user_id=2)
epost = Post(title='Post', content='Hello I am Emilie', user_id=3)

user_list = [zach, mariah, emilie, john]
db.session.add_all(user_list)
db.session.commit()

post_list = [zpost, mpost, epost]
db.session.add_all(post_list)
db.session.commit()
from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

zach = User(first_name='Zach', last_name='Boudreaux', image_url='https://images.unsplash.com/photo-1527980965255-d3b416303d12?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80')
mariah = User(first_name='Mariah', last_name='Rick', image_url='https://images.unsplash.com/photo-1499887142886-791eca5918cd?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80')
emilie = User(first_name='Emilie', last_name='Boudreaux', image_url='https://images.unsplash.com/photo-1497340525489-441e8427c980?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80')

db.session.add(zach)
db.session.add(mariah)
db.session.add(emilie)
db.session.commit()
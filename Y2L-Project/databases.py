from models import Base, Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
sess = DBSession()

def add_user(username, password):
    """
    Adds a user to the database, given their username and password.
    """
    user_object = Users(username=username, password=password, score=0)
    sess.add(user_object)
    sess.commit()

def update_score(username, score):
    """
    Updates the saved score of the user, given the username.
    """
    user_object = sess.query(Users).filter_by(username=username).first()
    user_object.score = score
    sess.commit()

def delete_user(username):
    """
    Deletes the user from the database, given their username.
    """
    sess.query(Users).filter_by(username=username).delete()
    sess.commit()

def query_all():
    """
    Returns all the users in the database.
    """
    users = sess.query(Users).all()
    return users

def query_by_username(username):
    """
    Returns the user with the given username.
    """
    user = sess.query(Users).filter_by(username=username).first()
    return user

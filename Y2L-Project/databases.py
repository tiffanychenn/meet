from models import Base, Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_user(username, password):
    """
    Adds a user to the database, given their username and password.
    """
    user_object = Users(username=username, password=password, score=0)
    session.add(user_object)
    session.commit()

def update_score(username, score):
    """
    Updates the saved score of the user, given the username.
    """
    user_object = session.query(Users).filter_by(username=username).first()
    user_object.score = score
    session.commit()

def delete_user(username):
    """
    Deletes the user from the database, given their username.
    """
    session.query(Users).filter_by(username=username).delete()
    session.commit()

def query_all():
    """
    Returns all the users in the database.
    """
    users = session.query(Users).all()
    return users

def query_by_username(username):
    """
    Returns the user with the given username.
    """
    user = session.query(Users).filter_by(username=username).first()
    return user

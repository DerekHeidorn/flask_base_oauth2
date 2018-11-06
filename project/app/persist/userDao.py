from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime



from project.app.models.user import User
from project.app.persist.baseDao import getSession



def addUser(newUser, session=None):
    """
    Creates and saves a new user to the database.

    :param newUser: new User record

    """
    #app.logger.info(newUser) 

    if(session == None):
        session = getSession()

    session.add(newUser)
    session.commit()

    return newUser.id

def getUsers(session=None):
    """
    Get all users, order by Last Name

    :return: users.
    """
    if(session == None):
        session = getSession()

    all_users = session.query(User).order_by(User.lastName).all()

    return all_users

def getUser(id, session=None):
    """
    Gets the User based on the id parameter

    :param id: The id of the user which needs to be loaded
    :return: The user.
    """
    if(session == None):
        session = getSession()

    user = session.query(User).filter(User.id == id).first()
    return user 

def getUserByUsername(username, session=None):
    """
    Gets the User based on the username parameter

    :param username: The username of the user which needs to be loaded
    :return: The user.
    """

    if(session == None):
        session = getSession()

    user = session.query(User).filter(User.username == username).first()
    return user


def updateUser(id, userToBeUpdated):
    updated_user = None
    session = getSession()

    user = getUser(id, session=session)
    if user == None:
        return updated_user

    user.firstName = userToBeUpdated["firstName"]
    user.lastName = userToBeUpdated["lastName"]
    user.username = userToBeUpdated["username"]

    session.commit()
    updated_user = getUser(id)

    return updated_user


def deleteUser(id):
    intId = int(id)
    if intId < 0 :
        raise ValueError("Parameter [id] should be a positive number!")

    if intId > 0 :
        session = getSession()
        items_deleted = session.query(User).filter(User.id == intId).delete()
        return items_deleted > 0

    return False







from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime



from models.user import User
from persist.baseDao import getSession



def add_user(newUser, session=None):
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

def get_users(serialize=False, session=None):
    """
    Get all users, order by Last Name

    :return: users.
    """
    if(session == None):
        session = getSession()

    all_users = session.query(User).order_by(User.last_name).all()

    if serialize:
        return [user.serialize() for user in all_users]
    else:
        return all_users

def get_user(id, serialize=False, session=None):
    """
    Gets the User based on the id parameter

    :param id: The id of the user which needs to be loaded
    :return: The user.
    """
    if(session == None):
        session = getSession()

    user = session.query(User).filter(User.id == id).first()
    if(user is not None):
        if serialize:
            return user.serialize()
        else:
            return user   
    else:
        return None


         

def get_user_by_login(login, serialize=False, session=None):
    """
    Gets the User based on the login parameter

    :param login: The login of the user which needs to be loaded
    :return: The user.
    """

    if(session == None):
        session = getSession()

    user = session.query(User).filter(User.login == login).first()
    if(user is not None):
        if serialize:
            return user.serialize()
        else:
            return user
    else:
        return None




def update_user(id, user_to_be_updated):
    updated_user = None
    session = getSession()

    user = get_user(id, session=session)
    if user == None:
        return updated_user

    user.first_name = user_to_be_updated["first_name"]
    user.last_name = user_to_be_updated["last_name"]
    user.login = user_to_be_updated["login"]


    session.commit()
    updated_user = get_user(id, session=session)

    return updated_user.serialize()


def delete_user(id):
    intId = int(id)
    if intId < 0 :
        raise ValueError("Parameter [id] should be a positive number!")

    if intId > 0 :
        session = getSession()
        items_deleted = session.query(User).filter(User.id == intId).delete()
        return items_deleted > 0

    return False







import hashlib
import json

from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask import Blueprint
from datetime import datetime, timedelta

import jwt

from math import ceil

from project.app.models.user import User
from project.app.persist import userDao, securityDao
from project.app.services.baseService import BaseService
from project.app.services.utils import userUtils
from project.app.services import commonService

def isUserValid(username, password):
    user = userDao.getUserByLogin(username)
    if(user is not None):
        return userUtils.isUserValid(user, password)
    else:
        return False


def buildMessage(key, message):
    return {key:message}    

def deleteUser(id):
    return userDao.deleteUser(id)

def updateUser(id, userToBeUpdated):
    return userDao.updateUser(id, userToBeUpdated)    

def getUserById(id):
    return userDao.getUser(id)

def getUserByLogin(username):
    return userDao.getUserByLogin(username)

def getUserByLoginAndValidate(username, password):
    user = userDao.getUserByLogin(username)
    if(user is not None):
        return {"user": user, "isPasswordValid": userUtils.isUserValid(user, password)}
    else:
        return  {"user": None, "isPasswordValid": False}

def addUser(login, password, firstName=None, lastName=None):

    userUtils.randomUserPrivateKey(32)

    newUser = User(firstName=firstName, lastName=lastName, login=login)
    newUser.statusCd = 'A'
    newUser.typeCd = '1'
    newUser.failedAttemptCnt = 0
    newUser.privateKey = userUtils.randomUserPrivateKey(32)
    newUser.passwordSalt = userUtils.randomUserPrivateKey(32) 
    newUser.passwordHash = userUtils.getHashedPassword(password, newUser.passwordSalt)
    userId = userDao.addUser(newUser)
    if userId:
        return userDao.getUser(userId)
    else:
        return None




 




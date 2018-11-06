from project.app.models.user import User
from project.app.persist import userDao, securityDao
from project.app.services.utils import userUtils


def isUserValid(username, password):
    user = userDao.getUserByUsername(username)
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


def getUserByUsername(username):
    return userDao.getUserByUsername(username)


def isUsernameUnique(username):
    return userDao.isUsernameUnique(username)


def getUserByUsernameAndValidate(username, password):
    user = userDao.getUserByUsername(username)
    if(user is not None):
        return {"user": user, "isPasswordValid": userUtils.isUserValid(user, password)}
    else:
        return  {"user": None, "isPasswordValid": False}


def addPublicUser(username, password, firstName=None, lastName=None):

    userUtils.randomUserPrivateKey(32)

    session = securityDao.getSession()
    securityGroup = securityDao.getSecurityGroupByName(securityDao.SECURITY_GROUP_CUSTOMER_NAME
                                                          , session=session)


    newUser = User(firstName=firstName, lastName=lastName, username=username)
    newUser.statusCd = 'A'
    newUser.typeCd = '1'
    newUser.failedAttemptCnt = 0
    newUser.privateKey = userUtils.randomUserPrivateKey(32)
    newUser.passwordSalt = userUtils.randomUserPrivateKey(32) 
    newUser.passwordHash = userUtils.getHashedPassword(password, newUser.passwordSalt)

    newUser.securityGroups.append(securityGroup)
    userId = userDao.addUser(newUser, session=session)
    if userId:
        return userDao.getUser(userId)
    else:
        return None



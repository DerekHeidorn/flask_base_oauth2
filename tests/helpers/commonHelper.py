from services import userService
from tests.utils import randomUtil

def createPublicUser():

    first_name = "FirstNm_" + randomUtil.randomString(6, 10),
    last_name = "LastNm_" + randomUtil.randomString(6, 10),
    login = randomUtil.randomLogin(),
    password = randomUtil.randomString(10, 25)

    newUser = userService.addUser(login, password, first_name, last_name)

    return newUser
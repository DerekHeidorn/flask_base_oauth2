from services import userService
from tests.utils import randomUtil

DEFAULT_PUBLIC_USER_PASSWORD = "fooBar@123"

def createPublicUser():

    first_name = "FirstNm_" + randomUtil.randomString(6, 10),
    last_name = "LastNm_" + randomUtil.randomString(6, 10),
    login = randomUtil.randomLogin(),
    password = DEFAULT_PUBLIC_USER_PASSWORD

    newUser = userService.addUser(login, password, first_name, last_name)

    return newUser
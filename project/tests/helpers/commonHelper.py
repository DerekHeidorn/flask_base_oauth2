from project.app.services import userService
from project.tests.utils import randomUtil

DEFAULT_PUBLIC_USER_PASSWORD = "fooBar@123"
DEFAULT_PUBLIC_USERNAME = "Joe.Customer@foo.com.invali"
DEFAULT_ADMIN_USERNAME = "sys.admin@foo.com.invali"


def createPublicUser():

    username = randomUtil.randomUsername()
    password = DEFAULT_PUBLIC_USER_PASSWORD
    first_name = "FirstNm_" + randomUtil.randomString(6, 10)
    last_name = "LastNm_" + randomUtil.randomString(6, 10)

    newUser = userService.addUser(username, password, first_name, last_name)

    return newUser
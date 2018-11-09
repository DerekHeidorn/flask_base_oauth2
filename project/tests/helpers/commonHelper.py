from project.app.services import userService
from project.tests.utils import randomUtil

DEFAULT_PUBLIC_USER_PASSWORD = "foobar@123"
DEFAULT_PUBLIC_USERNAME = "Joe.Customer@foo.com.invali"
DEFAULT_ADMIN_USERNAME = "sys.admin@foo.com.invali"
DEFAULT_PUBLIC_CLIENT_ID = "CLTID-Zeq1LRso5q-iLU9RKCKnu"


def create_public_user():

    username = randomUtil.random_username()
    password = DEFAULT_PUBLIC_USER_PASSWORD
    first_name = "FirstNm_" + randomUtil.random_string(6, 10)
    last_name = "LastNm_" + randomUtil.random_string(6, 10)

    new_user = userService.add_public_user(DEFAULT_PUBLIC_CLIENT_ID, username, password, first_name, last_name)

    return new_user

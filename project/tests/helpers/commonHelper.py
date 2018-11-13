from urllib import parse
from project.app.services import userService, commonService
from project.app.services.utils import userUtils
from project.app.web.utils import authUtils
from project.tests.utils import randomUtil

DEFAULT_PUBLIC_USER_PASSWORD = "foobar@123"
DEFAULT_PUBLIC_USERNAME = "Joe.Customer@foo.com.invali"
DEFAULT_PUBLIC_UUID = "c95802ac-e465-11e8-9f32-f2801f1b9fd1"  # Joe.Customer@foo.com.invali

DEFAULT_ADMIN_USERNAME = "sys.admin@foo.com.invali"
DEFAULT_ADMIN_UUID = "c957fece-e465-11e8-9f32-f2801f1b9fd1"  # sys.admin@foo.com.invali

DEFAULT_PUBLIC_CLIENT_ID = "CLTID-Zeq1LRso5q-iLU9RKCKnu"


def create_public_user():

    username = randomUtil.random_username()
    password = DEFAULT_PUBLIC_USER_PASSWORD
    first_name = "FirstNm_" + randomUtil.random_string(6, 10)
    last_name = "LastNm_" + randomUtil.random_string(6, 10)

    new_user = userService.add_public_user(DEFAULT_PUBLIC_CLIENT_ID, username, password, first_name, last_name)

    return new_user


def create_public_user_and_token(testClient):

    print("common helper: create_public_user_and_token")
    username = randomUtil.random_username()
    password = randomUtil.random_string(10, 25)
    resp = testClient.post('/signup',
                           data=dict(username=username,
                                     password=password,
                                     password_repeat=password,
                                     grant_type="password",
                                     client_id=DEFAULT_PUBLIC_CLIENT_ID
                                     )
                           )

    param_dict = dict(parse.parse_qsl(parse.urlsplit(resp.location).query))


    # check the database for the new user
    user = userService.get_user_by_username(username)


    return {"user": user, "token": param_dict.get('access_token')}


def get_default_staff_and_token():

    staff = userService.get_user_by_uuid(DEFAULT_ADMIN_UUID)
    bearer_token = generate_jwt_token(staff)

    return {"user": staff, "token": bearer_token}


def generate_jwt_token(user):

    authorities = userUtils.get_user_authorities(user)
    oauth2_secret_key = commonService.get_config_by_key('oauth2_secret_key')
    token = authUtils.encode_auth_token(user, authorities, oauth2_secret_key)

    return token.decode("utf-8")

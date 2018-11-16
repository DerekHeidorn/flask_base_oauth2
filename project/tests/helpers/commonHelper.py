import os
from urllib import parse
from project.app.services import userService
from project.app.services.utils import userUtils
from project.app.web.utils import authUtils
from project.tests.utils import randomUtil
from project.app import main

DEFAULT_PUBLIC_USER_PASSWORD = "foobar@123"
DEFAULT_PUBLIC_USERNAME = "Joe.Customer@foo.com.invali"
DEFAULT_PUBLIC_UUID = "c95802ac-e465-11e8-9f32-f2801f1b9fd1"  # Joe.Customer@foo.com.invali

DEFAULT_ADMIN_USERNAME = "sys.admin@foo.com.invali"
DEFAULT_ADMIN_UUID = "c957fece-e465-11e8-9f32-f2801f1b9fd1"  # sys.admin@foo.com.invali

DEFAULT_PUBLIC_CLIENT_ID = "CLTID-Zeq1LRso5q-iLU9RKCKnu"


def setup_dev_settings():
    # for using http instead of https
    os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Application specific
    os.environ["APP_MODE"] = "dev"  # dev, test, or prod
    os.environ["APP_SECRET_KEY"] = "KlkdZyb5xrGpDcNkSBrDhe790ohLfuea"
    os.environ["APP_FLASK_SECRET_KEY"] = "wbr59q8tof3k2FfeSIvO"

    os.environ["APP_JWT_ISS"] = "https://localhost:9000"
    os.environ["APP_JWT_KEY"] = "BMcrqdcd7QeEmR8CXyU"

    # database config
    os.environ["APP_DB_CONNECTION_URI"] = "postgresql://postgres:P$F$xs+n?5+Ug3AU5PTe3q@localhost/postgres"
    os.environ["APP_DB_ENGINE_DEBUG"] = "False"


def create_public_user():

    username = randomUtil.random_username()
    password = DEFAULT_PUBLIC_USER_PASSWORD
    first_name = "FirstNm_" + randomUtil.random_string(6, 10)
    last_name = "LastNm_" + randomUtil.random_string(6, 10)

    new_user = userService.add_public_user(DEFAULT_PUBLIC_CLIENT_ID, username, password, first_name, last_name)

    return new_user


def create_public_user_and_token(test_client):

    print("common helper: create_public_user_and_token")
    username = randomUtil.random_username()
    password = randomUtil.random_string(10, 25)
    resp = test_client.post('/signup',
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
    oauth2_secret_key = main.global_config["APP_JWT_KEY"]
    token = authUtils.encode_auth_token(user, authorities, oauth2_secret_key)

    return token.decode("utf-8")

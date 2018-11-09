
from project.tests.persist.baseTest import BaseTest
from project.tests.helpers import commonHelper
from project.app.persist import oauth2Dao


class OauthDaoTestCase(BaseTest):

    # def add_authorization_code(client, user, request):
    def test_add_authorization_code(self):
        print("running test_add_authorization_code...")
        created_user = commonHelper.create_public_user()

        user = oauth2Dao.add_authorization_code(created_user.username)
        self.assertEquals(created_user.username, user.username)

    # def parse_authorization_code(code, client):
    def test_parse_authorization_code(self):
        print("running parse_authorization_code...")
        created_user = commonHelper.create_public_user()

        user = oauth2Dao.parse_authorization_code(created_user.username)
        self.assertEquals(created_user.username, user.username)

    # def delete_authorization_code(authorization_code):
    def test_delete_authorization_code(self):
        print("running delete_authorization_code...")
        created_user = commonHelper.create_public_user()

        user = oauth2Dao.delete_authorization_code(created_user.username)
        self.assertEquals(created_user.username, user.username)

    # def authenticate_user(authorization_code):
    def test_authenticate_user(self):
        print("running authenticate_user...")
        created_user = commonHelper.create_public_user()

        user = oauth2Dao.authenticate_user(created_user.username)
        self.assertEquals(created_user.username, user.username)

    # def create_access_token(client, grant_user=None):
    def test_create_access_token(self):
        print("running create_access_token...")
        created_user = commonHelper.create_public_user()

        user = oauth2Dao.create_access_token(created_user.username)
        self.assertEquals(created_user.username, user.username)

    #  def query_client(client_id, session=None):
    def test_query_client(self):
        print("running query_client...")
        created_user = commonHelper.create_public_user()

        user = oauth2Dao.query_client(created_user.username)
        self.assertEquals(created_user.username, user.username)

    # def query_token(token, token_type_hint):
    def test_query_token(self):
        print("running query_token...")
        created_user = commonHelper.create_public_user()

        user = oauth2Dao.query_token(created_user.username)
        self.assertEquals(created_user.username, user.username)

    # def save_token(client_id, user_id, token_type, scope, jti, issued_at, expires_in):
    def test_save_token(self):
        print("running save_token...")
        created_user = commonHelper.create_public_user()

        user = oauth2Dao.save_token(created_user.username)
        self.assertEquals(created_user.username, user.username)

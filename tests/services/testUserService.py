
from tests.services.baseTest import BaseTest
from tests.helpers import commonHelper
from app.services import userService


class UserServiceTestCase(BaseTest):

    def test_get_user_by_username(self):
        print("running testGetUserByUsername...")
        created_user = commonHelper.create_public_user()

        user = userService.get_user_by_username(created_user.username)
        self.assertEquals(created_user.username, user.username)


from project.tests.services.baseTest import BaseTest
from project.tests.helpers import commonHelper
from project.app.services import emailService


class EmailServiceTestCase(BaseTest):

    def test_get_user_by_username(self):
        print("running testGetUserByUsername...")
        created_user = commonHelper.create_public_user()

        emailService.send_reset_password_email(created_user)


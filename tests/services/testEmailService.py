
from tests.services.baseTest import BaseTest
from tests.helpers import commonHelper
from app.services import emailService


class EmailServiceTestCase(BaseTest):

    def test_send_reset_password_email(self):
        print("running send_reset_password_email...")
        created_user = commonHelper.create_public_user()

        emailService.send_reset_password_email(created_user.get_formatted_name(),
                                               created_user.username,
                                               '12345',
                                               'http://localhost:9000')


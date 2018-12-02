
from tests.persist.baseTest import BaseTest
from tests.helpers import commonHelper
from app.persist import securityDao


class SecurityDaoTestCase(BaseTest):

    def test_get_user_security_authorities(self):
        print("running get_user_security_authorities...")
        created_user = commonHelper.create_public_user()

        authorities = securityDao.get_user_security_authorities(created_user.user_id)
        print("authorities=" + str(authorities))
        found_cust_access = False
        for a in authorities:
            if a.key == "CUST_ACCESS":
                found_cust_access = True

        self.assertTrue(found_cust_access)

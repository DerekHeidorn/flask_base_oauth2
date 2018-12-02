
from tests.persist.baseTest import BaseTest
from tests.helpers import commonHelper
from app.persist import oauth2Dao


class OauthDaoTestCase(BaseTest):



    #  def query_client(client_id, session=None):
    def test_query_client(self):
        print("running query_client...")

        oauth2_client = oauth2Dao.query_client(commonHelper.DEFAULT_PUBLIC_CLIENT_ID)
        self.assertEquals(commonHelper.DEFAULT_PUBLIC_CLIENT_ID, oauth2_client.client_id)





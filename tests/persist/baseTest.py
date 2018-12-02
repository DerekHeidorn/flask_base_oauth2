
import unittest
from app import core
from tests.helpers import commonHelper


class BaseTest(unittest.TestCase):
    commonHelper.setup_dev_settings()
    app = core.create_application()

    def setUp(self):
        print("setting up Test Client...")
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.testClient = self.app.test_client()

    def tearDown(self):
        pass

    def debug_response(self, response):
        
        print("type=" + str(type(response)))
        print("status_code=" + str(response.status_code))
        print("response.content_type=" + str(response.content_type))
        
        if response.data:
            print("Data=" + response.data.decode("utf-8"))

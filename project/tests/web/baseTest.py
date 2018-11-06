
import os
import unittest
from project.app import main

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTH_INSECURE_TRANSPORT'] = '1'
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

class BaseTest(unittest.TestCase):

    app = main.createApplication()

    def setUp(self):
        print("setting up Test Client...")
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.testClient = self.app.test_client()

    def tearDown(self):
        pass

    def debugResponse(self, response):
        
        print("type=" + str(type(response)))
        print("status_code=" + str(response.status_code))
        print("response.content_type=" + str(response.content_type))
        
        if(response.data):
            print("Data=" + response.data.decode("utf-8") )
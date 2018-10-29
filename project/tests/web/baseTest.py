
import unittest
import sys
#sys.path.append("../..") # Adds higher directory to python modules path.

from project.app import app






class BaseTest(unittest.TestCase):

    app = app.createApplication()

    def setUp(self):
        print("setting up Test Client...")
        self.app.config['TESTING'] = True
        self.testClient = self.app.test_client()


    def tearDown(self):
        pass

    def debugResponse(self, response):
        
        print("type=" + str(type(response)))
        print("status_code=" + str(response.status_code))
        print("response.content_type=" + str(response.content_type))
        
        if(response.data):
            print("Data=" + response.data.decode("utf-8") )
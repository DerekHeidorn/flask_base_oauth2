import pytest
import unittest
import json
import time

from project.app.models.user import User
from project.tests.web.baseTest import BaseTest 
from project.tests.helpers import commonHelper
from project.tests.utils import randomUtil

class AuthTestCase(BaseTest):

    def registerUser(self, username, password):
        response = self.testClient.post(
            '/api/v1.0/auth/register',
            data=json.dumps(dict(
                username=username,
                password=password
            )),
            content_type='application/json',
        )
        self.debugResponse(response)
        return response

    def loginUser(self, username, password):
        response = self.testClient.post(
            '/api/v1.0/auth/login',
            data=json.dumps(dict(
                username=username,
                password=password
            )),
            content_type='application/json',
        )
        self.debugResponse(response)
        return response

    def testRegistration(self):
        """ Test for user registration """
        print("testing test_registration...")

        with self.testClient:
            response = self.registerUser(randomUtil.randomUsername(), '123456')
            data = json.loads(response.data.decode())
            self.assertEquals(data['status'],'success')
            self.assertEquals(data['message'], 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertEquals(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 201)

    def testRegisteredWithAlreadyRegisteredUser(self):
        """ Test registration with already registered email"""
        print("testing test_registered_with_already_registered_user...")
        user = commonHelper.createPublicUser()

        with self.testClient:
            response = self.registerUser(user.username, '123456')
            data = json.loads(response.data.decode())
            self.assertEquals(data['status'], 'fail')
            self.assertEquals(
                data['message'], 'User already exists. Please Log in.')
            self.assertEquals(response.content_type,'application/json')
            self.assertEqual(response.status_code, 202)

    def testRegisteredUserLogin(self):
        """ Test for login of registered-user login """
        print("testing testRegisteredUserLogin...")

        with self.testClient:
            username = randomUtil.randomUsername()

            # user registration
            resp_register = self.registerUser(username, commonHelper.DEFAULT_PUBLIC_USER_PASSWORD)
            data_register = json.loads(resp_register.data.decode())
            self.assertEquals(data_register['status'],'success')
            self.assertEquals(
                data_register['message'],'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertEquals(resp_register.content_type, 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = self.loginUser(username, commonHelper.DEFAULT_PUBLIC_USER_PASSWORD)
            data = json.loads(response.data.decode())
            self.assertEquals(data['status'], 'success')
            self.assertEquals(data['message'], 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertEquals(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 200)

    def testNonRegisteredUserLogin(self):
        """ Test for login of non-registered user """
        print("testing test_non_registered_user_login...")

        with self.testClient:
            response = self.loginUser('doesntExist@foo-bar.com', '123456')
            data = json.loads(response.data.decode())
            self.assertEquals(data['status'], 'fail')
            self.assertEquals(data['message'], 'User does not exist.')
            self.assertEquals(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 404)

    def testUserStatus(self):
        """ Test for user status """
        print("testing test_user_status...")

        with self.testClient:
            username = randomUtil.randomUsername()
            resp_register = self.registerUser(username, '123456')
            response = self.testClient.get(
                '/api/v1.0/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEquals(data['status'], 'success')
            self.assertTrue(data['data'] is not None)
            self.assertEquals(data['data']['username'], username)
            #self.assertTrue(data['data']['admin'] is 'true' or 'false')
            self.assertEqual(response.status_code, 200)

    def testUserStatusMalformedBearerToken(self):
        """ Test for user status with malformed bearer token"""
        print("testing test_user_status_malformed_bearer_token...")

        with self.testClient:
            username = randomUtil.randomUsername()
            resp_register = self.registerUser(username, '123456')
            response = self.testClient.get(
                '/api/v1.0/auth/status',
                headers=dict(
                    Authorization='Bearer' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEquals(data['status'], 'fail')
            self.assertEquals(data['message'], 'Bearer token malformed.')
            self.assertEqual(response.status_code, 401)

    def testValidLogout(self):
        """ Test for logout before token expires """
        print("testing testValidLogout...")

        with self.testClient:
            username = randomUtil.randomUsername()

            # user registration
            resp_register = self.registerUser(username, '123456')
            data_register = json.loads(resp_register.data.decode())

            self.assertEquals(data_register['status'], 'success')
            self.assertEquals(
                data_register['message'], 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertEquals(resp_register.content_type, 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.loginUser(username, '123456')
            data_login = json.loads(resp_login.data.decode())
            self.assertEquals(data_login['status'], 'success')
            self.assertEquals(data_login['message'], 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertEquals(resp_login.content_type, 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # valid token logout
            response = self.testClient.post(
                '/api/v1.0/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEquals(data['status'], 'success')
            self.assertEquals(data['message'], 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def testInvalidLogout(self):
        """ Testing logout after the token expires """
        print("testing testInvalidLogout...")

        with self.testClient:
            username = randomUtil.randomUsername()

            # user registration
            resp_register = self.registerUser(username, '123456')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertEqual(
                data_register['message'], 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.loginUser(username, '123456')
            data_login = json.loads(resp_login.data.decode())
            self.assertEqual(data_login['status'], 'success')
            self.assertEqual(data_login['message'],'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # invalid token logout
            time.sleep(6)
            response = self.testClient.post(
                '/api/v1.0/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
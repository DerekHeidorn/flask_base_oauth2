import pytest
import unittest
import json
import time
from baseTest import BaseTest 
from tests.utils import randomUtil

from models.user import User
from tests.helpers import commonHelper





class AuthTestCase(BaseTest):

    def register_user(self, login, password):
        response = self.testClient.post(
            '/api/v1.0/auth/register',
            data=json.dumps(dict(
                login=login,
                password=password
            )),
            content_type='application/json',
        )
        self.debugResponse(response)
        return response

    def login_user(self, login, password):
        response = self.testClient.post(
            '/api/v1.0/auth/login',
            data=json.dumps(dict(
                login=login,
                password=password
            )),
            content_type='application/json',
        )
        self.debugResponse(response)
        return response

    def test_registration(self):
        """ Test for user registration """
        print("testing test_registration...")

        with self.testClient:
            response = self.register_user(randomUtil.randomLogin(), '123456')
            data = json.loads(response.data.decode())
            self.assertEquals(data['status'],'success')
            self.assertEquals(data['message'], 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertEquals(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        print("testing test_registered_with_already_registered_user...")
        user = commonHelper.createPublicUser()

        with self.testClient:
            response = self.register_user(user.login, '123456')
            data = json.loads(response.data.decode())
            self.assertEquals(data['status'], 'fail')
            self.assertEquals(
                data['message'], 'User already exists. Please Log in.')
            self.assertEquals(response.content_type,'application/json')
            self.assertEqual(response.status_code, 202)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        print("testing test_registered_user_login...")

        with self.testClient:
            user = commonHelper.createPublicUser()

            # user registration
            resp_register = self.register_user(user.login, commonHelper.DEFAULT_PUBLIC_USER_PASSWORD)
            data_register = json.loads(resp_register.data.decode())
            self.assertEquals(data_register['status'],'success')
            self.assertEquals(
                data_register['message'],'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertEquals(resp_register.content_type, 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = self.login_user(user.login, commonHelper.DEFAULT_PUBLIC_USER_PASSWORD)
            data = json.loads(response.data.decode())
            self.assertEquals(data['status'], 'success')
            self.assertEquals(data['message'], 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertEquals(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        print("testing test_non_registered_user_login...")

        with self.testClient:
            response = self.login_user('doesntExist@foo-bar.com', '123456')
            data = json.loads(response.data.decode())
            self.assertEquals(data['status'], 'fail')
            self.assertEquals(data['message'], 'User does not exist.')
            self.assertEquals(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_user_status(self):
        """ Test for user status """
        print("testing test_user_status...")

        with self.testClient:
            userlogin = randomUtil.randomLogin()
            resp_register = self.register_user(userlogin, '123456')
            response = self.testClient.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEquals(data['status'], 'success')
            self.assertTrue(data['data'] is not None)
            self.assertEquals(data['data']['login'], userlogin)
            #self.assertTrue(data['data']['admin'] is 'true' or 'false')
            self.assertEqual(response.status_code, 200)

    def test_user_status_malformed_bearer_token(self):
        """ Test for user status with malformed bearer token"""
        print("testing test_user_status_malformed_bearer_token...")

        with self.testClient:
            userlogin = randomUtil.randomLogin()
            resp_register = self.register_user(userlogin, '123456')
            response = self.testClient.get(
                '/auth/status',
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

    def test_valid_logout(self):
        """ Test for logout before token expires """
        print("testing test_valid_logout...")

        with self.testClient:
            userlogin = randomUtil.randomLogin()

            # user registration
            resp_register = self.register_user(userlogin, '123456')
            data_register = json.loads(resp_register.data.decode())
            #self.assertTrue(data_register['status'] == 'success')
            self.assertEquals(data_register['status'], 'success')
            self.assertEquals(
                data_register['message'], 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertEquals(resp_register.content_type, 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.login_user(userlogin, '123456')
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

    def test_invalid_logout(self):
        """ Testing logout after the token expires """
        print("testing test_invalid_logout...")

        with self.testClient:
            userlogin = randomUtil.randomLogin()

            # user registration
            resp_register = self.register_user(userlogin, '123456')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.login_user(userlogin, '123456')
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # invalid token logout
            time.sleep(6)
            response = self.testClient.post(
                '/auth/logout',
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
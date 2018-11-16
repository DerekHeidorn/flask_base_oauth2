import json
import unittest
from urllib import parse
from project.tests.web.baseTest import BaseTest 
from project.tests.utils import randomUtil
from project.tests.helpers import commonHelper
from project.app.services import userService, encryptionService


class UserWebTestCase(BaseTest):

    def test_signup(self):
        print("Running: test_signup")
        username = randomUtil.random_username()
        password = randomUtil.random_string(10, 25)
        resp = self.testClient.post('/signup',
                                    data=dict(username=username,
                                              password=password,
                                              password_repeat=password,
                                              grant_type="password",
                                              client_id=commonHelper.DEFAULT_PUBLIC_CLIENT_ID
                                              )
                                    )
        self.debug_response(resp)

        # should be redirected to new page
        self.assertEqual(302, resp.status_code)
        self.assertEqual("text/html; charset=utf-8", resp.content_type)

        print("resp.location=" + resp.location)
        param_dict = dict(parse.parse_qsl(parse.urlsplit(resp.location).query))
        self.assertEqual('Bearer', param_dict.get('token_type'))
        self.assertTrue(len(param_dict.get('access_token')) > 0)

        # check the database for the new user
        user = userService.get_user_by_username(username)
        self.assertEqual(user.username, username)

    def test_login(self):
        print("Running: test_login")
        username_gen = randomUtil.random_username()
        password_gen = randomUtil.random_string(10, 25)

        # -----------------------------------------------
        #  Signup
        # -----------------------------------------------
        resp = self.testClient.post('/signup',
                                    data=dict(
                                              username=username_gen,
                                              password=password_gen,
                                              password_repeat=password_gen,
                                              grant_type="password",
                                              client_id=commonHelper.DEFAULT_PUBLIC_CLIENT_ID
                                              )
                                    )
        self.debug_response(resp)

        # should be redirected to new page
        self.assertEqual(302, resp.status_code)
        self.assertEqual("text/html; charset=utf-8", resp.content_type)

        print("resp.location=" + resp.location)
        param_dict = dict(parse.parse_qsl(parse.urlsplit(resp.location).query))
        self.assertEqual('Bearer', param_dict.get('token_type'))
        self.assertTrue(len(param_dict.get('access_token')) > 0)

        # check the database for the new user
        user = userService.get_user_by_username(username_gen)
        self.assertEquals(user.username, username_gen)

        # -----------------------------------------------
        #  Login
        # -----------------------------------------------
        resp = self.testClient.post('/login',
                                    data=dict(
                                              username=username_gen,
                                              password=password_gen,
                                              grant_type="password",
                                              client_id=commonHelper.DEFAULT_PUBLIC_CLIENT_ID
                                              )
                                    )
        self.debug_response(resp)

        # should be redirected to new page
        self.assertEqual(302, resp.status_code)
        self.assertEqual("text/html; charset=utf-8", resp.content_type)

        print("resp.location=" + resp.location)
        param_dict = dict(parse.parse_qsl(parse.urlsplit(resp.location).query))
        self.assertEqual('Bearer', param_dict.get('token_type'))
        self.assertTrue(len(param_dict.get('access_token')) > 0)

        # -----------------------------------------------
        #  Logout
        # -----------------------------------------------
        resp = self.testClient.get('/login',
                                   data=dict(
                                             username=username_gen,
                                             password=password_gen,
                                             grant_type="password",
                                             client_id=commonHelper.DEFAULT_PUBLIC_CLIENT_ID
                                             )
                                   )
        self.debug_response(resp)

        # should be redirected to new page
        self.assertEqual(302, resp.status_code)
        self.assertEqual("text/html; charset=utf-8", resp.content_type)

    def test_user_profile(self):
        print("Running: test_user_profile")
        user_info = commonHelper.create_public_user_and_token(self.testClient)
        print("user_info=" + str(user_info))
        new_user = user_info["user"]

        print("token=" + user_info['token'])
        resp = self.testClient.get('/api/v1.0/public/user/profile',
                                   headers={"Authorization": "bearer " + user_info['token']})

        self.debug_response(resp)

        self.assertEqual(200, resp.status_code)
        self.assertEqual("application/json", resp.content_type)

        response_data = json.loads(resp.data)

        self.assertEqual(new_user.username, response_data['username'])

    def test_reset_password(self):
        print("Running: test_reset_password")
        user = commonHelper.create_public_user()
        original_password_salt = user.password_salt
        original_password_hash = user.password_hash
        print("user=" + str(user))

        # make the initial request to reset password
        resp = self.testClient.get('/reset/request')

        # returns HTML
        self.assertEqual(200, resp.status_code)

        resp = self.testClient.post('/reset/request',
                                    data=dict(username=user.username
                                              )
                                    )
        # returns HTML
        self.assertEqual(200, resp.status_code)

        user = userService.get_user_by_username(user.username)
        print("user.reset_code=" + user.reset_code)
        self.assertTrue(len(user.reset_code) > 0)

        # --------------------------------------------------------------
        # COPIED from userService to get the correct encrypted values
        # new code is encrypted using the user's private key
        encrypted_reset_code = encryptionService.encrypt_string(user.reset_code, user.private_key)

        reset_info = {'username': user.username, 'code': encrypted_reset_code}
        encrypted_reset_info = encryptionService.encrypt_dictionary_with_base64(reset_info)
        # --------------------------------------------------------------

        resp = self.testClient.get('/reset?e=' + encrypted_reset_info)
        self.assertEqual(200, resp.status_code)

        new_password = "123Foobar@ABC"
        resp = self.testClient.post('/reset',
                                    data=dict(username=user.username,
                                              password=new_password,
                                              password_repeat=new_password,
                                              reset_code=user.reset_code
                                              )
                                    )
        self.assertEqual(200, resp.status_code)

        user = userService.get_user_by_username(user.username)

        # values below should have changed
        self.assertTrue(user.reset_code is None)
        self.assertNotEqual(original_password_salt, user.password_salt)
        self.assertNotEqual(original_password_hash, user.password_hash)

    def test_reactivate(self):
        print("Running: test_reactivate")
        user = commonHelper.create_public_user()
        print("user=" + str(user))

        # -----------------------------------------------
        #  Login
        # -----------------------------------------------
        for x in range(10):
            resp = self.testClient.post('/login',
                                        data=dict(
                                                    username=user.username,
                                                    password="FailedPassword",
                                                    grant_type="password",
                                                    client_id=commonHelper.DEFAULT_PUBLIC_CLIENT_ID
                                                )
                                        )

        user = userService.get_user_by_username(user.username)
        self.assertTrue(user.failed_attempt_count > 8)
        self.assertTrue(len(user.activation_code) > 0)
        self.assertTrue(user.last_attempts_ts is not None)

        # --------------------------------------------------------------
        # COPIED from userService to get the correct encrypted values
        # new code is encrypted using the user's private key
        encrypted_activation_code = encryptionService.encrypt_string(user.activation_code, user.private_key)

        reset_info = {'username': user.username, 'code': encrypted_activation_code}
        encrypted_activation_info = encryptionService.encrypt_dictionary_with_base64(reset_info)
        # --------------------------------------------------------------

        resp = self.testClient.get('/activate?e=' + encrypted_activation_info)
        self.assertEqual(200, resp.status_code)

        resp = self.testClient.post('/activate',
                                    data=dict(username=user.username,
                                              reset_code=user.activation_code
                                              )
                                    )
        self.assertEqual(200, resp.status_code)

        user = userService.get_user_by_username(user.username)

        # values below should have changed
        self.assertTrue(user.activation_code is None)
        self.assertEqual(0, user.failed_attempt_count)


if __name__ == '__main__':
    unittest.main()

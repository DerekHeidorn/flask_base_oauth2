import json
import unittest
from urllib import parse
from tests.web.baseTest import BaseTest
from tests.utils import randomUtil
from tests.helpers import commonHelper
from app.services import userService, encryptionService


class PublicUserApiTestCase(BaseTest):

    def test_signup(self):
        print("Running: test_signup")
        username = randomUtil.random_username()
        alias = randomUtil.random_string(10, 25)
        password = randomUtil.random_string(10, 25)
        resp = self.testClient.post('/signup',
                                    data=dict(username=username,
                                              alias=alias,
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
        alias_gen = randomUtil.random_string(8, 22)

        # -----------------------------------------------
        #  Signup
        # -----------------------------------------------
        resp = self.testClient.post('/signup',
                                    data=dict(
                                              username=username_gen,
                                              alias=alias_gen,
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
        self.assertEquals(user.alias, alias_gen)

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
            self.assertNotEqual(400, resp.status_code)

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

        resp = self.testClient.get('/reactivate?e=' + encrypted_activation_info)
        self.assertEqual(200, resp.status_code)

        resp = self.testClient.post('/reactivate',
                                    data=dict(username=user.username,
                                              reactivation_code=user.activation_code
                                              )
                                    )
        self.assertEqual(302, resp.status_code)

        user = userService.get_user_by_username(user.username)

        # values below should have changed
        print("user.activation_code=" + str(user.activation_code))
        print("user.failed_attempt_count=" + str(user.failed_attempt_count))
        self.assertTrue(user.activation_code is None)
        self.assertEqual(0, user.failed_attempt_count)

#
    def test_get_public_user_list(self):
        print("Running: get_public_user_details")
        user_info = commonHelper.get_default_customer_and_token()
        print("user_info=" + str(user_info))

        resp = self.testClient.get('/api/v1.0/public/user/list',
                                   headers={"Authorization": "bearer " + user_info['token']})

        self.debug_response(resp)

        self.assertEqual(200, resp.status_code)
        self.assertEqual("application/json", resp.content_type)

        response_data = json.loads(resp.data)

        found = False
        for user_data in response_data['data']:
            if user_data['user_uuid'] == commonHelper.DEFAULT_PUBLIC_SUBSCRIBED_UUID:
                found = True

        self.assertTrue(found)

    def test_get_public_profile(self):
        print("Running: test_get_public_profile")
        user_info_1 = commonHelper.create_public_user_and_token(self.testClient)
        print("user_info=" + str(user_info_1))

        new_user_2 = commonHelper.create_public_user()

        resp = self.testClient.get('/api/v1.0/public/user/profile/' + str(new_user_2.user_uuid),
                                   headers={"Authorization": "bearer " + user_info_1['token']})

        self.debug_response(resp)

        self.assertEqual(200, resp.status_code)
        self.assertEqual("application/json", resp.content_type)

        response_data = json.loads(resp.data)

        self.assertEqual(str(new_user_2.user_uuid), response_data['data']['user_uuid'])
        self.assertEqual(str(new_user_2.alias), response_data['data']['alias'])
        self.assertTrue(response_data['data']['user_uuid_digest'] is not None)


if __name__ == '__main__':
    unittest.main()

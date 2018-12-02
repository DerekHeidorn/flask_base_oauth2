import json
import unittest
from urllib import parse
from tests.web.baseTest import BaseTest
from tests.utils import randomUtil
from tests.helpers import commonHelper


class PrivateUserApiTestCase(BaseTest):

    def test_user_profile(self):
        print("Running: test_user_profile")
        user_info = commonHelper.create_public_user_and_token(self.testClient)
        print("user_info=" + str(user_info))
        new_user = user_info["user"]

        print("token=" + user_info['token'])
        resp = self.testClient.get('/api/v1.0/my/profile',
                                   headers={"Authorization": "bearer " + user_info['token']})

        self.debug_response(resp)

        self.assertEqual(200, resp.status_code)
        self.assertEqual("application/json", resp.content_type)

        response_data = json.loads(resp.data)

        self.assertEqual(new_user.alias, response_data['data']['alias'])

    def test_update_my_account_password(self):
        print("Running: update_public_account_password")
        user_info = commonHelper.create_public_user_and_token(self.testClient)
        new_user = user_info["user"]
        username = new_user.username
        new_password = 'MySecretPassword123'

        json_string = json.dumps({"old_password": commonHelper.DEFAULT_PUBLIC_USER_PASSWORD,
                                  "new_password": new_password})

        resp = self.testClient.put('/api/v1.0/my/account/password',
                                   headers={"Authorization": "bearer " + user_info['token']},
                                   data=json_string)

        self.debug_response(resp)

        self.assertEqual(200, resp.status_code)

        # -----------------------------------------------
        #  Login
        # -----------------------------------------------
        resp = self.testClient.post('/login',
                                    data=dict(
                                              username=username,
                                              password=new_password,
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

    def test_update_my_account_username(self):
        print("Running: test_update_public_account_username")
        user_info = commonHelper.create_public_user_and_token(self.testClient)
        new_user = user_info["user"]

        password = commonHelper.DEFAULT_PUBLIC_USER_PASSWORD
        old_username = new_user.username
        new_username = randomUtil.random_username()

        json_string = json.dumps({"password": password,
                                  "old_username": old_username,
                                  "new_username": new_username})

        resp = self.testClient.put('/api/v1.0/my/account/username',
                                   headers={"Authorization": "bearer " + user_info['token']},
                                   data=json_string)

        self.debug_response(resp)

        self.assertEqual(200, resp.status_code)

        # -----------------------------------------------
        #  Login
        # -----------------------------------------------
        resp = self.testClient.post('/login',
                                    data=dict(
                                              username=new_username,
                                              password=password,
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

    def test_update_public_account_username_invalid_username(self):
        print("Running: test_update_public_account_username_invalid_username")
        user_info = commonHelper.create_public_user_and_token(self.testClient)
        new_user = user_info["user"]

        password = commonHelper.DEFAULT_PUBLIC_USER_PASSWORD
        old_username = new_user.username
        new_username = randomUtil.random_string(5, 6)

        json_string = json.dumps({"password": password,
                                  "old_username": old_username,
                                  "new_username": new_username})

        resp = self.testClient.put('/api/v1.0/my/account/username',
                                   headers={"Authorization": "bearer " + user_info['token']},
                                   data=json_string)

        self.debug_response(resp)

        self.assertEqual(400, resp.status_code)


if __name__ == '__main__':
    unittest.main()

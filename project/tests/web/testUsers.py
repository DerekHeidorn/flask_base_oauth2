import json
import unittest
from urllib import parse
from project.tests.web.baseTest import BaseTest 
from project.tests.utils import randomUtil
from project.tests.helpers import commonHelper
from project.app.services import userService


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
        self.assertEquals(302, resp.status_code)
        self.assertEquals("text/html; charset=utf-8", resp.content_type)

        print("resp.location=" + resp.location)
        param_dict = dict(parse.parse_qsl(parse.urlsplit(resp.location).query))
        self.assertEquals('Bearer', param_dict.get('token_type'))
        self.assertTrue(len(param_dict.get('access_token')) > 0)

        # check the database for the new user
        user = userService.get_user_by_username(username)
        self.assertEquals(user.username, username)

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
        self.assertEquals(302, resp.status_code)
        self.assertEquals("text/html; charset=utf-8", resp.content_type)

        print("resp.location=" + resp.location)
        param_dict = dict(parse.parse_qsl(parse.urlsplit(resp.location).query))
        self.assertEquals('Bearer', param_dict.get('token_type'))
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
        self.assertEquals(302, resp.status_code)
        self.assertEquals("text/html; charset=utf-8", resp.content_type)

        print("resp.location=" + resp.location)
        param_dict = dict(parse.parse_qsl(parse.urlsplit(resp.location).query))
        self.assertEquals('Bearer', param_dict.get('token_type'))
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
        self.assertEquals(302, resp.status_code)
        self.assertEquals("text/html; charset=utf-8", resp.content_type)

    def test_user_profile(self):
        print("Running: test_user_profile")
        user_info = commonHelper.create_public_user_and_token(self.testClient)
        print("user_info=" + str(user_info))
        new_user = user_info["user"]

        print("token=" + user_info['token'])
        resp = self.testClient.get('/api/v1.0/public/user/profile',
                                   headers={"Authorization": "bearer " + user_info['token']})

        self.debug_response(resp)

        self.assertEquals(200, resp.status_code)
        self.assertEquals("application/json", resp.content_type)

        response_data = json.loads(resp.data)

        self.assertEquals(new_user.username, response_data['username'])


if __name__ == '__main__':
    unittest.main()

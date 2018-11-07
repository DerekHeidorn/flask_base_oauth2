
import unittest
from urllib import parse
from project.tests.web.baseTest import BaseTest 
from project.tests.utils import randomUtil

from project.app.services import userService


class UserServiceTestCase(BaseTest):

    def testSignup(self):
        print("Running: testSignup")
        username = randomUtil.random_username()
        password = randomUtil.random_string(10, 25)
        resp = self.testClient.post('/signup',
                                    data=dict(username=username,
                                              password=password,
                                              passwordRepeat=password,
                                              grant_type="password",
                                              client_id="CLTID-Zeq1LRso5q-iLU9RKCKnu"
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

    def testLogin(self):
        print("Running: testSignup")
        username_gen = randomUtil.random_username()
        password_gen = randomUtil.random_string(10, 25)

        # -----------------------------------------------
        #  Signup
        # -----------------------------------------------
        resp = self.testClient.post('/signup',
                                    data=dict(
                                              username=username_gen,
                                              password=password_gen,
                                              passwordRepeat=password_gen,
                                              grant_type="password",
                                              client_id="CLTID-Zeq1LRso5q-iLU9RKCKnu"
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
                                              client_id="CLTID-Zeq1LRso5q-iLU9RKCKnu"
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
                                             client_id="CLTID-Zeq1LRso5q-iLU9RKCKnu"
                                             )
                                   )
        self.debug_response(resp)

        # should be redirected to new page
        self.assertEquals(302, resp.status_code)
        self.assertEquals("text/html; charset=utf-8", resp.content_type)


if __name__ == '__main__':
    unittest.main()

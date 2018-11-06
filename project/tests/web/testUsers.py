
import unittest
from urllib import parse
from project.tests.web.baseTest import BaseTest 
from project.tests.utils import randomUtil

from project.app.services import userService


class UserServiceTestCase(BaseTest):

    def testSignup(self):
        print("Running: testSignup")
        usernameGen = randomUtil.randomUsername()
        passwordGen = randomUtil.randomString(10, 25)
        resp = self.testClient.post('/signup',
        data = dict(
            username = usernameGen,
            password = passwordGen,
            passwordRepeat = passwordGen,
            grant_type = "password",
            client_id = "CLTID-Zeq1LRso5q-iLU9RKCKnu"
        ))
        self.debugResponse(resp)

        # should be redirected to new page
        self.assertEquals(302, resp.status_code)
        self.assertEquals("text/html; charset=utf-8", resp.content_type)

        print("resp.location=" + resp.location)
        paramDict = dict(parse.parse_qsl(parse.urlsplit(resp.location).query))
        self.assertEquals('Bearer', paramDict.get('token_type'))
        self.assertTrue(len(paramDict.get('access_token')) > 0)

        # check the database for the new user
        user = userService.getUserByUsername(usernameGen)
        self.assertEquals(user.username, usernameGen)

    def testLogin(self):
        print("Running: testSignup")
        usernameGen = randomUtil.randomUsername()
        passwordGen = randomUtil.randomString(10, 25)


        # -----------------------------------------------
        #  Signup
        # -----------------------------------------------
        resp = self.testClient.post('/signup',
        data = dict(
            username = usernameGen,
            password = passwordGen,
            passwordRepeat = passwordGen,
            grant_type = "password",
            client_id = "CLTID-Zeq1LRso5q-iLU9RKCKnu"
        ))
        self.debugResponse(resp)

        # should be redirected to new page
        self.assertEquals(302, resp.status_code)
        self.assertEquals("text/html; charset=utf-8", resp.content_type)

        print("resp.location=" + resp.location)
        paramDict = dict(parse.parse_qsl(parse.urlsplit(resp.location).query))
        self.assertEquals('Bearer', paramDict.get('token_type'))
        self.assertTrue(len(paramDict.get('access_token')) > 0)

        # check the database for the new user
        user = userService.getUserByUsername(usernameGen)
        self.assertEquals(user.username, usernameGen)

        # -----------------------------------------------
        #  Login
        # -----------------------------------------------
        resp = self.testClient.post('/login',
        data = dict(
            username = usernameGen,
            password = passwordGen,
            grant_type="password",
            client_id="CLTID-Zeq1LRso5q-iLU9RKCKnu"
        ))
        self.debugResponse(resp)

        # should be redirected to new page
        self.assertEquals(302, resp.status_code)
        self.assertEquals("text/html; charset=utf-8", resp.content_type)

        print("resp.location=" + resp.location)
        paramDict = dict(parse.parse_qsl(parse.urlsplit(resp.location).query))
        self.assertEquals('Bearer', paramDict.get('token_type'))
        self.assertTrue(len(paramDict.get('access_token')) > 0)

        # -----------------------------------------------
        #  Logout
        # -----------------------------------------------
        resp = self.testClient.get('/login',
        data = dict(
            username = usernameGen,
            password = passwordGen,
            grant_type="password",
            client_id="CLTID-Zeq1LRso5q-iLU9RKCKnu"
        ))
        self.debugResponse(resp)

        # should be redirected to new page
        self.assertEquals(302, resp.status_code)
        self.assertEquals("text/html; charset=utf-8", resp.content_type)


if __name__ == '__main__':
    unittest.main()

import unittest
from urllib import parse
from project.tests.services.baseTest import BaseTest 
from project.tests.utils import randomUtil
from project.tests.helpers import commonHelper
from project.app.services import userService


class UserServiceTestCase(BaseTest):

    def testGetUserByUsername(self):
        print("running testGetUserByUsername...")
        createdUser = commonHelper.createPublicUser()

        user = userService.getUserByUsername(createdUser.username)
        self.assertEquals(createdUser.username, user.username)
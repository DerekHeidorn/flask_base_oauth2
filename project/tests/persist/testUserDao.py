import unittest
from urllib import parse
from project.tests.persist.baseTest import BaseTest 
from project.tests.utils import randomUtil
from project.tests.helpers import commonHelper
from project.app.persist import userDao


class UserDaoTestCase(BaseTest):

    def testGetUserByUsername(self):
        print("running testGetUserByUsername...")
        createdUser = commonHelper.createPublicUser()

        user = userDao.getUserByUsername(createdUser.username)
        self.assertEquals(createdUser.username, user.username)
import pytest
import unittest
import json
from project.tests.web.baseTest import BaseTest 
from project.tests.utils.randomUtil import randomUsername 
from project.tests.utils.randomUtil import randomString


class UserServiceTestCase(BaseTest):

    def createUser(self):
        passwordGen = randomString(10, 25)
        resp = self.testClient.post('/api/v1.0/customer/signup',data = dict(
            username = randomUsername(),
            password = passwordGen,
            passwordRepeat = passwordGen
        ))
        self.debugResponse(resp)
        self.assertEquals(201, resp.status_code)
        responseData = json.loads(resp.data)

        return responseData["id"]

    def testSignup(self):
        print("Running: testSignup")
        passwordGen = randomString(10, 25)
        resp = self.testClient.post('/api/v1.0/customer/signup',
        content_type = 'application/json',
        data = dict(
            username = randomUsername(),
            password = passwordGen,
            passwordRepeat = passwordGen,
            grant_type = "password",
            client_id = "CLTID-Zeq1LRso5q-iLU9RKCKnu",
            csrf_token = "ImViMmIzNTAyMzliMjg1ZDc3YmExZTg3NTMyOGNhMjg2OTgwYTc3NTIi.DsN71w.qXREVWkiPt0uc6fdZ8jd7_iP-2c"
        ))
        self.debugResponse(resp)

        self.assertEquals(201, resp.status_code)
        responseData = json.loads(resp.data)
        assert responseData["id"] is not None
        assert responseData["url"] is not None

        return responseData["id"]

    def xtestUserById_OK(self):
        print("Running: test_user_by_id_OK")
        id = self.createUser()


        print("\nRunning: test_user_by_id_OK")
        resp = self.testClient.get('/api/v1.0/admin/user/' + str(id),
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"})
        
        self.debugResponse(resp)
        self.assertEquals( 200, resp.status_code)
        user = json.loads(resp.data)

        assert user is not None
        
        self.assertEquals(id, user["id"])
        self.assertEquals("Tester", user["firstName"])

    def xtestUpdateUser(self):
        print("Running: test_update_user")
        id = self.createUser()
        newFirstName = "UpdatedTester"
        newLastName = "UpdatedAuto"
        newUsername = "updated.auto@tester.com"

        print("\nRunning: test_update_user")
        resp = self.testClient.put('/api/v1.0/admin/user/' + str(id),
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"},
                            data = dict(
            firstName = newFirstName,
            lastName = newLastName,
            username = newUsername
        ))
        self.debugResponse(resp)
        user = json.loads(resp.data)

        assert user is not None
        
        self.assertEquals(id,  user["id"])
        self.assertEquals( newFirstName , user["firstName"])
        self.assertEquals( newLastName , user["lastName"])
        self.assertEquals( newUsername , user["username"])


    def xtestUserDelete(self):
        print("Running: test_user_delete")
        id = self.createUser()

        print("\nRunning: test_api_candidate_by_id_OK")
        resp = self.testClient.delete('/api/v1.0/user/' + str(id),
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"})
        
        print("resp.data=" + str(resp.data))


if __name__ == '__main__':
    unittest.main()

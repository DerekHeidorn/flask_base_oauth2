import pytest
import unittest
import json
from baseTest import BaseTest 
from tests.utils.randomUtil import randomLogin 
from tests.utils.randomUtil import randomString


# @pytest.fixture(scope="class", autouse=True)
class UserServiceTestCase(BaseTest):

    def createUser(self):
        resp = self.testClient.post('/api/v1.0/user',data = dict(
            firstName = "Tester",
            lastName = "Auto",
            login = randomLogin(),
            password = randomString(10, 25)
        ))
        self.debugResponse(resp)
        assert resp.status_code == 201
        responseData = json.loads(resp.data)

        return responseData["id"]

    def test_user_create(self):
        print("Running: test_user_create")
        resp = self.testClient.post('/api/v1.0/user',data = dict(
            firstName = "Tester",
            lastName = "Auto",
            login = randomLogin(),
            password = randomString(10, 25)
        ))
        self.debugResponse(resp)

        assert resp.status_code == 201
        responseData = json.loads(resp.data)
        assert responseData["id"] is not None
        assert responseData["url"] is not None
        # self.my_test_read(tmp_data["id"])

        return responseData["id"]

    def test_user_by_id_OK(self):
        print("Running: test_user_by_id_OK")
        id = self.createUser()


        print("\nRunning: test_user_by_id_OK")
        resp = self.testClient.get('/api/v1.0/user/' + str(id),
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"})
        
        self.debugResponse(resp)
        assert resp.status_code == 200
        user = json.loads(resp.data)

        assert user is not None
        
        assert id == user["id"]
        assert "Tester" == user["firstName"]

    def test_update_user(self):
        print("Running: test_update_user")
        id = self.createUser()
        newFirstName = "UpdatedTester"
        newLastName = "UpdatedAuto"
        newLoginName = "updated.auto@tester.com"

        print("\nRunning: test_update_user")
        resp = self.testClient.put('/api/v1.0/user/' + str(id),
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"},
                            data = dict(
            firstName = newFirstName,
            lastName = newLastName,
            login = newLoginName
        ))
        self.debugResponse(resp)
        user = json.loads(resp.data)

        assert user is not None
        
        assert id == user["id"]
        assert newFirstName == user["firstName"]
        assert newLastName == user["lastName"]
        assert newLoginName == user["login"]


    def test_user_delete(self):
        print("Running: test_user_delete")
        id = self.createUser()

        print("\nRunning: test_api_candidate_by_id_OK")
        resp = self.testClient.delete('/api/v1.0/user/' + str(id),
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"})
        
        print("resp.data=" + str(resp.data))
        # tmp_data = json.loads(resp.data)

        #print("tmp_data=" + tmp_data)

        # user = tmp_data["user"][0]

        # print("user=" + user)
        # print("type(user)=" + str(type(user)))
        # print("type(user)=" + str(type(eval(user))))

        # userDictionary = eval(user)

        # assert user is not None
        
        # assert 1 == userDictionary["id"]
        # assert "Tester" == userDictionary["first_name"]

if __name__ == '__main__':
    unittest.main()
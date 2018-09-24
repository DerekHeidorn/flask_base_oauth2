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
            first_name = "Tester",
            last_name = "Auto",
            login = randomLogin(),
            password = randomString(10, 25)
        ))
        self.debugResponse(resp)
        tmp_data = json.loads(resp.data)

        return tmp_data["id"]

    def test_user_create(self):
        print("Running: test_user_create")
        resp = self.testClient.post('/api/v1.0/user',data = dict(
            first_name = "Tester",
            last_name = "Auto",
            login = randomLogin(),
            password = randomString(10, 25)
        ))
        self.debugResponse(resp)
        tmp_data = json.loads(resp.data)
        assert tmp_data["id"] is not None
        assert tmp_data["url"] is not None
        # self.my_test_read(tmp_data["id"])

        return tmp_data["id"]

    def test_user_by_id_OK(self):
        print("Running: test_user_by_id_OK")
        id = self.createUser()


        print("\nRunning: test_user_by_id_OK")
        resp = self.testClient.get('/api/v1.0/user/' + str(id),
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"})
        
        print("resp.data=" + str(resp.data))
        assert resp.status_code == 200
        tmp_data = json.loads(resp.data)

        #print("tmp_data=" + tmp_data)

        user = tmp_data["user"]

        print("user=" + user)
        print("type(user)=" + str(type(user)))
        print("type(user)=" + str(type(eval(user))))

        userDictionary = eval(user)

        assert user is not None
        
        assert id == userDictionary["id"]
        assert "Tester" == userDictionary["first_name"]

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
            first_name = newFirstName,
            last_name = newLastName,
            login = newLoginName
        ))
        
        print("resp.data=" + str(resp.data))
        tmp_data = json.loads(resp.data)

        #print("tmp_data=" + tmp_data)

        user = tmp_data["user"]

        print("user=" + user)
        print("type(user)=" + str(type(user)))
        print("type(user)=" + str(type(eval(user))))

        userDictionary = eval(user)

        assert user is not None
        
        assert id == userDictionary["id"]
        assert newFirstName == userDictionary["first_name"]
        assert newLastName == userDictionary["last_name"]
        assert newLoginName == userDictionary["login"]


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

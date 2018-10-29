import pytest
import unittest
import json
from baseTest import BaseTest 

# @pytest.fixture(scope="class", autouse=True)
class CodetableTestCases(BaseTest):

    def test_CtUserStatuses_OK(self):
        print("Running: test_CtUserStatuses_OK")

        resp = self.testClient.get('/api/v1.0/codetables/' + "CtUserStatuses",
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"})
        self.debugResponse(resp)
        assert resp.status_code == 200
        codeDict1 = json.loads(resp.data)

        assert "1" == codeDict1[0]["code"]
        assert "Batch" == codeDict1[0]["description"]
        

    def test_CtUserStatuses_cached_OK(self):
        print("Running: test_CtUserStatuses_cached_OK")

        resp = self.testClient.get('/api/v1.0/codetables/' + "CtUserStatuses",
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"})
        self.debugResponse(resp)
        assert resp.status_code == 200
        codeDict1 = json.loads(resp.data)

        assert "1" == codeDict1[0]["code"]
        assert "Batch" == codeDict1[0]["description"]       

    def test_CtUserTypes_OK(self):
        print("Running: test_CtUserTypes_OK")

        resp = self.testClient.get('/api/v1.0/codetables/' + "CtUserTypes",
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"})
        self.debugResponse(resp)

        assert resp.status_code == 200
        codeDict1 = json.loads(resp.data)

        assert "A" == codeDict1[0]["code"]
        assert "Active" == codeDict1[0]["description"]

if __name__ == '__main__':
    unittest.main()
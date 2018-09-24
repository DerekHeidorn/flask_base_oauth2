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
        tmp_data = json.loads(resp.data)

        codeDict1 = eval(tmp_data[0])

        assert "1" == codeDict1["code"].strip()
        assert "Batch" == codeDict1["description"].strip()
        

    def test_CtUserStatuses_cached_OK(self):
        print("Running: test_CtUserStatuses_cached_OK")

        resp = self.testClient.get('/api/v1.0/codetables/' + "CtUserStatuses",
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"})
        self.debugResponse(resp)
        assert resp.status_code == 200
        tmp_data = json.loads(resp.data)

        codeDict1 = eval(tmp_data[0])

        assert "1" == codeDict1["code"].strip()
        assert "Batch" == codeDict1["description"].strip()        

    def test_CtUserTypes_OK(self):
        print("Running: test_CtUserTypes_OK")

        resp = self.testClient.get('/api/v1.0/codetables/' + "CtUserTypes",
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"})
        self.debugResponse(resp)

        assert resp.status_code == 200
        tmp_data = json.loads(resp.data)

        codeDict1 = eval(tmp_data[0])

        assert "A" == codeDict1["code"].strip()
        assert "Active" == codeDict1["description"].strip()

if __name__ == '__main__':
    unittest.main()
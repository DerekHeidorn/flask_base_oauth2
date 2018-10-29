import pytest
import unittest
import json
from project.tests.web.baseTest import BaseTest 

# @pytest.fixture(scope="class", autouse=True)
class CommonTestCases(BaseTest):

    def testVersion_OK(self):
        print("Running: test_version_OK")

        resp = self.testClient.get('/api/v1.0/app/version',
                            headers={"MY_AUTH_TOKEN":"81c4e12b6879000837a3e7206795ee9ca874986cc97984d383c64093f5cc352d"})
        self.debugResponse(resp)
        assert resp.status_code == 200
        
        codeDict1 = json.loads(resp.data)
        assert "1.0" == codeDict1["application.version"].strip()



if __name__ == '__main__':
    unittest.main()
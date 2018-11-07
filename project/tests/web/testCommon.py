
import unittest
import json
from project.tests.web.baseTest import BaseTest 


class CommonTestCases(BaseTest):

    def testVersion_OK(self):
        print("Running: test_version_OK")

        resp = self.testClient.get('/api/v1.0/app/version')
        self.debug_response(resp)
        assert resp.status_code == 200
        
        code_dict = json.loads(resp.data)
        print("codeDict1=" + str(code_dict))
        assert "0.1" == code_dict["application.version"].strip()


if __name__ == '__main__':
    unittest.main()

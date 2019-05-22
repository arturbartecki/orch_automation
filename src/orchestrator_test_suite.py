import unittest
import os
import datetime
from HtmlTestRunner import HTMLTestRunner
# import HTMLTestRunner

import orch_automation_tools
import JP_test_suite
 
direct = os.getcwd()
 
class CITTestSuite(unittest.TestCase):
    CONTROL_JSON = os.path.join(
            os.getcwd(),
            'json_flow_data',
            'CIT_RESULTS.json'
    )
    def setUp(self):
        orch_automation_tools.create_directory(self.CONTROL_JSON)

    def test_Issue(self):
        smoke_test = unittest.TestSuite()
        smoke_test.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(JP_test_suite.CITPNGJPExportTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(JP_test_suite.CITPNGJPImportTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(JP_test_suite.CITPNGJPPaymentTests)
        ])
        # dir_name = orch_automation_tools.parse_json_data(self.CONTROL_JSON)['current_id']
        # filename = os.path.join(direct, dir_name, 'test_report.html')
        outfile = open('test_report.html', "w")

        runner1 = HTMLTestRunner(
            combine_reports=True,
            stream=outfile,
            report_title='Test Report'
        )

        runner1.run(smoke_test)

 
if __name__ == '__main__':
    unittest.main()
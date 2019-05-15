import unittest
import os
import datetime
from HtmlTestRunner import HTMLTestRunner
# import HTMLTestRunner

import JP_test_suite
 
direct = os.getcwd()
 
class MyTestSuite(unittest.TestCase):
    
    def setUp(self):
        """
        Function prepares directory for reporting and pass it into json file.
        Tests can use this directory to copy excell files.
        """
        nowdate = datetime.datetime.now()
        str_nowdate = nowdate.strftime('%d_%m_%Y_%H_%M')

    def test_Issue(self):
 
        smoke_test = unittest.TestSuite()
        smoke_test.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(JP_test_suite.CITPNGJPExportTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(JP_test_suite.CITPNGJPImportTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(JP_test_suite.CITPNGJPPaymentTests)
        ])
        filename = os.path.join(direct, 'test_report.html')
        outfile = open(filename, "w")

        runner1 = HTMLTestRunner(
            combine_reports=True,
            stream=outfile,
            report_title='Test Report'
        )
 
        runner1.run(smoke_test)

 
if __name__ == '__main__':
    unittest.main()
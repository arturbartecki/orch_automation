# Standard library import
import os
import time
import unittest

# Third party import
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

# Local import
import access_file
from excel_operations import rename_excel_template, generate_pnglo_JP_invoice


# class JPTests(unittest.TestCase):
#     BASE_URL = 'https://test-ct.maersk.com/'
#     LOGIN = access_file.user_4pl_payment
#     PASSWORD = access_file.pass_4pl_payment

#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(20)
#         self.driver.get(self.BASE_URL)
#         self.driver.maximize_window()
#         self.test_file = os.path.join(
#             os.getcwd(), "PNGLO001R_JP_INVOICE_SO_Template.xlsx"
#         )

#     def test_invoices_module(self):
#         driver = self.driver
#         actionChains = ActionChains(driver)
#         # Login as appropriate user
#         login = driver.find_element_by_xpath('//*[@id="f7"]/div[2]/div/input')
#         login.send_keys(self.LOGIN)
#         password = driver.find_element_by_xpath(
#             '//*[@id="f8"]/div[2]/div/input'
#         )
#         password.send_keys(self.PASSWORD)
#         password.send_keys(Keys.RETURN)

#         # Go to P&G Payment Tracker To Do List JP and wait untill it loads
#         go_to_pg_payment_tracker_jp(driver)

#         # Go to example tasks
#         driver.find_element_by_link_text(
#             'Confirm Invoice Approval by Lane Manager (JP)'
#         ).click()

#         # Select and open context menu, select View option
#         element = driver.find_element_by_xpath('//*[@id="r146"]')
#         element.click()
#         actionChains.context_click(element).perform()
#         driver.find_element_by_xpath(
#             '//*[@id="contextMenu"]/ul/a[1]/li'
#         ).click()
#         time.sleep(3)

#         # Close current tab, and test uploading file
#         driver.close()
#         driver.switch_to.window(driver.window_handles[-1])

#         # Go to file upload, and make sure it loads
#         driver.find_element_by_id('p15').click()
#         try:
#             WebDriverWait(driver, 5).until(
#                 EC.title_is('Excel Sheet Upload')
#             )
#         except TimeoutException:
#             driver.switch_to.window(driver.window_handles[-1])

#         driver.switch_to.window(driver.window_handles[-1])
#         actionChains = ActionChains(driver)

#         # Locate and move over Browse button to run JS script
#         upload_button = driver.find_element_by_id('AFUSelectFileButtont3_0')
#         actionChains.move_to_element(upload_button).perform()

#         # Locate and remove all styling from invisible div
#         invisible_div = driver.find_element_by_xpath('/html/body/div[3]')
#         driver.execute_script("arguments[0].style = ' ';", invisible_div)

#         # Submit test file
#         file_input = driver.find_element_by_xpath('/html/body/div[3]/input')
#         file_input.send_keys(os.path.join(os.getcwd(), self.test_file))

#         # Commented out submit button click
#         # driver.find_element_by_xpath('//*[@id="t2"]/div[5]/a').click()

#         time.sleep(5)
#         driver.close()
#         driver.switch_to.window(driver.window_handles[-1])

#         # Go to task list and search options
#         go_to_pg_payment_tracker_jp(driver)
#         driver.find_element_by_xpath('//*[@id="tabs"]/div[1]/a').click()
#         driver.find_element_by_xpath(
#             '//*[@id="t65_14513"]'
#         ).send_keys('TestDataSearch')
#         driver.find_element_by_xpath('//*[@id="t53"]/div[27]/a[1]').click()
#         time.sleep(5)
#         driver.close()
#         driver.switch_to_window(driver.window_handles[-1])

#         # Logout the user
#         driver.find_element_by_xpath('//*[@id="page"]/div[2]/a[4]/div').click()
#         driver.find_element_by_xpath('//*[@id="conf"]/div[3]/a[1]').click()
#         time.sleep(5)


class JPCtiTests(unittest.TestCase):
    BASE_URL = 'https://ct-cit.damco.com/'
    LOGIN_4PL = access_file.user_4pl
    PASSWORD_4PL = access_file.pass_4pl
    LOGIN_3PL = access_file.user_3pl
    PASSWORD_3PL = access_file.pass_3pl
    LOGIN_WH = access_file.user_wh
    PASSWORD_WH = access_file.pass_wh
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(20)
        self.driver.get(self.BASE_URL)
        self.driver.maximize_window()
        self.test_file = os.path.join(
            os.getcwd(), "PNGLO001R_IMPORT_SO_IMP_20193020.xlsx"
        )

    def test_pg_process(self):
        rename_excel_template()
        data_dict = generate_pnglo_JP_invoice()
        driver = self.driver
        actionChains = ActionChains(driver)

        # Login as 4PL user
        login = driver.find_element_by_xpath('//*[@id="f7"]/div[2]/div/input')
        login.send_keys(self.LOGIN_4PL)
        password = driver.find_element_by_xpath(
            '//*[@id="f8"]/div[2]/div/input'
        )
        password.send_keys(self.PASSWORD_4PL)
        password.send_keys(Keys.RETURN)

        # Commented out the file upload section

        driver.find_element_by_id('p21').click()
        try:
            WebDriverWait(driver, 5).until(
                EC.title_is('Excel Sheet Upload')
            )
        except TimeoutException:
            driver.switch_to.window(driver.window_handles[-1])

        driver.switch_to.window(driver.window_handles[-1])
        actionChains = ActionChains(driver)

        # Locate and move over Browse button to run JS script
        upload_button = driver.find_element_by_xpath('//*[@id="AFUSelectFileButtonWrappert3_0"]')
        actionChains.move_to_element(upload_button).perform()

        # Locate and remove all styling from invisible div
        invisible_div = driver.find_element_by_xpath('/html/body/div[3]')
        driver.execute_script("arguments[0].style = ' ';", invisible_div)

        # Submit test file
        file_input = driver.find_element_by_xpath('/html/body/div[3]/input')
        file_input.send_keys(os.path.join(os.getcwd(), self.test_file))

        # Commented out submit button click
        driver.find_element_by_xpath('//*[@id="t2"]/div[5]/a').click()
        # time.sleep(30)
        try:
            WebDriverWait(driver, 120).until(
                EC.text_to_be_present_in_element((By.XPATH, '//*[@id="r18"]/td[6]'), 'Accepted')
            )
        except TimeoutException:
            driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])

        driver.find_element_by_id('p20').click()
        try:
            WebDriverWait(driver, 5).until(
                EC.title_is('4PL Task List (JP)')
            )
        except TimeoutException:
            driver.switch_to.window(driver.window_handles[-1])
        driver.find_element_by_xpath('//*[@id="tabs"]/div[1]/a').click()

        # Target search field and pass the SHIPMENT PO
        shipment_po_field = driver.find_element_by_xpath('//*[@id="t65_20114"]')
        shipment_po_field.send_keys(data_dict['shipment'])
        # shipment_po_field.send_keys('DEPHMTEST142')
        driver.find_element_by_xpath('//*[@id="t53"]/div[21]/a[1]').click()
        # 1st task
        actionChains = ActionChains(driver)
        uci_task = driver.find_element_by_xpath("//div[contains(text(),'Confirm Service PO / PO Conditions Exist/Correct (JP)')]")
        # uci_task = driver.find_element_by_link_text('Confirm Service PO / PO Conditions Exist/Correct (JP)')
        uci_task.click()
        time.sleep(2)

        uci_task = driver.find_element_by_xpath("//div[contains(text(),'Confirm Service PO / PO Conditions Exist/Correct (JP)')]")
        actionChains.context_click(uci_task).perform()
        driver.find_element_by_xpath(
            '//*[@id="contextMenu"]/ul/a[4]/li'
        ).click()
        time.sleep(5)
        comment_field = select_input_by_label(driver, 'User Comments', 'textarea')
        comment_field.send_keys('Test data comment')
        driver.find_element_by_xpath("//a[contains(text(),'Accept')]").click()
        time.sleep(5)

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 2nd task completion
        driver.switch_to.window(driver.window_handles[-1])
        actionChains = ActionChains(driver)
        uci_task = driver.find_element_by_xpath("//div[contains(text(),'Upload Commercial Invoice (Import) (JP)')]")
        # uci_task = driver.find_element_by_link_text('Confirm Service PO / PO Conditions Exist/Correct (JP)')
        uci_task.click()
        time.sleep(2)
        # actionChains = ActionChains(driver)
        uci_task = driver.find_element_by_xpath("//div[contains(text(),'Upload Commercial Invoice (Import) (JP)')]")
        actionChains.context_click(uci_task).perform()
        time.sleep(2)
        driver.find_element_by_xpath(
            '//*[@id="contextMenu"]/ul/a[4]/li'
        ).click()
        # driver.find_element_by_xpath('//*[@id="t323_7"]').send_keys('Test data comment')
        # driver.find_element_by_xpath('//*[@id="t46"]/div[7]/a').click()
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        # Commercial Invoice Number
        # driver.find_element_by_xpath('//*[@id="t322_18_1"]').send_keys('Test data')
        cin_field = select_input_by_label(driver, 'Commercial Invoice Number', 'input')
        cin_field.send_keys("test data")
        # Goods Value
        # driver.find_element_by_xpath('//*[@id="t322_18_3"]').send_keys('Test data')
        gv_field = select_input_by_label(driver, 'Goods Value', 'input')
        gv_field.send_keys('test data')
        # Incoterm used in CI
        # driver.find_element_by_xpath('//*[@id="t322_18_2"]').send_keys('Test data')
        iuic_field = comment_field = select_input_by_label(driver, 'Incoterm used in CI', 'input')
        iuic_field.send_keys('test data')
        # Currency
        # driver.find_element_by_xpath('//*[@id="t322_18_4"]').send_keys('Test data')
        cur_field = comment_field = select_input_by_label(driver, 'Currency', 'input')
        cur_field.send_keys('test data')
        driver.find_element_by_xpath("//a[contains(text(),'Proceed')]").click()
        # driver.find_element_by_xpath('//*[@id="t46"]/div[11]/a').click()

        # try:
        #     WebDriverWait(driver, 90).until(
        #         EC.text_to_be_present_in_element((By.XPATH, '//*[@id="r18"]/td[6]'), 'Accepted')
        #     )
        # except TimeoutException:
        #     driver.switch_to.window(driver.window_handles[-1])

        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        actionChains = ActionChains(driver)
        time.sleep(2)
        upload_button = driver.find_element_by_xpath("//span[contains(text(),'Browse..')]")
        # upload_button = driver.find_element_by_id('AFUSelectFileUploadContainert421_0__7')
        # upload_button = driver.find_element_by_xpath('//*[@id="AFUSelectFileUploadContainert421_0__7"]')
        actionChains.move_to_element(upload_button).perform()

        # Locate and remove all styling from invisible div
        invisible_div = driver.find_element_by_xpath('/html/body/div[4]')
        driver.execute_script("arguments[0].style = ' ';", invisible_div)

        # Submit test file
        file_input = driver.find_element_by_xpath('/html/body/div[4]/input')
        file_input.send_keys(os.path.join(os.getcwd(), self.test_file))

        # Commented out submit button click
        driver.find_element_by_xpath("//a[contains(text(),'Save')]").click()
        # driver.find_element_by_xpath('//*[@id="t342"]/div[6]/a').click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # Logout and login as 3PL user

        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element_by_xpath('//*[@id="page"]/div[2]/a[4]/div').click()
        driver.find_element_by_xpath('//*[@id="conf"]/div[3]/a[1]').click()
        time.sleep(5)

        # Login as 3PL user
        login = driver.find_element_by_xpath('//*[@id="f7"]/div[2]/div/input')
        login.send_keys(self.LOGIN_3PL)
        password = driver.find_element_by_xpath(
            '//*[@id="f8"]/div[2]/div/input'
        )
        password.send_keys(self.PASSWORD_3PL)
        password.send_keys(Keys.RETURN)
        time.sleep(5)

        driver.find_element_by_id('p14').click()
        try:
            WebDriverWait(driver, 5).until(
                EC.title_is('P&G 3PL Task List JP')
            )
        except TimeoutException:
            driver.switch_to.window(driver.window_handles[-1])
        driver.find_element_by_xpath('//*[@id="tabs"]/div[1]/a').click()
        shipment_po_field = driver.find_element_by_xpath('//*[@id="t65_20114"]')
        shipment_po_field.send_keys(data_dict['shipment'])
        # shipment_po_field.send_keys('DEPHMTEST142')
        driver.find_element_by_xpath('//*[@id="t53"]/div[21]/a[1]').click()
        time.sleep(5)

        uci_task = driver.find_element_by_xpath("//div[contains(text(),'Confirm FTA Documents Received & Accurate (JP)')]")
        # uci_task = driver.find_element_by_link_text('Confirm Service PO / PO Conditions Exist/Correct (JP)')
        uci_task.click()
        time.sleep(2)
        actionChains = ActionChains(driver)
        uci_task = driver.find_element_by_xpath("//div[contains(text(),'Confirm FTA Documents Received & Accurate (JP)')]")
        actionChains.context_click(uci_task).perform()
        time.sleep(2)
        driver.find_element_by_xpath(
            '//*[@id="contextMenu"]/ul/a[4]/li'
        ).click()
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])
        # select_field = Select(driver.find_element_by_xpath('//select'))
        # time.sleep(100)
        # select_field = Select(driver.find_element_by_id('t303_18_1'))
        select_field = Select(select_input_by_label(driver, 'FTA Document Name', 'select'))
        # select_field = Select(driver.find_element_by_xpath("//div[@name='FTA Document Name']//select"))
        select_field.select_by_index(1)
        date_field = select_input_by_label(driver, 'FTA Received Date', 'input')
        date_field.send_keys('April/30/2019')
        submit_button = driver.find_element_by_xpath("//a[contains(text(),'Accept')]").click()
        time.sleep(15)

# FTA Received Date - April/30/2019

# Helper functions
def go_to_pg_payment_tracker_jp(driver):
    """
    Go to P&G Payment Tracker To Do List JP and make sure it loads
    """
    driver.find_element_by_id('p14').click()
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (
                    By.LINK_TEXT,
                    'Confirm Invoice Approval by Lane Manager (JP)'
                )
            )
        )
    except TimeoutException:
        driver.switch_to.window(driver.window_handles[-1])


def select_input_by_label(driver, label, input_type):
    # func_string = f'driver.find_element_by_xpath("//div[contains(text(),"{label}")]/{input_type}")'
    func_string = 'find_element_by_xpath'
    # //div[contains(@class, 'Caption') and text()='Model saved']
    return getattr(driver, func_string)(f'//div[@name="{label}"]//{input_type}')
    # return  exec(func_string)

if __name__ == "__main__":
    unittest.main()

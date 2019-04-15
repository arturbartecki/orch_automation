import unittest
import time
import os

import access_file

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JPTests(unittest.TestCase):
    BASE_URL = 'https://test-ct.maersk.com/'
    LOGIN = access_file.user_4pl_payment
    PASSWORD = access_file.pass_4pl_payment

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(20)
        self.driver.get(self.BASE_URL)
        self.test_file = os.path.join(
            os.getcwd(), "PNGLO001R_JP_INVOICE_SO_Template.xlsx"
        )

    def test_invoices_module(self):
        driver = self.driver
        actionChains = ActionChains(driver)
        # Login as appropriate user
        login = driver.find_element_by_xpath('//*[@id="f7"]/div[2]/div/input')
        login.send_keys(self.LOGIN)
        password = driver.find_element_by_xpath(
            '//*[@id="f8"]/div[2]/div/input'
        )
        password.send_keys(self.PASSWORD)
        password.send_keys(Keys.RETURN)

        # Go to P&G Payment Tracker To Do List JP and wait untill it loads
        go_to_pg_payment_tracker_jp(driver)

        # Go to example tasks
        driver.find_element_by_link_text(
            'Confirm Invoice Approval by Lane Manager (JP)'
        ).click()

        # Select and open context menu, select View option
        element = driver.find_element_by_xpath('//*[@id="r146"]')
        element.click()
        actionChains.context_click(element).perform()
        driver.find_element_by_xpath(
            '//*[@id="contextMenu"]/ul/a[1]/li'
        ).click()

        # Close current tab, and test uploading file
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])

        # Go to file upload, and make sure it loads
        driver.find_element_by_id('p15').click()
        try:
            element = WebDriverWait(driver, 5).until(
                EC.title_is('Excel Sheet Upload')
            )
        except TimeoutException:
            driver.switch_to.window(driver.window_handles[-1])

        driver.switch_to.window(driver.window_handles[-1])
        actionChains = ActionChains(driver)

        # Locate and move over Browse button to run JS script
        upload_button = driver.find_element_by_id('AFUSelectFileButtont3_0')
        actionChains.move_to_element(upload_button).perform()

        # Locate and remove all styling from invisible div
        invisible_div = driver.find_element_by_xpath('/html/body/div[3]')
        driver.execute_script("arguments[0].style = ' ';", invisible_div)

        # Submit test file
        file_input = driver.find_element_by_xpath('/html/body/div[3]/input')
        file_input.send_keys(os.path.join(os.getcwd(), self.test_file))
        driver.find_element_by_xpath('//*[@id="t2"]/div[5]/a')
        time.sleep(5)
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])

        # Go to task list and search options
        go_to_pg_payment_tracker_jp(driver)
        driver.find_element_by_xpath('//*[@id="tabs"]/div[1]/a').click()
        driver.find_element_by_xpath('//*[@id="t65_14513"]').send_keys('TestDataSearch')
        driver.find_element_by_xpath('//*[@id="t53"]/div[27]/a[1]').click()
        time.sleep(5)
        driver.close()
        driver.switch_to_window(driver.window_handles[-1])

    # Logout the user
        driver.find_element_by_xpath('//*[@id="page"]/div[2]/a[4]/div').click()
        driver.find_element_by_xpath('//*[@id="conf"]/div[3]/a[1]').click()
        time.sleep(5)

# Helper functions
def go_to_pg_payment_tracker_jp(driver):
    """
    Go to P&G Payment Tracker To Do List JP and make sure it loads
    """
    driver.find_element_by_id('p14').click()
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (
                    By.LINK_TEXT,
                    'Confirm Invoice Approval by Lane Manager (JP)'
                )
            )
        )
    except TimeoutException:
        driver.switch_to.window(driver.window_handles[-1])

if __name__ == "__main__":
    unittest.main()

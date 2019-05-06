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
from selenium.webdriver.chrome.options import Options

# Local import
import access_file
import qa_helper_functions
from excel_operations import rename_excel_template, generate_pnglo_JP_invoice


class JPCtiTests(unittest.TestCase):
    BASE_URL = 'https://ct-cit.damco.com/'
    LOGIN_4PL = access_file.user_4pl
    PASSWORD_4PL = access_file.pass_4pl
    LOGIN_3PL = access_file.user_3pl
    PASSWORD_3PL = access_file.pass_3pl
    LOGIN_WH = access_file.user_wh
    PASSWORD_WH = access_file.pass_wh
    
    def setUp(self):
        chrome_options = Options()  
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
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
        login_user(driver, self.LOGIN_4PL, self.PASSWORD_4PL)
        
        # Upload excel file
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

        driver.find_element_by_xpath('//*[@id="t2"]/div[5]/a').click()

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
        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()

        # Target search field and pass the SHIPMENT PO
        shipment_po_field = select_input_by_label(driver, 'PO# (1st Leg)', 'input[@type="text"]')
        shipment_po_field.send_keys(data_dict['shipment'])
        driver.find_element_by_xpath('//*[@id="t53"]/div[21]/a[1]').click()

        # 1st task
        use_task_context_menu(driver, 'Confirm Service PO / PO Conditions Exist/Correct (JP)', 4)
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
        use_task_context_menu(driver, 'Upload Commercial Invoice (Import) (JP)', 4)
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
 
        # Commercial Invoice Number
        cin_field = select_input_by_label(driver, 'Commercial Invoice Number', 'input')
        cin_field.send_keys("test data")
        # Goods Value
        gv_field = select_input_by_label(driver, 'Goods Value', 'input')
        gv_field.send_keys('test data')
        # Incoterm used in CI
        iuic_field = comment_field = select_input_by_label(driver, 'Incoterm used in CI', 'input')
        iuic_field.send_keys('test data')
        # Currency
        cur_field = comment_field = select_input_by_label(driver, 'Currency', 'input')
        cur_field.send_keys('test data')

        driver.find_element_by_xpath("//a[contains(text(),'Proceed')]").click()

        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        actionChains = ActionChains(driver)
        time.sleep(2)
        upload_button = driver.find_element_by_xpath("//span[contains(text(),'Browse..')]")
        actionChains.move_to_element(upload_button).perform()

        # Locate and remove all styling from invisible div
        invisible_div = driver.find_element_by_xpath('/html/body/div[4]')
        driver.execute_script("arguments[0].style = ' ';", invisible_div)

        # Submit test file
        file_input = driver.find_element_by_xpath('/html/body/div[4]/input')
        file_input.send_keys(os.path.join(os.getcwd(), self.test_file))

        # Commented out submit button click
        time.sleep(3)
        actionChains = ActionChains(driver)
        driver.find_element_by_xpath("//a[contains(text(),'Save')]").click()
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
        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()
        time.sleep(3)
        shipment_po_field = select_input_by_label(driver, 'PO# (1st Leg)', 'input[@type="text"]')
        shipment_po_field.send_keys(data_dict['shipment'])

        driver.find_element_by_xpath('//*[@id="t53"]/div[21]/a[1]').click()
        time.sleep(5)

        # Third
        use_task_context_menu(driver, 'Confirm Pre-Alert Accurate & Complete (JP)', 4)
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])

        select_ci = Select(select_input_by_label(driver, 'Commercial Invoice (Y/N/NA)', 'select'))
        select_ci.select_by_index(1)

        select_bol = Select(select_input_by_label(driver, 'Bill of Lading (Y/N/NA)', 'select'))
        select_bol.select_by_index(1)

        select_plts = Select(select_input_by_label(driver, 'PL/Tally Sheet (Y/N/NA)', 'select'))
        select_plts.select_by_index(1)

        select_coa = Select(select_input_by_label(driver, 'COA (Y/N/NA)', 'select'))
        select_coa.select_by_index(1)

        date_field = select_input_by_label(driver, 'Pre-Alert Received Date', 'input')
        date_field.send_keys('04 30 19 00:00')

        driver.find_element_by_xpath("//a[contains(text(),'Accept')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )
        # Fourth task
        use_task_context_menu(driver, 'Confirm FTA Documents Received & Accurate (JP)', 4)
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])

        select_field = Select(select_input_by_label(driver, 'FTA Document Name', 'select'))
        select_field.select_by_index(1)
        date_field = select_input_by_label(driver, 'FTA Received Date', 'input')
        date_field.send_keys('April/30/2019')
        driver.find_element_by_xpath("//a[contains(text(),'Accept')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # Fifth task
        use_task_context_menu(driver, 'Confirm Additional Import Customs Requirements (JP)', 4)
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])

        select_cn = Select(select_input_by_label(driver, 'Cosmetic Notification (Y/N/NA)', 'select'))
        select_cn.select_by_index(1)

        select_cscl = Select(select_input_by_label(driver, 'Chem Sub Control Law (Y/N/NA)', 'select'))
        select_cscl.select_by_index(1)

        select_jprpa = Select(select_input_by_label(driver, 'JPR Pallet Agreement (Y/N/NA)', 'select'))
        select_jprpa.select_by_index(1)

        select_gic = Select(select_input_by_label(driver, 'Gas Inspect Cert (Y/N/NA)', 'select'))
        select_gic.select_by_index(1)

        select_qdal = Select(select_input_by_label(driver, 'Quasi Drug App Lic (Y/N/NA)', 'select'))
        select_qdal.select_by_index(1)

        select_ac = Select(select_input_by_label(driver, 'ASSIST Cost (Y/N/NA)', 'select'))
        select_ac.select_by_index(1)

        select_flt = Select(select_input_by_label(driver, 'Fire Length Test (Y/N/NA)', 'select'))
        select_flt.select_by_index(1)

        driver.find_element_by_xpath("//a[contains(text(),'Accept')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # Sixth task
        use_task_context_menu(driver, 'Confirm Import HS Code (JP)', 4)
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])

        driver.find_element_by_xpath("//a[contains(text(),'OK & Complete')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # Seventh task
        use_task_context_menu(driver, 'Confirm All Import Documents Accurate and Complete (JP)', 4)
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])

        driver.find_element_by_xpath("//a[contains(text(),'Proceed')]").click()

        actionChains = ActionChains(driver)
        upload_button = driver.find_element_by_xpath("//span[contains(text(),'Browse..')]")
        actionChains.move_to_element(upload_button).perform()

        # Locate and remove all styling from invisible div
        invisible_div = driver.find_element_by_xpath('/html/body/div[4]')
        driver.execute_script("arguments[0].style = ' ';", invisible_div)

        # Submit test file
        file_input = driver.find_element_by_xpath('/html/body/div[4]/input')
        file_input.send_keys(os.path.join(os.getcwd(), self.test_file))

        time.sleep(3)
        driver.find_element_by_xpath("//a[contains(text(),'Save')]").click()
        
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element_by_xpath('//*[@id="page"]/div[2]/a[4]/div').click()
        driver.find_element_by_xpath('//*[@id="conf"]/div[3]/a[1]').click()
        time.sleep(5)

        # Login as 4PL user
        login = driver.find_element_by_xpath('//*[@id="f7"]/div[2]/div/input')
        login.send_keys(self.LOGIN_4PL)
        password = driver.find_element_by_xpath(
            '//*[@id="f8"]/div[2]/div/input'
        )
        password.send_keys(self.PASSWORD_4PL)
        password.send_keys(Keys.RETURN)
        time.sleep(5)
        driver.find_element_by_id('p20').click()

        try:
            WebDriverWait(driver, 5).until(
                EC.title_is('4PL Task List (JP)')
            )
        except TimeoutException:
            driver.switch_to.window(driver.window_handles[-1])

        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()

        # Target search field and pass the SHIPMENT PO
        time.sleep(3)
        shipment_po_field = select_input_by_label(driver, 'PO# (1st Leg)', 'input[@type="text"]')
        shipment_po_field.send_keys(data_dict['shipment'])
        driver.find_element_by_xpath('//*[@id="t53"]/div[21]/a[1]').click()

        # Nineth task
        use_task_context_menu(driver, 'Confirm Application for Payment to Customs System (JP)', 5)
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element_by_xpath("//a[contains(text(),'Pay Later')]").click()
        # driver.find_element_by_xpath("//a[contains(text(),'OK & Complete')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 1. Sign out
        driver.close()
        logout_user(driver)

        # 2. Sign in as 3pl
        login_user(driver, self.LOGIN_3PL, self.PASSWORD_3PL)

        # 3. Go to 3pl task list
        driver.find_element_by_id('p14').click()

        try:
            WebDriverWait(driver, 5).until(
                EC.title_is('P&G 3PL Task List JP')
            )
        except TimeoutException:
            driver.switch_to.window(driver.window_handles[-1])

        driver.switch_to.window(driver.window_handles[-1])

        # 4. Go to search tab
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()

        # 5. Change select "Target Entity" to number 3 , wait to load
        select_cn = Select(select_input_by_label(driver, 'Target Entity', 'select'))
        select_cn.select_by_index(4)
        time.sleep(5)

        # 6. Put consignment number in the field "Equipment/Container #"
        container_field = select_input_by_label(driver, 'Equipment/Container #', 'input[@type="text"]')
        container_field.send_keys(data_dict['container'])

        # 7. Click search
        driver.find_element_by_xpath("//a[contains(text(),'Search')]").click()

        # 8. Update ETA in Destination Port (JP) - task (3rd context menu). Fields: "Latest ETA": "04 30 19 00:00"
        # Submit by "a": "Update milestone"
        use_task_context_menu(driver, 'Update ETA in Destination Port (JP)', 3)

        leta_field = select_input_by_label(driver, 'Latest ETA', 'input')
        leta_field.send_keys('04 30 19 00:00')
        time.sleep(2)
        driver.find_element_by_xpath("//a[contains(text(),'Update Milestone')]").click()

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 9. Task "Confirm ATA in Destination Port (JP)" (3rd context menu). Fields: "Arrival Date (Actual)" : "04 30 19 00:00"
        # Submit by "a":"Update milestone"
        time.sleep(2)
        use_task_context_menu(driver, 'Confirm ATA in Destination Port (JP)', 3)
        time.sleep(3)
        ada_field = select_input_by_label(driver, 'Arrival Date (Actual)', 'input')
        ada_field.send_keys('04 30 19 00:00')
        driver.find_element_by_xpath("//a[contains(text(),'Confirm Milestone')]").click()

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 10. Task "Provide Draft First Point Delivery Schedule BONDED (Import) (JP)" , 3rd context, 
        # field "First Point of Delivery":"type YAS and send Return". Submit "a":"Propose draft"
        use_task_context_menu(driver, 'Provide Draft First Point Delivery Schedule BONDED (Import) (JP)', 3)
        # time.sleep(15000)
        time.sleep(3)
        ada_field = select_input_by_label(driver, 'First Point of Delivery', 'input')
        ada_field.send_keys('YAS')
        time.sleep(2)
        ada_field.send_keys(Keys.ARROW_DOWN)
        ada_field.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.find_element_by_xpath("//a[contains(text(),'Propose Draft')]").click()

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # Logout
        driver.close()
        logout_user()

        # Login as WH
        login_user(driver, self.LOGIN_WH, self.PASSWORD_WH)
        # 1. Go to P&G WH TaskList JP
        qa_helper_functions.use_main_search_bar(driver, 'P&G WH TaskList JP')
        # 2. Go to search tab, select Target Entity -  Consignment
        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()
        select_cn = Select(select_input_by_label(driver, 'Target Entity', 'select'))
        select_cn.select_by_visible_text("Consignment")
        # 3. Pass the container number to Equipment/Container# Click "Search"
        container_field = select_input_by_label(driver, 'Equipment/Container #', 'input[@type="text"]')
        container_field.send_keys(data_dict['container'])
        driver.find_element_by_xpath("//a[contains(text(),'Search')]").click()
        # 4. Go to task "Confirm First Point of Delivery Schedule BONDED (Import) (JP)" right click and select Review & Confirm (3rd)
        # 5. Option "B" should be selected in Non-Bonded or Bonded (NB or B)
        # 6. Click "Review & Confirm", wait to process
        # 7. Logout and login as 3PL 
        # 8. Go to P&G 3PL Task List JP -> Search
        # 9. select Target Entity -  Consignment, Pass the container number to Equipment/Container# Click "Search"
        # 10. Go to task "Accept First Point of Delivery Schedule (Import) (JP)" , right click and select "Accept"(3rd)
        # 11. Click "Accept" and wait for task to process
        # 12. Go to task "Bonded Movement Declaration (JP)" (there we need to find a way to w8 for assigning), 
        # right click and select "Coplete"(3rd)
        # 13. Fill in fields: "Actual Timestamp - 04 30 19 00:00", "CDN #", "Currency", "Customs Duties", "Consumption Tax", "Incoterm", "Customs Duties for Pallets", "Consumption Tax for Pallets", "Bonded Movement Declaration Date - "April/30/2019"
        # 14. Select field "FTA Applied at Import?" - 'Yes', click "Complete" wait for task to process
        # 15. Go to task "Confirm Gate-Out Timestamp (JP)" , right click "Confirm Milestone" (3rd)
        # 16.Fill fields : "Actual Timestamp" - "04 30 19 00:00" , click "Confirm Milestone", wait for task to process
        # 17. Go to task "Confirm Container First Point Delivery (Import) (JP)" and click "Complete" (3rd)
        # 18 Fill in field "Actual Timestamp" - "04 30 19 00:00" click "Complete"
        # 19. Logout, and login as WH?
        time.sleep(150000)
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
    """Function selects input element, based on it's label"""
    func_string = 'find_element_by_xpath'
    return getattr(driver, func_string)(f'//div[@name="{label}"]//{input_type}')


def login_user(driver, login, password):
    login_field = driver.find_element_by_xpath('//*[@id="f7"]/div[2]/div/input')
    login_field.send_keys(login)
    password_field = driver.find_element_by_xpath(
        '//*[@id="f8"]/div[2]/div/input'
    )
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)


def logout_user(driver):
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element_by_xpath('//*[@id="page"]/div[2]/a[4]/div').click()
    driver.find_element_by_xpath('//*[@id="conf"]/div[3]/a[1]').click()
    time.sleep(5)


def fill_task_fields():
    """Fill fields based on dictionary with locators, types and values"""
    pass


def use_task_context_menu(driver, task_name, context_number):
    """Function locates task, left clicks, right clicks and go to slected context menu item"""
    actionChains = ActionChains(driver)
    driver.find_element_by_xpath(f"//div[contains(text(),'{task_name}')]").click()
    time.sleep(3)
    task = driver.find_element_by_xpath(f"//div[contains(text(),'{task_name}')]")
    actionChains.context_click(task).perform()
    time.sleep(3)
    driver.find_element_by_xpath(
        f'//*[@id="contextMenu"]/ul/a[{context_number}]/li'
    ).click()


def make_file_input_visible():
    """Function handles file input that is invisible"""
    pass


if __name__ == "__main__":
    unittest.main()

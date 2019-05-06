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
from excel_operations import rename_excel_template, generate_pnglo_JP_invoice, increment_json_invoice_no, generate_png_payment_files


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

    # @unittest.skip("Skipping...")
    def test_pg_process(self):

        rename_excel_template()
        data_dict = generate_pnglo_JP_invoice()
        driver = self.driver
        actionChains = ActionChains(driver)

        # Login as 4PL user
        qa_helper_functions.login_user(driver, self.LOGIN_4PL, self.PASSWORD_4PL)
        
        # Upload excel file
        qa_helper_functions.use_main_search_bar(driver, 'Excel File Upload')
        qa_helper_functions.submit_excel_file(driver, self.test_file, 'Submit')

        WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), '1 Files Imported Sucessfully')
        )
        
        # Success message element <div id="messageBar" style="display: none;" class="saved">1 Files Imported Sucessfully</div>
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])

        qa_helper_functions.use_main_search_bar(driver, '4PL Task List (JP)')
        
        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()

        # Target search field and pass the SHIPMENT PO
        shipment_po_field = qa_helper_functions.select_input_by_label(driver, 'PO# (1st Leg)', 'input[@type="text"]')
        shipment_po_field.send_keys(data_dict['shipment'])
        driver.find_element_by_xpath('//a[contains(text(), "Search")]').click()
        time.sleep(2)

        # 1st task
        # qa_helper_functions.use_task_context_menu(driver, 'Confirm Service PO / PO Conditions Exist/Correct (JP)', 'Assigned', 'Accept')
        # time.sleep(5)
        # comment_field = qa_helper_functions.select_input_by_label(driver, 'User Comments', 'textarea')
        # comment_field.send_keys('Test data comment')
        # driver.find_element_by_xpath("//a[contains(text(),'Accept')]").click()
        # time.sleep(5)

        # WebDriverWait(driver, 60).until(
        #     EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        # )
        tasks = qa_helper_functions.parse_json_data('JP_TEST.json')
        qa_helper_functions.exectue_simple_task(driver, tasks['task01'])
        # 2nd task completion
        driver.switch_to.window(driver.window_handles[-1])
        qa_helper_functions.use_task_context_menu(driver, 'Upload Commercial Invoice (Import) (JP)', 'Started', 'Complete')
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])

        # Commercial Invoice Number
        cin_field = qa_helper_functions.select_input_by_label(driver, 'Commercial Invoice Number', 'input')
        cin_field.send_keys("test data")
        # Goods Value
        gv_field = qa_helper_functions.select_input_by_label(driver, 'Goods Value', 'input')
        gv_field.send_keys('test data')
        # Incoterm used in CI
        iuic_field = qa_helper_functions.select_input_by_label(driver, 'Incoterm used in CI', 'input')
        iuic_field.send_keys('test data')
        # Currency
        cur_field = qa_helper_functions.select_input_by_label(driver, 'Currency', 'input')
        cur_field.send_keys('test data')

        driver.find_element_by_xpath("//a[contains(text(),'Proceed')]").click()

        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        fpath = os.path.join(os.getcwd(), self.test_file)

        qa_helper_functions.submit_excel_file(driver, fpath, 'Save')

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # Logout and login as 3PL user
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
        qa_helper_functions.logout_user(driver)

        # Login as 3PL user
        qa_helper_functions.login_user(driver, self.LOGIN_3PL, self.PASSWORD_3PL)

        qa_helper_functions.use_main_search_bar(driver, 'P&G 3PL Task List JP')

        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()
        time.sleep(3)
        shipment_po_field = qa_helper_functions.select_input_by_label(driver, 'PO# (1st Leg)', 'input[@type="text"]')
        shipment_po_field.send_keys(data_dict['shipment'])
        driver.find_element_by_xpath('//a[contains(text(), "Search")]').click()
        time.sleep(5)

        # Third
        qa_helper_functions.exectue_simple_task(driver, tasks['task03'])
        # qa_helper_functions.use_task_context_menu(driver, 'Confirm Pre-Alert Accurate & Complete (JP)', 'Assigned', 'Accept')
        # time.sleep(5)
        # driver.switch_to.window(driver.window_handles[-1])

        # select_ci = Select(qa_helper_functions.select_input_by_label(driver, 'Commercial Invoice (Y/N/NA)', 'select'))
        # select_ci.select_by_index(1)

        # select_bol = Select(qa_helper_functions.select_input_by_label(driver, 'Bill of Lading (Y/N/NA)', 'select'))
        # select_bol.select_by_index(1)

        # select_plts = Select(qa_helper_functions.select_input_by_label(driver, 'PL/Tally Sheet (Y/N/NA)', 'select'))
        # select_plts.select_by_index(1)

        # select_coa = Select(qa_helper_functions.select_input_by_label(driver, 'COA (Y/N/NA)', 'select'))
        # select_coa.select_by_index(1)

        # date_field = qa_helper_functions.select_input_by_label(driver, 'Pre-Alert Received Date', 'input')
        # date_field.send_keys('04 30 19 00:00')

        # driver.find_element_by_xpath("//a[contains(text(),'Accept')]").click()
        # WebDriverWait(driver, 60).until(
        #     EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        # )
        # Fourth task
        qa_helper_functions.use_task_context_menu(driver, 'Confirm FTA Documents Received & Accurate (JP)', 'Assigned', 'Accept')
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])

        select_field = Select(qa_helper_functions.select_input_by_label(driver, 'FTA Document Name', 'select'))
        select_field.select_by_index(1)
        date_field = qa_helper_functions.select_input_by_label(driver, 'FTA Received Date', 'input')
        date_field.send_keys('April/30/2019')
        driver.find_element_by_xpath("//a[contains(text(),'Accept')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # Fifth task
        qa_helper_functions.use_task_context_menu(driver, 'Confirm Additional Import Customs Requirements (JP)', 'Assigned', 'Accept')
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])

        select_cn = Select(qa_helper_functions.select_input_by_label(driver, 'Cosmetic Notification (Y/N/NA)', 'select'))
        select_cn.select_by_index(1)

        select_cscl = Select(qa_helper_functions.select_input_by_label(driver, 'Chem Sub Control Law (Y/N/NA)', 'select'))
        select_cscl.select_by_index(1)

        select_jprpa = Select(qa_helper_functions.select_input_by_label(driver, 'JPR Pallet Agreement (Y/N/NA)', 'select'))
        select_jprpa.select_by_index(1)

        select_gic = Select(qa_helper_functions.select_input_by_label(driver, 'Gas Inspect Cert (Y/N/NA)', 'select'))
        select_gic.select_by_index(1)

        select_qdal = Select(qa_helper_functions.select_input_by_label(driver, 'Quasi Drug App Lic (Y/N/NA)', 'select'))
        select_qdal.select_by_index(1)

        select_ac = Select(qa_helper_functions.select_input_by_label(driver, 'ASSIST Cost (Y/N/NA)', 'select'))
        select_ac.select_by_index(1)

        select_flt = Select(qa_helper_functions.select_input_by_label(driver, 'Fire Length Test (Y/N/NA)', 'select'))
        select_flt.select_by_index(1)

        driver.find_element_by_xpath("//a[contains(text(),'Accept')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # Sixth task
        qa_helper_functions.use_task_context_menu(driver, 'Confirm Import HS Code (JP)', 'Assigned', 'OK & Complete')
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])

        driver.find_element_by_xpath("//a[contains(text(),'OK & Complete')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # Seventh task
        qa_helper_functions.use_task_context_menu(driver, 'Confirm All Import Documents Accurate and Complete (JP)', 'Started', 'Complete')
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])

        driver.find_element_by_xpath("//a[contains(text(),'Proceed')]").click()
        qa_helper_functions.submit_excel_file(driver, fpath, 'Save')

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
        qa_helper_functions.logout_user(driver)

        # Login as 4PL user
        qa_helper_functions.login_user(driver, self.LOGIN_4PL, self.PASSWORD_4PL)

        qa_helper_functions.use_main_search_bar(driver, '4PL Task List (JP)')

        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()

        # Target search field and pass the SHIPMENT PO
        time.sleep(3)
        shipment_po_field = qa_helper_functions.select_input_by_label(driver, 'PO# (1st Leg)', 'input[@type="text"]')
        shipment_po_field.send_keys(data_dict['shipment'])

        driver.find_element_by_xpath('//a[contains(text(), "Search")]').click()

        # Eighth task
        qa_helper_functions.use_task_context_menu(driver, 'Confirm Application for Payment to Customs System (JP)', 'Assigned', 'Pay Later')
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element_by_xpath("//a[contains(text(),'Pay Later')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 1. Sign out
        driver.close()
        qa_helper_functions.logout_user(driver)

        # 2. Sign in as 3pl
        qa_helper_functions.login_user(driver, self.LOGIN_3PL, self.PASSWORD_3PL)

        # 3. Go to 3pl task list
        qa_helper_functions.use_main_search_bar(driver, 'P&G 3PL Task List JP')

        # 4. Go to search tab
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()

        # 5. Change select "Target Entity" to number 3 , wait to load
        select_cn = Select(qa_helper_functions.select_input_by_label(driver, 'Target Entity', 'select'))
        select_cn.select_by_visible_text('Consignment')
        time.sleep(4)

        # 6. Put consignment number in the field "Equipment/Container #"
        container_field = qa_helper_functions.select_input_by_label(driver, 'Equipment/Container #', 'input[@type="text"]')
        container_field.send_keys(data_dict['container'])

        # 7. Click search
        driver.find_element_by_xpath("//a[contains(text(),'Search')]").click()

        # 8. Update ETA in Destination Port (JP) - task (3rd context menu). Fields: "Latest ETA": "04 30 19 00:00"
        # Submit by "a": "Update milestone"
        qa_helper_functions.use_task_context_menu(driver, 'Update ETA in Destination Port (JP)', 'Started', 'Update Milestone')

        leta_field = qa_helper_functions.select_input_by_label(driver, 'Latest ETA', 'input')
        leta_field.send_keys('04 30 19 00:00')
        time.sleep(2)
        driver.find_element_by_xpath("//a[contains(text(),'Update Milestone')]").click()

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 9. Task "Confirm ATA in Destination Port (JP)" (3rd context menu). Fields: "Arrival Date (Actual)" : "04 30 19 00:00"
        # Submit by "a":"Update milestone"
        time.sleep(2)
        qa_helper_functions.use_task_context_menu(driver, 'Confirm ATA in Destination Port (JP)', 'Started', 'Confirm Milestone')
        time.sleep(3)
        ada_field = qa_helper_functions.select_input_by_label(driver, 'Arrival Date (Actual)', 'input')
        ada_field.send_keys('04 30 19 00:00')
        driver.find_element_by_xpath("//a[contains(text(),'Confirm Milestone')]").click()

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 10. Task "Provide Draft First Point Delivery Schedule BONDED (Import) (JP)" , 3rd context, 
        # field "First Point of Delivery":"type YAS and send Return". Submit "a":"Propose draft"
        qa_helper_functions.use_task_context_menu(driver, 'Provide Draft First Point Delivery Schedule BONDED (Import) (JP)', 'Started', 'Propose Draft')
        time.sleep(3)
        fpod_field = qa_helper_functions.select_input_by_label(driver, 'First Point of Delivery', 'input')
        fpod_field.send_keys('YAS')
        time.sleep(3)
        fpod_field.send_keys(Keys.ARROW_DOWN)
        fpod_field.send_keys(Keys.RETURN)
        time.sleep(4)
        driver.find_element_by_xpath("//a[contains(text(),'Propose Draft')]").click()

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # Logout
        driver.close()
        time.sleep(2)
        qa_helper_functions.logout_user(driver)

        # Login as WH
        qa_helper_functions.login_user(driver, self.LOGIN_WH, self.PASSWORD_WH)

        # 1. Go to P&G WH TaskList JP
        qa_helper_functions.use_main_search_bar(driver, 'P&G WH TaskList JP')

        # 2. Go to search tab, select Target Entity -  Consignment
        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()
        select_cn = Select(qa_helper_functions.select_input_by_label(driver, 'Target Entity', 'select'))
        select_cn.select_by_visible_text('Consignment')
        time.sleep(4)

        # 3. Pass the container number to Equipment/Container# Click "Search"
        container_field = qa_helper_functions.select_input_by_label(driver, 'Equipment/Container#', 'input[@type="text"]')
        container_field.send_keys(data_dict['container'])
        driver.find_element_by_xpath("//a[contains(text(),'Search')]").click()

        # 4. Go to task "Confirm First Point of Delivery Schedule BONDED (Import) (JP)"(Assigned) right click and select Review & Confirm (3rd)
        qa_helper_functions.use_task_context_menu(driver, 'Confirm First Point of Delivery Schedule BONDED (Import) (JP)', 'Assigned', 'Review & Confirm')
        time.sleep(3)

        # 5. Option "B" should be selected in Non-Bonded or Bonded (NB or B)
        select_bond = Select(qa_helper_functions.select_input_by_label(driver, 'Non-Bonded or Bonded (NB or B)', 'select'))
        select_bond.select_by_visible_text("B")

        # 6. Click "Review & Confirm", wait to process
        driver.find_element_by_xpath("//a[contains(text(),'Review & Confirm')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 7. Logout and login as 3PL
        driver.close()
        time.sleep(2)
        qa_helper_functions.logout_user(driver)
        qa_helper_functions.login_user(driver, self.LOGIN_3PL, self.PASSWORD_3PL)

        # 8. Go to P&G 3PL Task List JP -> Search
        qa_helper_functions.use_main_search_bar(driver,'P&G 3PL Task List JP')
        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()

        # 9. select Target Entity -  Consignment, Pass the container number to Equipment/Container# Click "Search"
        select_cn = Select(qa_helper_functions.select_input_by_label(driver, 'Target Entity', 'select'))
        select_cn.select_by_visible_text("Consignment")
        time.sleep(4)
        container_field = qa_helper_functions.select_input_by_label(driver, 'Equipment/Container #', 'input[@type="text"]')
        container_field.send_keys(data_dict['container'])
        driver.find_element_by_xpath("//a[contains(text(),'Search')]").click()
        time.sleep(2)

        # 10. Go to task "Accept First Point of Delivery Schedule (Import) (JP)"(Assigned) , right click and select "Accept"(3rd)
        qa_helper_functions.use_task_context_menu(driver, 'Accept First Point of Delivery Schedule (Import) (JP)', 'Assigned', 'Accept')
        time.sleep(3)

        # 11. Click "Accept" and wait for task to process
        driver.find_element_by_xpath("//a[contains(text(),'Accept')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 12. Go to task "Bonded Movement Declaration (JP)" (Started), 
        # right click and select "Complete"(3rd)
        qa_helper_functions.use_task_context_menu(driver, 'Bonded Movement Declaration (JP)', 'Started', 'Complete')
        time.sleep(3)

        # 13. Fill in fields: "Actual Timestamp - 04 30 19 00:00", "CDN #", "Currency", "Customs Duties", "Consumption Tax", "Incoterm", "Customs Duties for Pallets", "Consumption Tax for Pallets", "Bonded Movement Declaration Date - "April/30/2019"
        at_field = qa_helper_functions.select_input_by_label(driver, 'Actual Timestamp', 'input')
        at_field.send_keys('04 30 19 00:00')

        cdn_field = qa_helper_functions.select_input_by_label(driver, 'CDN #', 'input')
        cdn_field.send_keys('Test data')

        cur_field = qa_helper_functions.select_input_by_label(driver, 'Currency', 'input')
        cur_field.send_keys('Test data0')

        cd_field = qa_helper_functions.select_input_by_label(driver, 'Customs Duties', 'input')
        cd_field.send_keys('Test data')

        ct_field = qa_helper_functions.select_input_by_label(driver, 'Consumption Tax', 'input')
        ct_field.send_keys('Test data')

        inco_field = qa_helper_functions.select_input_by_label(driver, 'Incoterm', 'input')
        inco_field.send_keys('Test data')

        cdfp_field = qa_helper_functions.select_input_by_label(driver, 'Customs Duties for Pallets', 'input')
        cdfp_field.send_keys('Test data')

        ctfp_field = qa_helper_functions.select_input_by_label(driver, 'Consumption Tax for Pallets', 'input')
        ctfp_field.send_keys('Test data')

        bmdd_field = qa_helper_functions.select_input_by_label(driver, 'Bonded Movement Declaration Date', 'input')
        bmdd_field.send_keys('April/30/2019')
        
        # 14. Select field "FTA Applied at Import?" - 'Yes', click "Complete" wait for task to process
        select_ftaaai = Select(qa_helper_functions.select_input_by_label(driver, 'FTA Applied at Import?', 'select'))
        select_ftaaai.select_by_visible_text("Yes")
        time.sleep(2)
        driver.find_element_by_xpath("//a[contains(text(),'Complete')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 15. Go to task "Confirm Gate-Out Timestamp (JP)"(Started) , right click "Confirm Milestone" (3rd)
        qa_helper_functions.use_task_context_menu(driver, 'Confirm Gate-Out Timestamp (JP)', 'Started', 'Confirm Milestone')
        time.sleep(3)
        
        # 16.Fill fields : "Actual Timestamp" - "04 30 19 00:00" , click "Confirm Milestone", wait for task to process
        at_field = qa_helper_functions.select_input_by_label(driver, 'Actual Timestamp', 'input')
        at_field.send_keys('04 30 19 00:00')
        driver.find_element_by_xpath("//a[contains(text(),'Confirm Milestone')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 17. Go to task "Confirm Container First Point Delivery (Import) (JP)"(Started) and click "Complete" (3rd)
        qa_helper_functions.use_task_context_menu(driver, 'Confirm Container First Point Delivery (Import) (JP)', 'Started', 'Complete')
        time.sleep(3)
        
        # 18 Fill in field "Actual Timestamp" - "04 30 19 00:00" click "Complete"
        at_field = qa_helper_functions.select_input_by_label(driver, 'Actual Timestamp', 'input')
        at_field.send_keys('04 30 19 00:00')
        driver.find_element_by_xpath("//a[contains(text(),'Complete')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 19. Logout, and login as WH
        time.sleep(2)
        driver.close()
        qa_helper_functions.logout_user(driver)
        qa_helper_functions.login_user(driver, self.LOGIN_WH, self.PASSWORD_WH)

        # 20. Go to "P&G WH TaskList JP", select Target Entity - Consignment
        qa_helper_functions.use_main_search_bar(driver, 'P&G WH TaskList JP')
        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()
        select_cn = Select(qa_helper_functions.select_input_by_label(driver, 'Target Entity', 'select'))
        select_cn.select_by_visible_text('Consignment')
        time.sleep(2)

        # 21. Pass container number, click Search
        container_field = qa_helper_functions.select_input_by_label(driver, 'Equipment/Container#', 'input[@type="text"]')
        container_field.send_keys(data_dict['container'])
        driver.find_element_by_xpath("//a[contains(text(),'Search')]").click()
        
        # 22. Go to task "Confirm Empty Container Availability (JP)" (Started), and click "Complete"
        qa_helper_functions.use_task_context_menu(driver, 'Confirm Empty Container Availability (JP)', 'Started', 'Complete')
        time.sleep(3)
        driver.find_element_by_xpath("//a[contains(text(),'Complete')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 23. Logout and login as 3PL
        time.sleep(2)
        driver.close()
        qa_helper_functions.logout_user(driver)
        qa_helper_functions.login_user(driver, self.LOGIN_3PL, self.PASSWORD_3PL)

        # 24. Go to P&G 3PL Task List JP -> Search
        qa_helper_functions.use_main_search_bar(driver, 'P&G 3PL Task List JP')
        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()

        # 25. Select, consignment, pass container id
        select_cn = Select(qa_helper_functions.select_input_by_label(driver, 'Target Entity', 'select'))
        select_cn.select_by_visible_text('Consignment')
        time.sleep(2)
        container_field = qa_helper_functions.select_input_by_label(driver, 'Equipment/Container #', 'input[@type="text"]')
        container_field.send_keys(data_dict['container'])
        driver.find_element_by_xpath("//a[contains(text(),'Search')]").click()

        # 26. Go to task "Confirm Container Departs from Unloading Site (JP)"(Started) and click Complete
        qa_helper_functions.use_task_context_menu(driver, 'Confirm Container Departs from Unloading Site (JP)', 'Started', 'Complete')
        time.sleep(3)
        
        # 27. Pass data to field "Actual Timestamp" - 05 01 19 00:00 and click "Complete"
        at_field = qa_helper_functions.select_input_by_label(driver, 'Actual Timestamp', 'input')
        at_field.send_keys('05 01 19 00:00')
        driver.find_element_by_xpath("//a[contains(text(),'Complete')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # 28. Go to task "Confirm Empty Container Returned (JP)" (Started), and click "Confirm Milestone"
        qa_helper_functions.use_task_context_menu(driver, 'Confirm Empty Container Returned (JP)', 'Started', 'Confirm Milestone')
        time.sleep(3)
        
        # 29. Fill field "Actual Timestamp" - 05 01 19 00:00 click "Confirm Milestone"
        at_field = qa_helper_functions.select_input_by_label(driver, 'Actual Timestamp', 'input')
        at_field.send_keys('05 01 19 00:00')
        driver.find_element_by_xpath("//a[contains(text(),'Confirm Milestone')]").click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )
        driver.quit()

    @unittest.skip("Skipping...")
    def test_png_payment_spo(self):
        """P&G Payment JP Test. PO Conditions flow."""
        PAYMENT4PL_USER = access_file.user_4pl_payment
        PAYMENT4PL_PASS = access_file.pass_4pl_payment
        PAYMENT3PL_USER = access_file.user_3pl_payment
        PAYMENT3PL_PASS = access_file.pass_3pl_payment
        increment_json_invoice_no()
        test_data = qa_helper_functions.parse_json_data('PNG_PAYMENT_JP.json')
        invoice_no = test_data['invoice_no']
        generate_png_payment_files(invoice_no, 'PO Conditions')
        driver = self.driver
        actionChains = ActionChains(driver)
        # test_file = os.path.join(
        #     os.getcwd(), "PNGLO001R_JP_INVOICE_SO_Template_20190501122733300.xlsx"
        # )
        upload_file = os.path.join(
            os.getcwd(),
            'excel_files',
            'png_payment_spo',
            'PNGLO001R_JP_INVOICE_SO_Template_20190501122733300.xlsx'
        )
        # Login to the system
        qa_helper_functions.login_user(driver, PAYMENT4PL_USER, PAYMENT4PL_PASS)
        # Upload generated xlsx file
        qa_helper_functions.use_main_search_bar(driver, 'Excel Sheet Upload')

        qa_helper_functions.submit_excel_file(driver, upload_file, 'Submit')
        WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), '1 Files Imported Sucessfully')
        )
        qa_helper_functions.close_current_tab(driver)

        # Go to "todo list" and do all tasks available as current user
        qa_helper_functions.use_main_search_bar(driver, 'P&G Payment Tracker To Do List JP')
        driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()

        invoice_no_field = qa_helper_functions.select_input_by_label(driver, 'Link ID / Invoice Number', 'input[@type="text"]')
        # invoice_no_field.send_keys('ABME26041920')
        invoice_no_field.send_keys(invoice_no)
        time.sleep(2)
        driver.find_element_by_xpath('//a[contains(text(), "Search")]').click()

        # Task 1 Invoice Verification Complete (JP)
        qa_helper_functions.use_task_context_menu(driver, 'Invoice Verification Complete (JP)', 'Assigned', 'Accept - Invoice Correct')
        time.sleep(5)

        select_ci = Select(qa_helper_functions.select_input_by_label(driver, 'Payment Method', 'select'))
        select_ci.select_by_visible_text('PO Conditions')

        uvcd_field = qa_helper_functions.select_input_by_label(driver, 'Update Verification Complete Date', 'input')
        uvcd_field.send_keys('01 May 2019')
        driver.find_element_by_xpath("//a[contains(text(),'Accept - Invoice Correct')]").click()
        time.sleep(5)

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # Task 2 Invoice Dispatched to P2P (JP)
        qa_helper_functions.use_task_context_menu(driver, 'Invoice Dispatched to P2P (JP)', 'Started', 'Complete')
        time.sleep(5)

        dtpd_field = qa_helper_functions.select_input_by_label(driver, 'Dispatched to P2P Date', 'input')
        dtpd_field.send_keys('01 May 2019')
        
        driver.find_element_by_xpath("//a[contains(text(),'Complete')]").click()
        time.sleep(5)

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )

        # Task 3 Confirm Invoice Payment Made (JP)
        qa_helper_functions.use_task_context_menu(driver, 'Confirm Invoice Payment Made (JP)', 'Started', 'Complete')
        time.sleep(5)

        pd_field = qa_helper_functions.select_input_by_label(driver, 'Payment Date', 'input')
        pd_field.send_keys('01 May 2019')
        
        driver.find_element_by_xpath("//a[contains(text(),'Complete')]").click()
        time.sleep(5)

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )
        
        # # Logout and login as user which has tasks to execute (repeat untill flow is done)
        # driver.close()
        # qa_helper_functions.logout_user(driver)
        # qa_helper_functions.login_user(driver, PAYMENT3PL_USER, PAYMENT3PL_PASS)

        # # Go to "todo list" and do all tasks available as current user
        # qa_helper_functions.use_main_search_bar(driver, 'P&G 3PL Task List JP')
        # time.sleep(4)
        # driver.find_element_by_xpath('//*[@id="tabs"]//a[contains(text(), "Search")]').click()

        # invoice_no_field = qa_helper_functions.select_input_by_label(driver, 'Link-ID', 'input[@type="text"]')
        # # invoice_no_field.send_keys('ABME26041920')
        # invoice_no_field.send_keys(invoice_no)
        # driver.find_element_by_xpath('//a[contains(text(), "Search")]').click()

        # Task 4
        qa_helper_functions.use_task_context_menu(driver, 'Confirm Invoice Payment Received (JP)', 'Started', 'Complete')
        time.sleep(5)

        pd_field = qa_helper_functions.select_input_by_label(driver, 'Update Vendor Payment Confirmed Date', 'input')
        pd_field.send_keys('01 May 2019')
        
        driver.find_element_by_xpath("//a[contains(text(),'Complete')]").click()
        time.sleep(5)

        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
        )
        driver.quit()


if __name__ == "__main__":
    unittest.main()

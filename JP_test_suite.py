# Standard library import
import os
import time
import unittest

# Third party import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# Local import
import orch_automation_tools
from excel_operations import generate_excel_from_json


class CITPNGJPImportTests(unittest.TestCase):
    """Test suite for CIT PNG JP IMPORT"""
    BASE_URL = 'https://ct-cit.damco.com/'
    CONTROL_JSON = os.path.join(
            os.getcwd(),
            'json_flow_data',
            'CIT_BASE.json'
    )
    EXCEL_PATH = os.path.join(
            os.getcwd(),
            'excel_files',
            'png',
            'jp',
            'import'
    )
    JSON_PATH = os.path.join(
            os.getcwd(),
            'json_flow_data',
            'png',
            'jp',
            'import'
    )
    USER_CREDENTIALS = orch_automation_tools.parse_json_data(
        os.path.join(
            os.getcwd(),
            'json_flow_data',
            'CIT_ACCESS.json'
        )
    )['png']['jp']['import']
    excel_template = None
    def setUp(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(20)
        orch_automation_tools.open_main_page(self.driver, self.BASE_URL)
        # self.driver.get(self.BASE_URL)
        self.driver.maximize_window()
        self.test_file = os.path.join(
            os.getcwd(),
            'excel_files',
            "TEST_FILE.xlsx"
        )

    @unittest.skip("Skipping...")
    def test_png_i_b_nd_pl_fcl(self):
        """
        P&G Import Non Bonded Non Direct Customer - Pay Now(FCL)
        """
        USER_4PL = self.USER_CREDENTIALS['4pl']
        USER_3PL = self.USER_CREDENTIALS['3pl']
        USER_WH = self.USER_CREDENTIALS['wh']

        json_file = os.path.join(self.JSON_PATH, 'png_nondirect_bonded_fcl_paylater.json')
        excel_data = generate_excel_from_json(
            json_file, self.CONTROL_JSON, self.EXCEL_PATH
        )
        json_data = orch_automation_tools.parse_json_data(json_file)
        self.excel_template = os.path.join(
            self.EXCEL_PATH, json_data['template_name']
        )
        shipment_order = excel_data['shipment_order']
        container_number = excel_data['container_number']
        tasks = json_data['tasks']
        driver = self.driver

        orch_automation_tools.login_user(driver, USER_4PL)

        orch_automation_tools.use_main_search_bar(driver, 'Excel File Upload')
        orch_automation_tools.submit_excel_file(driver, self.excel_template, 'Submit')
        
        WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="messageBar"]'),
                '1 Files Imported Sucessfully'
            )
        )

        orch_automation_tools.close_current_tab(driver)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task01'])

        # 2nd task completion
        fpath = os.path.join(os.getcwd(), self.test_file)
        orch_automation_tools.exectue_task_with_upload(
            driver, tasks['task02'], fpath
        )

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task03'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task04'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task05'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task06'])

        orch_automation_tools.exectue_task_with_upload(
            driver, tasks['task07'], fpath
        )

        orch_automation_tools.change_user(driver, USER_4PL)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task08'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task09'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task10'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task11'])

        orch_automation_tools.change_user(driver, USER_WH)

        orch_automation_tools.find_tasks(
            driver, 'P&G WH TaskList JP', container_number,
            'Equipment/Container#', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task12'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task13'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task14'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task15'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task16'])

        orch_automation_tools.change_user(driver, USER_WH)

        orch_automation_tools.find_tasks(
            driver, 'P&G WH TaskList JP', container_number,
            'Equipment/Container#', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task17'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task18'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task19'])

    @unittest.skip("Skipping...")
    def test_png_i_b_nd_pl_lcl(self):
        """
        P&G Import Non Bonded Non Direct Customer - Pay Now(FCL)
        """
        USER_4PL = self.USER_CREDENTIALS['4pl']
        USER_3PL = self.USER_CREDENTIALS['3pl']
        USER_WH = self.USER_CREDENTIALS['wh']

        json_file = os.path.join(self.JSON_PATH, 'png_nondirect_bonded_lcl_paylater.json')
        excel_data = generate_excel_from_json(
            json_file, self.CONTROL_JSON, self.EXCEL_PATH
        )
        json_data = orch_automation_tools.parse_json_data(json_file)
        self.excel_template = os.path.join(
            self.EXCEL_PATH, json_data['template_name']
        )
        shipment_order = excel_data['shipment_order']
        container_number = excel_data['container_number']
        tasks = json_data['tasks']
        driver = self.driver

        orch_automation_tools.login_user(driver, USER_4PL)

        orch_automation_tools.use_main_search_bar(driver, 'Excel File Upload')
        orch_automation_tools.submit_excel_file(driver, self.excel_template, 'Submit')
        
        WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="messageBar"]'),
                '1 Files Imported Sucessfully'
            )
        )

        orch_automation_tools.close_current_tab(driver)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task01'])

        # 2nd task completion
        fpath = os.path.join(os.getcwd(), self.test_file)
        orch_automation_tools.exectue_task_with_upload(
            driver, tasks['task02'], fpath
        )

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task03'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task04'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task05'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task06'])

        orch_automation_tools.exectue_task_with_upload(
            driver, tasks['task07'], fpath
        )

        orch_automation_tools.change_user(driver, USER_4PL)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task08'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task09'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task10'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task11'])

        orch_automation_tools.change_user(driver, USER_WH)

        orch_automation_tools.find_tasks(
            driver, 'P&G WH TaskList JP', container_number,
            'Equipment/Container#', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task12'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task13'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task14'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task15'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task16'])

    @unittest.skip("Skipping...")
    def test_png_i_nb_nd_pn_fcl(self):
        """
        P&G Import Bonded Non Direct Customer - Pay Later(FCL)
        """
        USER_4PL = self.USER_CREDENTIALS['4pl']
        USER_3PL = self.USER_CREDENTIALS['3pl-febre']
        USER_WH = self.USER_CREDENTIALS['wh']
        json_file = os.path.join(self.JSON_PATH, 'png_nondirect_nonbonded_fcl_paynow.json')
        excel_data = generate_excel_from_json(
            json_file, self.CONTROL_JSON, self.EXCEL_PATH
        )
        json_data = orch_automation_tools.parse_json_data(json_file)
        self.excel_template = os.path.join(
            self.EXCEL_PATH, json_data['template_name']
        )
        shipment_order = excel_data['shipment_order']
        container_number = excel_data['container_number']
        tasks = json_data['tasks']
        driver = self.driver

        orch_automation_tools.login_user(driver, USER_4PL)

        orch_automation_tools.use_main_search_bar(driver, 'Excel File Upload')
        orch_automation_tools.submit_excel_file(driver, self.excel_template, 'Submit')

        WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="messageBar"]'),
                '1 Files Imported Sucessfully'
            )
        )

        orch_automation_tools.close_current_tab(driver)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task01'])

        fpath = os.path.join(os.getcwd(), self.test_file)
        orch_automation_tools.exectue_task_with_upload(
            driver, tasks['task02'], fpath
        )
        orch_automation_tools.change_user(driver, USER_3PL)
        
        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', shipment_order, 'Link-ID'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task03'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task04'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task05'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task06'])

        orch_automation_tools.exectue_task_with_upload(
            driver, tasks['task07'], fpath
        )
        orch_automation_tools.change_user(driver, USER_4PL)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task08'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', shipment_order, 'Link-ID'
        )
        orch_automation_tools.exectue_simple_task(driver, tasks['task09'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task10'])

        orch_automation_tools.close_current_tab(driver)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )
        orch_automation_tools.exectue_simple_task(driver, tasks['task11'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task12'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task13'])

        orch_automation_tools.change_user(driver, USER_WH)

        orch_automation_tools.find_tasks(
            driver, 'P&G WH TaskList JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task14'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task15'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task16'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task17'])

        orch_automation_tools.change_user(driver, USER_WH)

        orch_automation_tools.find_tasks(
            driver, 'P&G WH TaskList JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task18'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task19'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task20'])

    @unittest.skip("Skipping...")
    def test_png_i_nb_nd_pn_lcl(self):
        """
        P&G Import Non Bonded Non Direct Customer - Pay Now(LCL)
        """
        USER_4PL = self.USER_CREDENTIALS['4pl']
        USER_3PL = self.USER_CREDENTIALS['3pl-febre']
        USER_WH = self.USER_CREDENTIALS['wh']

        json_file = os.path.join(
            self.JSON_PATH, 'png_nondirect_nonbonded_lcl_paynow.json'
        )
        excel_data = generate_excel_from_json(
            json_file, self.CONTROL_JSON, self.EXCEL_PATH
        )
        json_data = orch_automation_tools.parse_json_data(json_file)
        self.excel_template = os.path.join(
            self.EXCEL_PATH, json_data['template_name']
        )
        shipment_order = excel_data['shipment_order']
        container_number = excel_data['container_number']
        tasks = json_data['tasks']

        driver = self.driver

        orch_automation_tools.login_user(driver, USER_4PL)

        orch_automation_tools.use_main_search_bar(driver, 'Excel File Upload')
        orch_automation_tools.submit_excel_file(driver, self.excel_template, 'Submit')

        WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="messageBar"]'),
                '1 Files Imported Sucessfully'
            )
        )

        orch_automation_tools.close_current_tab(driver)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task01'])

        fpath = os.path.join(os.getcwd(), self.test_file)
        orch_automation_tools.exectue_task_with_upload(
            driver, tasks['task02'], fpath
        )
        orch_automation_tools.change_user(driver, USER_3PL)
        
        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', shipment_order, 'Link-ID'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task03'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task04'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task05'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task06'])

        orch_automation_tools.exectue_task_with_upload(
            driver, tasks['task07'], fpath
        )
        orch_automation_tools.change_user(driver, USER_4PL)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task08'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', shipment_order, 'Link-ID'
        )
        orch_automation_tools.exectue_simple_task(driver, tasks['task09'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task10'])

        orch_automation_tools.close_current_tab(driver)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )
        orch_automation_tools.exectue_simple_task(driver, tasks['task11'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task12'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task13'])

        orch_automation_tools.change_user(driver, USER_WH)

        orch_automation_tools.find_tasks(
            driver, 'P&G WH TaskList JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task14'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task15'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task16'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task17'])

    @unittest.skip("Skipping...")
    def test_png_i_nb_nd_pl_fcl(self):
        """
        P&G Import Non Bonded Non Direct Customer - Pay Later(FCL)
        """
        USER_4PL = self.USER_CREDENTIALS['4pl']
        USER_3PL = self.USER_CREDENTIALS['3pl-febre']
        USER_WH = self.USER_CREDENTIALS['wh-akashi']

        json_file = os.path.join(
            self.JSON_PATH, 'png_nondirect_nonbonded_fcl_paylater.json'
        )
        excel_data = generate_excel_from_json(
            json_file, self.CONTROL_JSON, self.EXCEL_PATH
        )
        json_data = orch_automation_tools.parse_json_data(json_file)
        self.excel_template = os.path.join(
            self.EXCEL_PATH, json_data['template_name']
        )
        shipment_order = excel_data['shipment_order']
        container_number = excel_data['container_number']
        tasks = json_data['tasks']
        driver = self.driver

        orch_automation_tools.login_user(driver, USER_4PL)

        orch_automation_tools.use_main_search_bar(driver, 'Excel File Upload')
        orch_automation_tools.submit_excel_file(driver, self.excel_template, 'Submit')

        WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="messageBar"]'),
                '1 Files Imported Sucessfully'
            )
        )

        orch_automation_tools.close_current_tab(driver)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task01'])

        fpath = os.path.join(os.getcwd(), self.test_file)
        orch_automation_tools.exectue_task_with_upload(
            driver, tasks['task02'], fpath
        )

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', shipment_order, 'Link-ID'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task03'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task04'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task05'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task06'])

        orch_automation_tools.exectue_task_with_upload(
            driver, tasks['task07'], fpath
        )

        orch_automation_tools.change_user(driver, USER_4PL)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task08'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', shipment_order, 'Link-ID'
        )
        orch_automation_tools.exectue_simple_task(driver, tasks['task09'])

        orch_automation_tools.change_user(driver, USER_4PL)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )
        orch_automation_tools.exectue_simple_task(driver, tasks['task10'])

        orch_automation_tools.change_user(driver, USER_3PL)
        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )
        orch_automation_tools.exectue_simple_task(driver, tasks['task11'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task12'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task13'])

        orch_automation_tools.change_user(driver, USER_WH)

        orch_automation_tools.find_tasks(
            driver, 'P&G WH TaskList JP', container_number,
            'Equipment/Container#', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task14'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task15'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task16'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task17'])

        orch_automation_tools.change_user(driver, USER_WH)

        orch_automation_tools.find_tasks(
            driver, 'P&G WH TaskList JP', container_number,
            'Equipment/Container#', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task18'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task19'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task20'])

    @unittest.skip("Skipping...")
    def test_png_i_nb_nd_pl_lcl(self):
        """
        P&G Import Non Bonded Non Direct Customer - Pay Later(LCL)
        """
        USER_4PL = self.USER_CREDENTIALS['4pl']
        USER_3PL = self.USER_CREDENTIALS['3pl-febre']
        USER_WH = self.USER_CREDENTIALS['wh-akashi']

        json_file = os.path.join(
            self.JSON_PATH, 'png_nondirect_nonbonded_lcl_paylater.json'
        )
        excel_data = generate_excel_from_json(
            json_file, self.CONTROL_JSON, self.EXCEL_PATH
        )
        json_data = orch_automation_tools.parse_json_data(json_file)
        self.excel_template = os.path.join(
            self.EXCEL_PATH, json_data['template_name']
        )
        shipment_order = excel_data['shipment_order']
        container_number = excel_data['container_number']
        tasks = json_data['tasks']
        driver = self.driver

        orch_automation_tools.login_user(driver, USER_4PL)

        orch_automation_tools.use_main_search_bar(driver, 'Excel File Upload')
        orch_automation_tools.submit_excel_file(driver, self.excel_template, 'Submit')

        WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="messageBar"]'),
                '1 Files Imported Sucessfully'
            )
        )

        orch_automation_tools.close_current_tab(driver)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task01'])

        fpath = os.path.join(os.getcwd(), self.test_file)
        orch_automation_tools.exectue_task_with_upload(
            driver, tasks['task02'], fpath
        )

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', shipment_order, 'Link-ID'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task03'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task04'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task05'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task06'])

        orch_automation_tools.exectue_task_with_upload(
            driver, tasks['task07'], fpath
        )

        orch_automation_tools.change_user(driver, USER_4PL)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task08'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', shipment_order, 'Link-ID'
        )
        orch_automation_tools.exectue_simple_task(driver, tasks['task09'])

        orch_automation_tools.change_user(driver, USER_4PL)

        orch_automation_tools.find_tasks(
            driver, '4PL Task List (JP)', shipment_order, 'PO# (1st Leg)'
        )
        orch_automation_tools.exectue_simple_task(driver, tasks['task10'])

        orch_automation_tools.change_user(driver, USER_3PL)
        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )
        orch_automation_tools.exectue_simple_task(driver, tasks['task11'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task12'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task13'])

        orch_automation_tools.change_user(driver, USER_WH)

        orch_automation_tools.find_tasks(
            driver, 'P&G WH TaskList JP', container_number,
            'Equipment/Container#', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task14'])

        orch_automation_tools.change_user(driver, USER_3PL)

        orch_automation_tools.find_tasks(
            driver, 'P&G 3PL Task List JP', container_number,
            'Equipment/Container #', 'Consignment'
        )

        orch_automation_tools.exectue_simple_task(driver, tasks['task15'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task16'])

        orch_automation_tools.exectue_simple_task(driver, tasks['task17'])

    def tearDown(self):
        self.driver.quit()


class CITPNGJPPaymentTests(unittest.TestCase):
    """Test suite for CIT PNG JP IMPORT"""
    BASE_URL = 'https://ct-cit.damco.com/'
    CONTROL_JSON = os.path.join(
            os.getcwd(),
            'json_flow_data',
            'CIT_BASE.json'
        )
    EXCEL_PATH = os.path.join(
            os.getcwd(),
            'excel_files',
            'png',
            'jp',
            'payment'

        )
    JSON_PATH = os.path.join(
            os.getcwd(),
            'json_flow_data',
            'png',
            'jp',
            'payment'
        )
    USER_CREDENTIALS = orch_automation_tools.parse_json_data(
        os.path.join(
            os.getcwd(),
            'json_flow_data',
            'CIT_ACCESS.json'
        )
    )['png']['jp']['payment']
    excel_template = None
    excel_name = None

    def setUp(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(20)
        # self.driver.get(self.BASE_URL)
        orch_automation_tools.open_main_page(self.driver, self.BASE_URL)
        self.driver.maximize_window()
        self.test_file = os.path.join(
            os.getcwd(),
            'excel_files',
            "TEST_FILE.xlsx"
        )

    @unittest.skip("Skipping...")
    def test_png_payment_po(self):
        """P&G Payment JP Test. PO Conditions flow."""
        # Test case settings
        USER_4PL = self.USER_CREDENTIALS['4pl']
        test_case_name = 'wowlolo'
        json_file = os.path.join(self.JSON_PATH, 'png_po.json')
        excel_data = generate_excel_from_json(
            json_file, self.CONTROL_JSON, self.EXCEL_PATH
        )
        
        json_data = orch_automation_tools.parse_json_data(json_file)
        
        self.excel_template = os.path.join(
            self.EXCEL_PATH, json_data['template_name']
        )
        invoice_no = excel_data['invoice_number']
        tasks = json_data['tasks']
        driver = self.driver

        # Test case execution
        orch_automation_tools.login_user(driver, USER_4PL)
        orch_automation_tools.use_main_search_bar(driver, 'Excel Sheet Upload')
        orch_automation_tools.submit_excel_file(driver, self.excel_template, 'Submit')

        WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="messageBar"]'),
                '1 Files Imported Sucessfully'
            )
        )
        orch_automation_tools.close_current_tab(driver)

        # Go to "todo list" and do all tasks available as current user
        orch_automation_tools.find_payment_tasks(
            driver, 'P&G Payment Tracker To Do List JP', invoice_no
        )

        # Task 1 Invoice Verification Complete (JP)
        orch_automation_tools.exectue_simple_task(driver, tasks['task01'])

        # Task 2 Invoice Dispatched to P2P (JP)
        orch_automation_tools.exectue_simple_task(driver, tasks['task02'])

        # Task 3 Confirm Invoice Payment Made (JP)
        orch_automation_tools.exectue_simple_task(driver, tasks['task03'])

        # Task 4
        orch_automation_tools.exectue_simple_task(driver, tasks['task04'])

    @unittest.skip("Skipping...")
    def test_png_payment_fi(self):
        """P&G Payment JP Test. FI Conditions flow."""
        USER_4PL = self.USER_CREDENTIALS['4pl']

        json_file = os.path.join(self.JSON_PATH, 'png_fi_jptcd.json')
        excel_data = generate_excel_from_json(
            json_file, self.CONTROL_JSON, self.EXCEL_PATH
        )
        json_data = orch_automation_tools.parse_json_data(json_file)
        self.excel_template = os.path.join(
            self.EXCEL_PATH, json_data['template_name']
        )

        invoice_no = excel_data['invoice_number']
        tasks = json_data['tasks']

        driver = self.driver

        # Login to the system
        orch_automation_tools.login_user(driver, USER_4PL)
        # Upload generated xlsx file
        orch_automation_tools.use_main_search_bar(driver, 'Excel Sheet Upload')
        orch_automation_tools.submit_excel_file(driver, self.excel_template, 'Submit')

        WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="messageBar"]'),
                '1 Files Imported Sucessfully'
                )
        )
        orch_automation_tools.close_current_tab(driver)

        # Go to "todo list" and do all tasks available as current user
        orch_automation_tools.find_payment_tasks(
            driver, 'P&G Payment Tracker To Do List JP', invoice_no
        )

        # Task 1 Invoice Verification Complete (JP)
        orch_automation_tools.exectue_simple_task(driver, tasks['task01'])

        # Task 2 Invoice Dispatched to P2P (JP)
        orch_automation_tools.exectue_simple_task(driver, tasks['task02'])

        # Task 3 Confirm Invoice Payment Made (JP)
        orch_automation_tools.exectue_simple_task(driver, tasks['task03'])

        # Task 4
        orch_automation_tools.exectue_simple_task(driver, tasks['task04'])

        # Task 5
        orch_automation_tools.exectue_simple_task(driver, tasks['task05'])

    @unittest.skip("Skipping...")
    def test_png_payment_po_to_fi(self):
        """P&G Payment JP Test. SPO Conditions to FI."""
        USER_4PL = self.USER_CREDENTIALS['4pl']

        json_file = os.path.join(self.JSON_PATH, 'png_po_to_fi.json')
        excel_data = generate_excel_from_json(
            json_file, self.CONTROL_JSON, self.EXCEL_PATH
        )
        json_data = orch_automation_tools.parse_json_data(json_file)
        self.excel_template = os.path.join(
            self.EXCEL_PATH, json_data['template_name']
        )

        invoice_no = excel_data['invoice_number']
        tasks = json_data['tasks']

        driver = self.driver

        # Login to the system
        orch_automation_tools.login_user(driver, USER_4PL)
        # Upload generated xlsx file
        orch_automation_tools.use_main_search_bar(driver, 'Excel Sheet Upload')
        orch_automation_tools.submit_excel_file(driver, self.excel_template, 'Submit')

        WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element(
                (
                    By.XPATH,
                    '//*[@id="messageBar"]'), '1 Files Imported Sucessfully'
                )
        )
        orch_automation_tools.close_current_tab(driver)

        # Go to "todo list" and do all tasks available as current user
        orch_automation_tools.find_payment_tasks(
            driver, 'P&G Payment Tracker To Do List JP', invoice_no
        )

        # Task 1 Invoice Verification Complete (JP)
        orch_automation_tools.exectue_simple_task(driver, tasks['task01'])

        # Task 2 Invoice Dispatched to P2P (JP)
        orch_automation_tools.exectue_simple_task(driver, tasks['task02'])

        # Task 3 Confirm Invoice Payment Made (JP)
        orch_automation_tools.exectue_simple_task(driver, tasks['task03'])

        # Task 4
        orch_automation_tools.exectue_simple_task(driver, tasks['task04'])

        # Task 5
        orch_automation_tools.exectue_simple_task(driver, tasks['task05'])

    def tearDown(self):
        # close the browser window
        orch_automation_tools.move_excel_to_report(self.excel_template,  )
        self.driver.quit()


class CITPNGJPExportTests():
    pass


if __name__ == "__main__":
    unittest.main()

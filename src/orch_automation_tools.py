# Standard library import
import time
import datetime
import json
import os
import shutil

# Third party import
from selenium.common.exceptions import (
    TimeoutException,
    ElementNotVisibleException
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select


# Helper functions

def fill_task_fields(driver, field_data):
    """
    Fill fields based on dictionary with locators, types and values
    driver - instance of selenium webdriver
    field_data - dictionary with fields. 
                Key is fieldname;fieldtype. 
                Value is value to pass
    """
    for field, value in field_data.items():
        try:
            data = field.split(';')
            if data[1] == 'select':
                cur_field = Select(select_input_by_label(driver, data[0], data[1]))
                try:
                    cur_field.select_by_visible_text(value)
                except (
                    EC.NoSuchElementException,
                    EC.StaleElementReferenceException,
                    ElementNotVisibleException
                ):
                    print("Select option {} is invalid".format(value))
            elif data[1] == 'input-af':
                cur_field = select_input_by_label(driver, data[0], 'input')
                cur_field.send_keys(value)
                time.sleep(3)
                cur_field.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
            else:
                cur_field = select_input_by_label(driver, data[0], data[1])
                cur_field.send_keys(value)
        except (
            EC.NoSuchElementException,
            EC.StaleElementReferenceException,
            ElementNotVisibleException
        ):
            print("Field {} is invalid".format(data))
            raise
        time.sleep(1)


def use_task_context_menu(driver, task_name, status, action):
    """
    Function locates task, left clicks,
    right clicks and go to slected context menu item
    driver - selenium webdriver instance
    taskname, str -  name of task to target
    status, str - task status which is needed to complete it
    action, str -  action to perform on the context menu
    """
    for i in range(30):
        try:
            actionChains = ActionChains(driver)
            task = driver.find_element_by_xpath(
                f"//div[contains(text(),'{task_name}')]"
            )
            task.click()
            driver.find_element_by_xpath(
                f'//tr[contains(@class, "context selected")]\
                //div[contains(text(), "{status}")]'
            )
            time.sleep(3)
            task = driver.find_element_by_xpath(
                f"//div[contains(text(),'{task_name}')]"
            )
            actionChains.context_click(task).perform()
            time.sleep(3)
            driver.find_element_by_xpath(
                f'//div[@id="contextMenu"]//li[contains(text(),"{action}")]'
            ).click()
            break
        except (
            EC.NoSuchElementException,
            EC.StaleElementReferenceException,
            ElementNotVisibleException
        ):
            
            time.sleep(5)
            refresh_task_list(driver)
            continue
    else:
        print(f"Task {task_name} status is not valid, or task is not visible")


def submit_excel_file(driver, file_path, button):
    """
    Function handles file input that is invisible.
    driver - instance of selenium webdriver
    file_path, str -  path of the file to submit
    button, str - value on the button element that submits the file
    """
    actionChains = ActionChains(driver)

    time.sleep(2)
    upload_button = driver.find_element_by_xpath(
        '//span[contains(text(),"Browse...")]'
    )
    actionChains.move_to_element(upload_button).perform()

    invisible_div = driver.find_element_by_xpath('/html/body/div[last()]')
    driver.execute_script("arguments[0].style = ' ';", invisible_div)

    file_input = driver.find_element_by_xpath('//input[@type="file"]')
    file_input.send_keys(file_path)
    time.sleep(5)
    driver.find_element_by_xpath(f'//a[contains(text(),"{button}")]').click()


def parse_json_data(filename):
    """
    Function returns parsed json data.
    file_path, str -  path of the file to submit
    """
    with open(filename) as fn:
        config_data = json.load(fn)
    return config_data


def login_user(driver, credentials):
    """
    Function login user to the system from the index page.
    driver - instance of selenium webdriver\
    credentials, dict - dictionary with keys: 'username' and 'password'
    """
    login = credentials['username']
    password = credentials['password']
    login_field = select_input_by_label(driver, 'Username', 'input')
    login_field.send_keys(login)
    password_field = select_input_by_label(driver, 'Password', 'input')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)


def logout_user(driver):
    """
    Function perform logging out user from the main page.
    driver - instance of selenium webdriver
    """
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element_by_xpath('//*[@id="page"]/div[2]/a[4]/div').click()
    driver.find_element_by_xpath('//*[@id="conf"]/div[3]/a[1]').click()
    time.sleep(5)


def change_user(driver, credentials):
    """
    Function wraps up logging out and logging in.
    driver - selenium webdriver instance
    credentials, dict - dictionary with keys: 'username' and 'password'
    """
    driver.close()
    time.sleep(2)
    logout_user(driver)
    login_user(driver, credentials)


def select_input_by_label(driver, label, input_type):
    """
    Function selects input element, based on it's label
    driver - instance of selenium webdrier
    label, str - label of the target input
    input_type, str - type of the target input
    """
    func_string = 'find_element_by_xpath'
    return getattr(
        driver, func_string
    )(f'//div[@name="{label}"]//{input_type}')


def use_main_search_bar(driver, menu_item):
    """
    Search program in main search bar
    driver - instance of selenium webdriver
    menu_item, str - name of the searched program
    """
    for i in range(3):
        try:
            time.sleep(2)
            search_field = driver.find_element_by_xpath(
                '*//div[@id="quicklinks"]//input[1]'
            )
            search_field.send_keys(menu_item)
            time.sleep(4)
            driver.find_element_by_xpath(
                f'//div[@id="tooltip"]//li[contains(text(),"{menu_item}")]'
            ).click()
            wait_for_title_load(driver, menu_item)
            break
        except (ElementNotVisibleException, EC.NoSuchElementException) as error:
            continue
    else:
        print("There is a problem with selecting program {}".format(menu_item))


def wait_for_title_load(driver, title):
    """
    Function handles waiting for the page to load basing on the title
    driver - instance of selenium webdriver
    title, str - title of the page to load
    """
    driver.switch_to.window(driver.window_handles[-1])
    try:
        WebDriverWait(driver, 5).until(
            EC.title_is(title)
        )
    except TimeoutException:
        driver.switch_to.window(driver.window_handles[-1])
    driver.switch_to.window(driver.window_handles[-1])


def close_current_tab(driver):
    """
    Function closes current tab
    driver - instance of selenium webdriver
    """
    if len(driver.window_handles) > 1:
        driver.close()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])


def refresh_task_list(driver):
    """
    Function refresh task list and handles problem with refresh  button
    driver - selenium webdriver instance
    """
    for i in range(2):
        try:
            actionChains = ActionChains(driver)

            actions = driver.find_element_by_xpath(
                "//div[contains(text(),'Actions')]"
            )
            actionChains.move_to_element(actions).click(actions).perform()

            refresh = driver.find_element_by_xpath(
                "//div[@id='contextMenu']//li[contains(text(),'Refresh')]"
            )
            actionChains.move_to_element(refresh).click(refresh).perform()
            time.sleep(2)
            break
        except (EC.NoSuchElementException, EC.StaleElementReferenceException):
            driver.find_element_by_xpath(
                '//div[contains(text(), "Selected")]'
            ).click()
            continue


def exectue_simple_task(driver, task_data):
    """
    Function executes simple task, with only one window based on json data
    driver - selenium webdriver instance
    task_data, dict - dictionary with all informations about task
    """
    task_name = task_data['name']
    task_status = task_data['status']
    context_action = task_data['action']
    task_fields = task_data['fields']
    submit_task = task_data['submit']

    use_task_context_menu(driver, task_name, task_status, context_action)
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])

    fill_task_fields(driver, task_fields)

    driver.find_element_by_xpath(
        f"//a[contains(text(),'{submit_task}')]"
    ).click()
    WebDriverWait(driver, 120).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
    )


def exectue_task_with_upload(driver, task_data, test_file):
    """
    Function executes task with one additional upload window based on json data
    driver - selenium webdriver instance
    task_data, dict - dictionary with all informations about task
    test_file, str - path to the upload file
    """
    task_name = task_data['name']
    task_status = task_data['status']
    context_action = task_data['action']
    task_fields = task_data['fields']

    use_task_context_menu(driver, task_name, task_status, context_action)
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])

    fill_task_fields(driver, task_fields)

    driver.find_element_by_xpath("//a[contains(text(),'Proceed')]").click()

    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    submit_excel_file(driver, test_file, 'Save')

    WebDriverWait(driver, 60).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
    )


def find_tasks(driver, program, reference, label, entity="Shipment Order"):
    """
    Function finds task list for given instance
    driver - selenium webdriver instance
    program, str - name of the program where to look for tasks
    reference, str - shipment order or container number, depending on settings
    label, str - label of the field to pass reference
    entity, str - task level to choose at Target Entity
    """
    use_main_search_bar(driver, program)
    time.sleep(4)
    for i in range(5):
        try:
            driver.find_element_by_xpath(
                '//div[@id="tabs"]//a[contains(text(), "Search")]'
            ).click()
            break
        except EC.NoSuchElementException:
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(5)

    select_cn = Select(select_input_by_label(
        driver, 'Target Entity', 'select')
    )
    select_cn.select_by_visible_text(entity)
    time.sleep(4)

    reference_field = select_input_by_label(
        driver, label, 'input[@type="text"]'
    )
    reference_field.send_keys(reference)

    driver.find_element_by_xpath("//a[contains(text(),'Search')]").click()


def find_payment_tasks(
    driver, program,
    invoice, label='Link ID / Invoice Number'
):
    """
    Function finds task list for given instance in payment process
    driver - selenium webdriver instance
    program, str - name of the program where to look for tasks
    invoice, str - invoice number
    label, str - label of the field to pass invoice
    """
    use_main_search_bar(driver, program)
    time.sleep(4)

    for i in range(5):
        try:
            driver.find_element_by_xpath(
                '//div[@id="tabs"]//a[contains(text(), "Search")]'
            ).click()
            break
        except EC.NoSuchElementException:
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(5)

    invoice_field = select_input_by_label(driver, label, 'input[@type="text"]')
    invoice_field.send_keys(invoice)

    driver.find_element_by_xpath("//a[contains(text(),'Search')]").click()


def open_main_page(driver, url):
    for i in range(3):
        try:
            driver.get(url)
            time.sleep(5)
            break
        except:
            driver.quit()


def add_object_to_result_json(json_path, test_id, nowdate):
    """
    Add new object to result json
    json_path, str - path to environment json
    test_id, str - datetime formated for files ending
    nowdate, str - datetime formated for better readability
    """
    with open(json_path, 'r+') as jsonFile:
        data = json.load(jsonFile)
    data['current_id'] = test_id
    data[test_id] = {
        "datetime":nowdate,
        "directory":test_id
    }
    with open(json_path, "w") as jsonFile:
        json.dump(data, jsonFile)


def move_excel_to_report(path, name, folder, reference):
    """
    Moves excel input file to report folder with changed name
    path, str - path to the source excel
    name, str - name of the source excel
    folder, str - name of the destination folder
    reference, str/int - reference number of the given excel
    """
    if os.path.exists(path):
        filename = '{}_{}{}'.format(name[:-5], reference, name[-5:])
        report_folder = os.path.join(
            os.getcwd(),
            'reports',
            folder
        )
        if not os.path.exists(report_folder):
            os.mkdir(report_folder)

        destination_path = os.path.join(
            report_folder,
            filename
        )
        shutil.copy2(path, destination_path)


def create_directory(json_path):
    """
    Function prepares directory for reporting and pass it into json file.
    Tests can use this directory to copy excell files.
    json_path, str - path to json that stores test results
    """
    nowdate = datetime.datetime.now()
    file_date = nowdate.strftime('%d_%m_%Y_%H_%M')
    format_date = nowdate.strftime('%d.%m.%Y %H:%M')
    add_object_to_result_json(json_path, file_date, format_date)


def submit_main_excel(driver, excel_file, program="Excel File Upload"):
    """
    Function wraps up navigating to excel file upload program,
    uploads file and wait for it to process
    """
    use_main_search_bar(driver, program)
    submit_excel_file(driver, excel_file, 'Submit')

    WebDriverWait(driver, 120).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, '//*[@id="messageBar"]'),
            '1 Files Imported Sucessfully'
        )
    )
    try:
        driver.find_element_by_xpath(
            "//td[contains(text(),'Accepted')]"
        ).click()
    except (EC.NoSuchElementException, EC.StaleElementReferenceException) as error:
        print("File was processed with errors")
        raise

    close_current_tab(driver)
# Standard library import
import os
import time
import unittest
import json

# Third party import
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options


# Local import
import access_file

# Helper functions

def fill_task_fields(driver, field_data):
    """Fill fields based on dictionary with locators, types and values"""
    for field, value in field_data.items():
        data = field.split(';')
        if data[1] == 'select':
            cur_field = Select(select_input_by_label(driver, data[0], data[1]))
            cur_field.select_by_visible_text(value)
        else:
            cur_field = select_input_by_label(driver, data[0], data[1])
            cur_field.send_keys(value)
        
        time.sleep(1)


def use_task_context_menu(driver, task_name, status, action):
    """Function locates task, left clicks, right clicks and go to slected context menu item"""
    for i in range(15):
        try:
            actionChains = ActionChains(driver)
            task = driver.find_element_by_xpath(f"//div[contains(text(),'{task_name}')]")
            task.click()
            task_row_status = driver.find_element_by_xpath(
                f'//tr[contains(@class, "context selected")]//div[contains(text(), "{status}")]'
            )
            time.sleep(3)
            task = driver.find_element_by_xpath(f"//div[contains(text(),'{task_name}')]")
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
        ) as error:
            print("Task status is not valid")
            print(error)
            time.sleep(10)
            refresh_task_list(driver)
            continue
    

def submit_excel_file(driver, file_path, button):
    """Function handles file input that is invisible"""
    actionChains = ActionChains(driver)

    # Locate and move over Browse button to run JS script
    upload_button = driver.find_element_by_xpath('//span[contains(text(),"Browse...")]')
    actionChains.move_to_element(upload_button).perform()

    # Locate and remove all styling from invisible div
    invisible_div = driver.find_element_by_xpath('/html/body/div[last()]')
    driver.execute_script("arguments[0].style = ' ';", invisible_div)

    # Submit test file
    # file_input = driver.find_element_by_xpath('/html/body/div[last()]/input')
    file_input = driver.find_element_by_xpath('//input[@type="file"]')
    file_input.send_keys(file_path)
    time.sleep(5)
    driver.find_element_by_xpath(f'//a[contains(text(),"{button}")]').click()


def parse_json_data(filename):
    """Function returns parsed json data"""
    with open(filename) as fn:
        config_data =  json.load(fn)
    return config_data


def login_user(driver, login, password):
    login_field = select_input_by_label(driver, 'Username', 'input')
    login_field.send_keys(login)
    password_field = select_input_by_label(driver, 'Password', 'input')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)


def logout_user(driver):
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element_by_xpath('//*[@id="page"]/div[2]/a[4]/div').click()
    driver.find_element_by_xpath('//*[@id="conf"]/div[3]/a[1]').click()
    time.sleep(5)


def select_input_by_label(driver, label, input_type):
    """Function selects input element, based on it's label"""
    func_string = 'find_element_by_xpath'
    return getattr(driver, func_string)(f'//div[@name="{label}"]//{input_type}')


def use_main_search_bar(driver, menu_item):
    """Search program in main search bar"""
    time.sleep(2)
    search_field = driver.find_element_by_xpath('*//div[@id="quicklinks"]//input[1]')
    search_field.send_keys(menu_item)
    time.sleep(4)
    search_field.send_keys(Keys.ARROW_DOWN)
    search_field.send_keys(Keys.RETURN)
    wait_for_title_load(driver, menu_item)


def wait_for_title_load(driver, title):
    driver.switch_to.window(driver.window_handles[-1])
    try:
        WebDriverWait(driver, 5).until(
            EC.title_is(title)
        )
    except TimeoutException:
        driver.switch_to.window(driver.window_handles[-1])
    driver.switch_to.window(driver.window_handles[-1])


def fill_fields_from_json(driver, field_data):
    """
    Function fills fields from json. Key = 'Field name' , Value = 'value'
    Takes argument driver, and field_data which should be dictionary
    """
    for field, value in field_data.items():
        cur_field = select_input_by_label(driver, field, 'input')
        cur_field.send_keys(value)
        if field == 'Country':
            time.sleep(1)
            cur_field.send_keys(Keys.ARROW_DOWN)
            cur_field.send_keys(Keys.RETURN)
        time.sleep(1)


def close_current_tab(driver):
    """Function close the current tab, wait 2 secs and switches to last opened window"""
    driver.close()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])


def refresh_task_list(driver):
    for i in range(5):
        try:
            driver.find_element_by_xpath("//div[contains(text(),'Actions')]").click()
            driver.find_element_by_xpath("//div[@id='contextMenu']//li[contains(text(),'Refresh')]").click()
            time.sleep(2)
        except (EC.NoSuchElementException, EC.StaleElementReferenceException) as error:
            print("Action button error")


def exectue_simple_task(driver, task_data):
    """Function finishes simple task based on json data"""
    task_name = task_data['name']
    task_status = task_data['status']
    context_action = task_data['action']
    task_fields = task_data['fields']
    submit_task = task_data['submit']

    # Pass task data to helper function
    use_task_context_menu(driver, task_name, task_status, context_action)
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])

    # Fill fields
    fill_task_fields(driver, task_fields)

    # Submit task
    driver.find_element_by_xpath(f"//a[contains(text(),'{submit_task}')]").click()
    WebDriverWait(driver, 60).until(
        EC.text_to_be_present_in_element((By.XPATH, '//*[@id="messageBar"]'), 'Task(s) Processed')
    )
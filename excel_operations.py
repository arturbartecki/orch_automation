import os
import json
from openpyxl import load_workbook

import orch_automation_tools


def increment_control_number_json(json_base):
    """
    Function increments value in given json.
    json_base, str - json file where data is stored
    """
    with open(json_base, 'r+') as jsonFile:
        data = json.load(jsonFile)

    inv_no = data['control_number']
    inv_no = int(inv_no) + 1
    data['control_number'] = str(inv_no)

    with open(json_base, "w") as jsonFile:
        json.dump(data, jsonFile)


def generate_excel_from_json(js_file, control_js, path):
    """
    Function generates excell file basing on json file
    js_file, str - json file with flow data
    control_js, str - json file with control number for whole environment
    path, str - path to excel file
    """
    test_data = {}
    increment_control_number_json(control_js)
    js_data = orch_automation_tools.parse_json_data(js_file)
    control_data = orch_automation_tools.parse_json_data(control_js)
    excel_template = os.path.join(path, js_data['template_name'])
    
    wb_file = load_workbook(excel_template, data_only=True)
    wb_sheet = wb_file._sheets[0]
    for key, value in js_data['excel_data'].items():
        if value['control_num'] and value['control_num'] == 'Yes':
            for field in value['fields']:
                control_num = control_data['control_number']
                test_data[key] = f"{value['value']}{control_num}"
                wb_sheet[field].value = f"{value['value']}{control_num}"
        else:
            for field in value['fields']:
                wb_sheet[field].value = value['value']
    wb_file.save(excel_template)
    return test_data

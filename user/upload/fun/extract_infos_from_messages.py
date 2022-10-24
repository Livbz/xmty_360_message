import copy
import re

import numpy as np


def main(messages):
    """
            if return_data["code"] is false:
                then an error is occur during this function
            if return_data["code"] is not false:
                then info of message is extracted and is stored in return_data["data"]["infos"] as a list, whose
                elements are string of message.
    :param messages: messages is a list, whose element, message, are just a string of message
    :return:
    """
    original_return_data = {"success": False, "code": "-1", "message": "error", "data": {}}
    return_data = copy.deepcopy(original_return_data)
    try:
        infos = []
        for message in messages:
            return_extracted_infos = extract_info_from_message(message)
            infos.append(return_extracted_infos)
        return_data["data"]["infos"] = infos
        return return_data
    except:
        return original_return_data


def extract_info_from_message(message):
    original_return_data = {"code": False, "data": {}, "message": "error"}
    return_data = copy.deepcopy(original_return_data)
    try:
        account_message_piece = re.findall(r'（户号.*?），您用', message)[0]
        time_period_message_pieces = re.findall(r'您用电周期.*?内', message)
        electricity_amount_message_pieces = re.findall(r'电量.*?度', message)
        electricity_bill_message_pieces = re.findall(r'电费.*?元', message)

        time_periods = [extract_middle("您用电周期", time_period_message_piece, "内") for time_period_message_piece in time_period_message_pieces]
        electricity_amounts = [float(extract_middle("电量", electricity_amount_message_piece, "度")) for electricity_amount_message_piece in electricity_amount_message_pieces]
        electricity_bills = [float(extract_middle("电费", electricity_bill_message_piece, "元")) for electricity_bill_message_piece in electricity_bill_message_pieces]
        accounts = [extract_middle("（户号", account_message_piece, "），您用") for time_period_message_piece in time_period_message_pieces]

        length_array = np.array([len(time_periods), len(electricity_amounts), len(electricity_bills), len(accounts)])
        if np.sum(length_array-np.min(length_array))!=0:
            return {"code": False, "data": message, "message": "error"}

        infos = {"account": accounts, "time_periods": time_periods, "electricity_amounts": electricity_amounts, "electricity_bills": electricity_bills}

        return_data["data"]["infos"] = infos
        return_data["message"] = "success"
        return_data["code"] = True
        return return_data
    except:
        error_data = {"code": False, "data": message, "message": "error"}
        return error_data


def extract_middle(start_string, full_string, end_string):
    middle_and_end = full_string.split(start_string)[1]
    middle_string = middle_and_end.split(end_string)[0]
    return middle_string
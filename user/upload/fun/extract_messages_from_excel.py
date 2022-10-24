import xlrd
import copy


def main(filename):
    """

    open the excel, ana locate the cell of 短信内容, then extract messages into the return_data

    :param filename: it is just the filename
    :return: a dict
            return_data["message"] stores the message sent back from the function
            if return_data["success"] is false:
                then an error is occurred during this function
                and return_data["code"] = "-1"
            if return_data["success"] is not false:
                then messages are extracted from excel and are stored in return_data["data"]["messages"] as a list,
                whose elements are string of one piece of message.
    """
    original_return_data = {"success": False, "code": "-1", "message": "error", "data": {}}
    return_data = copy.deepcopy(original_return_data)
    try:
        workbook = xlrd.open_workbook(filename)
        sheet = workbook.sheet_by_index(0)
        message_header_index = sheet.row_values(0).index('短信内容')  # 获取短信内容这一单元格的index
        message_cells = sheet.col(message_header_index)[1:]
        messages = [text.value for text in message_cells]

        return_data["data"]["messages"] = messages
        return_data["message"] = "success"
        return_data["code"] = 200
        return_data["success"] = True
        return return_data
    except Exception as e:
        raise e
        return original_return_data
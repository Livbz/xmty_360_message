import pandas as pd
import xlwt

from user.upload.fun import extract_messages_from_excel as extract_messages_from_excel
from user.upload.fun import extract_infos_from_messages as extract_infos_from_messages
from .RecordObject import RecordObject
from .LineObject import LineObject
from .DateObject import DateObject
from flask import session


def do_one_chuck(one_chuck, name):
    # Just reset, don't ask why, and don't delete the following line, or YOU WOULD FUCK UP :)
    DateObject.reset_year_list()
    """
    receive a DataFrame, process it, sum up the electricity_amount and the electricity_bill, then write the result into 
                        a excel
    :param one_chuck: one_chuck is a DataFrame that has the same date period, name
    :param name: date period
    :return: nothing
    """
    RecordList_real = list()
    RecordList_fake = list()
    for i, row in one_chuck.iterrows():
        try:
            period_string = row["period"]
            electricity_amount = row["electricity_amount"]
            electricity_bill = row["electricity_bill"]
            Record = RecordObject(period_string, electricity_amount, electricity_bill)
            if Record.real:
                RecordList_real.append(Record)
            else:
                RecordList_fake.append(Record)
        except:
            print()

    year_list = list(RecordObject.get_yearlist())
    year_list.sort()

    lines = {year: {} for year in year_list}
    for year in year_list:
        for month in range(12):
            month = month + 1
            lines[year][month] = LineObject(year, month)

    for record in RecordList_real:
        lines[record.after_year][record.after_month].append(record)
    LineObject.generate_transformer(year_list, 10)
    xl = xlwt.Workbook(encoding='UTF-8')
    sheet = xl.add_sheet('结果', cell_overwrite_ok=True)
    sheet2 = xl.add_sheet('结果复制', cell_overwrite_ok=True)
    sheet.write(0, 0, "总电量")
    sheet.write(0, 1, "总电费")
    sheet.write(0, 2, "平均电价")

    sheet2.write(0, 0, "总电量")
    sheet2.write(0, 1, "总电费")
    sheet2.write(0, 2, "平均电价")


    for i in range(year_list.__len__()):
        year = year_list[i]
        max_o = LineObject.year_max_object[year]*4-1
        try:
            sheet.write_merge(0 + 15*i, 0 + 15*i, 4+1, 4+1+max_o, str(year)+"/电量/电费/单价")
            sheet2.write_merge(0 + 15*i, 0 + 15*i, 4+1, 4+1+max_o, str(year)+"/电量/电费/单价")
        except:
            sheet.write(0 + 15*i, 5, str(year) + "ERROR")
            sheet2.write(0 + 15*i, 5, str(year) + "ERROR")
        for month in range(12):
            sheet.write(1 + month + 15*i, 4+0, str(month+1) + "月")
            sheet2.write(1 + month + 15*i, 4+0, str(month+1) + "月")
            month = month + 1
            lines[year][month].sheet_write(sheet, month + 15*i, 4+1)
            lines[year][month].sheet_write(sheet2, month + 15*i, 4+1)

    if RecordList_fake.__len__()!=0:
        sheet.write_merge(46, 46, 0, 3, "差错退补")
        sheet2.write_merge(46, 46, 0, 3, "差错退补")
        n = 1
        sheet.write(46 + n, 0, "电量")
        sheet.write(46 + n, 1, "电费")
        sheet.write_merge(46 + n, 46 + n, 2, 3, "日期区间")
        sheet2.write(46 + n, 0, "电量")
        sheet2.write(46 + n, 1, "电费")
        sheet2.write_merge(46 + n, 46 + n, 2, 3, "日期区间")
        n = n + 1
        for Record in RecordList_fake:
            sheet.write(46 + n, 0, Record.electricity_amount)
            sheet.write(46 + n, 1, Record.electricity_bill)
            sheet.write_merge(46 + n, 46 + n, 2, 3, Record.period_string)
            sheet2.write(46 + n, 0, Record.electricity_amount)
            sheet2.write(46 + n, 1, Record.electricity_bill)
            sheet2.write_merge(46 + n, 46 + n, 2, 3, Record.period_string)
            n = n + 1
    xl.save("temp/" + name + ".xls")


def process(filename):
    returned_extracted_messages = extract_messages_from_excel.main(filename)
    if not returned_extracted_messages["code"]:
        pass
    messages = returned_extracted_messages["data"]["messages"]
    returned_extracted_infos = extract_infos_from_messages.main(messages)
    returned_infos = returned_extracted_infos["data"]["infos"]

    account_list = list()
    period_list = list()
    electricity_amount = list()
    electricity_bill = list()
    error_message = list()
    for return_info in returned_infos:
        if return_info['code']:
            info = return_info["data"]["infos"]

            account_list = account_list + info['account']
            period_list = period_list + info['time_periods']
            electricity_amount = electricity_amount + info['electricity_amounts']
            electricity_bill = electricity_bill + info['electricity_bills']
        else:
            error_message.append(return_info["data"])
    if error_message.__len__() != 0:
        return {"code": False, "data": error_message}

    data = pd.DataFrame(
        {"account_number": account_list, "period": period_list, "electricity_amount": electricity_amount,
         "electricity_bill": electricity_bill})

    unique_index = data["account_number"].unique()
    if session["filecode"]!=session["token_now"]:
        return {"code": True, "data": unique_index}

    for index in unique_index:
        chunk = data[data["account_number"] == index]
        do_one_chuck(chunk, index)
    return {"code": True, "data": unique_index}


if __name__ == '__main__':
    print(process("东林城市.xlsx"))

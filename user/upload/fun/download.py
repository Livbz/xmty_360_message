
import os
from flask import make_response
from flask import send_from_directory


def download_file(filename):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    directory = os.getcwd()  # 假设在当前目录
    print(filename)
    response = make_response(
        send_from_directory("temp/", filename.encode('utf-8').decode('utf-8'), as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response
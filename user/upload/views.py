from . import user_upload_bp
from flask import render_template, redirect, url_for, request
import hashlib
import time
import json
from user.upload.fun.main import process
from user.upload.fun.download import download_file
import zipfile
from flask import session
from dbfun import dbfun
from tools.testMail import send_email
from tools.encrypt import encrpto, dencrpto


@user_upload_bp.route('/check_code/', methods=['POST'])
def check_code():
    data = request.get_data()
    data = data.decode()
    data = json.loads(data, strict=False)
    code = data.get('code')

    RES = {
        'check': True
    }

    if time.time() - int(dencrpto(code)) < 60*30:
        session['login'] = '200'
        session['start_time'] = time.time()
        return RES


@user_upload_bp.route('/login/', methods=['POST'])
def login():
    data = request.get_data()
    data = data.decode()
    data = json.loads(data,strict=False)
    account = data.get('account')

    RES = {
        "send": False,
        "msg": "Invalid account."
    }
    Eamil_map = {
        "Kuang": "harry.k@xmtyet.com",
        "ShiXu": "sx@xmtyet.com",
        "Admin": "yby@xmtyet.com"
    }

    session.clear()

    if account not in ["Kuang","ShiXu","Admin"]:
        send_email(encrpto(), account + '@xmtyet.com')
        session['level'] = 'salesman'
        return RES
    else:
        send_email(encrpto(), Eamil_map[account])
        session['level'] = 'super'
        return RES





@user_upload_bp.route("/")
def u_u_upload():
    """
    As shown below, each time when the user is visiting the upload page, token_now and o_token are generated based on
    the current time. And token_now and o_token are set to be the same. The propose of those two token is that:
    when the user is uploading the file, it might take a while for the server to respond, during which the user might
    click the submit button again. The submit will go to the view function u_u_api_upload, in which the token_now will
    be upgraded, but the o_token will remain the same. When the user is clicking submit button again, the view function
    u_u_api_upload will find that two tokens are not the same, so it would return nothing.

    This mechanism will avoid duplicate submission!!!
    """
    if session.get('login') == '200':
        session.clear()  # be careful
        session["token_now"] = hashlib.md5(str(time.time()).encode("utf-8")).hexdigest()
        session["o_token"] = session["token_now"]
        return render_template('user_upload_index.html')
    else:
        return render_template('map_login.html')


@user_upload_bp.route("/", methods=["POST"])
def u_u_api_upload():
    if session["o_token"] == session["token_now"]:
        session["token_now"] = hashlib.md5(str(time.time()).encode("utf-8")).hexdigest()
        if request.method == 'POST':
            f = request.files['fileToUpload']

            if f.filename == "":
                return redirect(url_for("jump.jump", reason="没有收到文件...", target="user_upload.u_u_upload"))
            if f.filename.split(".")[1] not in ["xls", "xlsx"]:
                return redirect(url_for("jump.jump", reason="仅支持xls或xlse文件", target="user_upload.u_u_upload"))
            else:
                file_code = session["token_now"]
                session["filecode"] = file_code
                session["upload_filename"] = f.filename
                f.save("temp/" + file_code)
                return redirect(url_for("user_upload.u_u_analysis", filename=f.filename))
        else:
            return "sssssss"
    return "请勿重复提交"


@user_upload_bp.route("/analysis/")
def u_u_analysis():
    return redirect(url_for("user_upload.get_user_input"))


@user_upload_bp.route("/analysis/go")
def get_user_input():
    print("-----")
    print(session["filecode"])
    return_data = process("temp/" + session["filecode"])
    if not return_data["code"]:
        return render_template("error.html", datas=return_data["data"])

    session["zip_name"] = session["upload_filename"].split(".")[0] + session["filecode"] + ".zip"
    session["token_now"] = hashlib.md5(str(time.time()).encode("utf-8")).hexdigest()

    file_list = return_data["data"]
    zip_name = session["upload_filename"].split(".")[0] + session["filecode"] + ".zip"
    with zipfile.ZipFile("temp/" + zip_name, 'w') as zf:
        for i in range(len(file_list)):
            zf.write("temp/" + file_list[i] + ".xls", "temp/" + file_list[i] + ".xls")

    session["zip_name"] = zip_name
    session["token_now"] = hashlib.md5(str(time.time()).encode("utf-8")).hexdigest()
    session["o_token"] = session["token_now"]
    return render_template("message.html", file_list=file_list, prefix=session["upload_filename"], name=session["upload_filename"].split(".")[0])


@user_upload_bp.route("/downloadpage", methods=["POST"])
def download():
    if session["o_token"] == session["token_now"]:
        session["token_now"] = hashlib.md5(str(time.time()).encode("utf-8")).hexdigest()
        companynames = request.form.getlist("companyname")
        accountnumbers = request.form.getlist("accountnumber")
        usertypes = request.form.getlist("usertype")
        voltages = request.form.getlist("voltage")
        volumns = request.form.getlist("volumn")
        dbfun.insert_into_db(companynames, accountnumbers, usertypes, voltages, volumns)
    return render_template("download.html", filename=session["upload_filename"])


@user_upload_bp.route("/downloadpage")
def download_api():
    return download_file(session["zip_name"])

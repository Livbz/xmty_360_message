from flask import Blueprint

user_upload_bp = Blueprint('user_upload', __name__,static_folder='./static/',
    template_folder='./templates/',)

from . import views
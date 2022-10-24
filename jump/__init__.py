from flask import Blueprint

jump_bp = Blueprint('jump', __name__)

from . import views
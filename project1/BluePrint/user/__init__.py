from flask import Blueprint

user_print = Blueprint("user_print", __name__)

from BluePrint.user.views import *



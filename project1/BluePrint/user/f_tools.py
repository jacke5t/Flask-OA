import os
import hashlib
import uuid

from functools import wraps

from flask import request, redirect
from .models import *


def change_filename(filename):
    """
    修改文件名称
    :param filename: 要修改的文件名
    :return: 返回修改后的文件名
    """
    uuid_str = str(uuid.uuid1())
    file_type = os.path.splitext(filename)[1]
    # print(uuid_str, file_type)
    return uuid_str + file_type


def encrypt_password(password):
    """
    密码加密函数
    :param password: 要加密的密码
    :return: 加密后的字符串
    """
    md5 = hashlib.md5()
    md5.update(bytes(password, encoding='utf-8'))
    result = md5.hexdigest()
    return result


def login_check(fun):
    @wraps(fun)
    def inner(*args, **kwargs):
        user_id = request.cookies.get("user_id")
        username = request.cookies.get("username")
        if username and user_id:
            user = Person.query.filter(Person.id == int(user_id)).first()
            if user.username == username:
                return fun(*args, **kwargs)
        return redirect('/login')
    return inner

from flask import session
from BluePrint.user.models import *


def middleware_template():
    # 数据
    data = {
        "job": "",
        "show_subordinate": True,  # 是否显示下属考勤
        "show_news": True,  # 是否显示新闻管理
        "show_person": True,  # 是否显示职员管理
        "show_permission": True,  # 是否显示权限管理
    }
    # 当前用户
    username = session.get("username")
    person = Person.query.filter(Person.username == username).first()
    data["job"] = person.person_position_map.name
    # 新闻管理权限
    p_news = Permission.query.get(1)
    # 人事管理权限
    p_person = Permission.query.get(2)
    # 权限管理权限
    p_permission = Permission.query.get(4)

    data["show_subordinate"] = True if person.person_position_map.level > 1 else False  # 是否显示下属
    data["show_news"] = True if person.person_position_map in p_news.permission_position_map else False  # 是否显示新闻
    data["show_person"] = True if person.person_position_map in p_person.permission_position_map else False  # 是否显示职员管理
    data["show_permission"] = True if person.person_position_map in p_permission.permission_position_map else False  # 是否显示权限管理

    # 返回
    return data
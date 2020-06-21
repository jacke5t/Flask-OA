from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand
from flask_wtf import CSRFProtect

from BluePrint.filter import *

# 使用pymysql兼容mysqldb
import pymysql
pymysql.install_as_MySQLdb()


# 创建空的db对象
db = SQLAlchemy()
csrf = CSRFProtect()
app = Flask(__name__)  # 创建app


def create_app(obj):
    """
    创建app函数
    :param obj: 配置文件类
    :return: goods
    """
    app.config.from_object(obj)  # app的配置类
    # db与app关联
    db.init_app(app)
    # csrf与app关联
    csrf.init_app(app)
    # 该引用必须放在函数里面，不然会循环引用
    from BluePrint.user import user_print
    # 注册蓝图
    app.register_blueprint(user_print)
    app.add_template_filter(get_datatime, "get_datatime")
    app.add_template_filter(get_title, "get_title")
    from BluePrint.middleware import middleware_template
    app.add_template_global(middleware_template, "middleware_template")
    return app


class Run(Command):
    def run(self):
        app.run(port="5000", host="127.0.0.1")


def make_manage():
    """
    创建命令的函数
    :return:  创建命令后的对象
    """
    # 服务启动命令安装
    manager = Manager(app)  # 命令行绑定应用
    manager.add_command("run", Run)  # 安装命令
    # 数据库操作命令安装
    migrate = Migrate(app, db)  # 绑定应用和数据库
    manager.add_command("db", MigrateCommand)  # 安装命令
    return manager


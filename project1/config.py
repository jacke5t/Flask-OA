import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # 指定文件存放的目录


class Develop:
    """开发环境配置"""
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "OA.sqlite")  # sqlite数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 支持追踪修改
    SQLALCHEMY_ECHO = True  # sql语句输出
    SECRET_KEY = "session"  # session盐值
    DEBUG = True  # 开启debug模式


class Product:
    """生产环境配置"""
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1/oa"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "session"



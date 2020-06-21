from flask_wtf import FlaskForm
import wtforms
from wtforms import validators, ValidationError


def check_username(form, field):
    """
    自定义校验：验证用户名不能包含敏感信息
    :param form: 表单
    :param form:字段
    """
    print("当前字段的值：", field.data)
    data_list = ["admin", "nb"]
    # 判断
    for data in data_list:
        if field.data.find(data) != -1:
            raise ValidationError("用户名不能包含敏感信息")


class RegisterForm(FlaskForm):
    username = wtforms.StringField(
        # 文本
        label="用户名",
        # 验证规则
        validators=[
            validators.Length(min=2, max=16, message="用户名长度在2-16之间"),
            check_username
        ]
    )
    password = wtforms.PasswordField(
        # 文本
        label="密码",
        # 验证规则
        validators=[
            validators.DataRequired(message="密码必填")
        ]
    )
    repassword = wtforms.PasswordField(
        # 文本
        label="重复输入密码",
        # 验证规则
        validators=[
            validators.EqualTo("password", message="密码不一致")
        ]
    )

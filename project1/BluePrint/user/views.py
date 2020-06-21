import os
from datetime import datetime

from functools import wraps
from BluePrint import csrf
from BluePrint.user import user_print
from flask import render_template, session, redirect, request, jsonify
from sqlalchemy import func
import uuid

from .f_tools import *


# 首页
@user_print.route('/')
@login_check
def index():
    news_list = News.query.order_by(News.pubtime.desc()).limit(4).all()
    person = Person.query.filter(Person.username == session.get("username")).first()
    attendance_list = Attendance.query.filter(Attendance.person_id == person.id).order_by(Attendance.start.desc()).limit(5).all()
    return render_template('index.html', **locals())


# 职员管理
@user_print.route('/person')
@login_check
def person():
    department_type = request.args.get("dy", default="")
    person_username = request.args.get("person_username", default="")
    page_size = 10  # 每页的个数
    page_now = int(request.args.get("page_now", default=1))
    if person_username:
        # 根据输入的内容查询用户名
        person_username_search = f"%{person_username}%"
        person_query = Person.query.filter(Person.username.like(person_username_search))
    elif department_type:
        # 根据部门查询员工
        # person_list = []
        # d = Department.query.filter(Department.id == department_type).first()
        # position_list = d.department_position_map
        # for position in position_list:
        #     person_list.extend(position.position_person_map)
        # print(position_list)
        person_query = Person.query.outerjoin(Position).outerjoin(Department).filter(Department.id == department_type)
    else:
        # 未携带任何参数，查询所有
        person_query = Person.query

    my_paginate = person_query.order_by(Person.id.desc()).paginate(page=page_now, per_page=page_size)
    if page_now > 2:
        page_range = range(1, my_paginate.pages + 1)[page_now - 3: page_now + 2]
    else:
        page_range = range(1, my_paginate.pages + 1)[:5]
    d_list = Department.query.all()
    return render_template('person.html', **locals())


# 添加职员
@user_print.route('/add_person', methods=["GET", "POST"])
@login_check
def add_person():
    # data = request.args
    position_list = Position.query.order_by(Position.id).all()
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")
        nickname = data.get("nickname")
        gender = data.get("gender")
        age = data.get("age")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")
        position_id = data.get("position_id")

        photo = request.files.get("photo")
        filename = 'my_photo.jpg'  # 默认头像名称
        if photo:
            filename = change_filename(photo.filename)
            file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static/img',
                                     filename)
            photo.save(file_path)

        # print(file_path)
        person = Person()
        person.username = username
        person.password = encrypt_password(password)
        person.nickname = nickname
        person.gender = gender
        person.age = age
        person.phone = phone
        person.email = email
        person.address = address
        person.photo = filename
        person.position_id = position_id
        person.save()
        return redirect("/person")
    return render_template('add_person.html', **locals())


# 员工详情
@user_print.route('/detail_person/<int:id>')
@login_check
def detail_person(id):
    person = Person.query.get(id)
    return render_template('detail_person.html', **locals())


# 员工信息修改
@user_print.route('/edit_person/<int:id>', methods=["GET", "POST"])
@login_check
def edit_person(id):
    person = Person.query.get(id)
    position_list = Position.query.order_by(Position.id).all()
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")
        nickname = data.get("nickname")
        gender = data.get("gender")
        age = data.get("age")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")
        position_id = data.get("position_id")
        photo = request.files.get("photo")
        if photo:
            filename = change_filename(photo.filename)
            file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static/img',
                                     filename)
            photo.save(file_path)
            person.photo = filename
        person.username = username
        if password != person.password:
            person.password = encrypt_password(password)
        person.nickname = nickname
        person.gender = gender
        person.age = age
        person.phone = phone
        person.email = email
        person.address = address
        person.position_id = position_id
        person.update()
        return redirect('/person')
    return render_template('edit_person.html', **locals())


# 员工删除
@user_print.route('/delete_person/<int:id>')
@login_check
def delete_person(id):
    person = Person.query.get(id)
    person.delete()
    return redirect('/person')


# 部门管理
@user_print.route('/department')
@login_check
def department():
    d_list = Department.query.all()
    return render_template('department.html', **locals())


# 部门添加
@user_print.route('/add_department', methods=["POST", "GET"])
@login_check
def add_department():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        department = Department()
        department.name = name
        department.description = description
        department.save()
        return redirect("/department")
    return render_template('add_department.html', **locals())


# 部门删除
@user_print.route('/delete_department')
@login_check
def delete_department():
    department_id = request.args.get("department_id")
    department = Department.query.get(department_id)
    department.delete()
    return redirect("/department")


# 部门管理
@user_print.route('/edit_department', methods=["GET", "POST"])
@login_check
def edit_department():
    department_id = request.args.get("department_id")
    department = Department.query.get(department_id)
    if request.method == "POST":
        department_id = request.form.get("department_id")
        department = Department.query.get(department_id)
        name = request.form.get("name")
        description = request.form.get("description")
        department.name = name
        department.description = description
        department.update()
        return redirect("department")
    return render_template('edit_department.html', **locals())


# 添加职位
@user_print.route('/position', methods=["POST", "GET"])
@login_check
def position():
    # d_list = Department.query.all()
    if request.method == "GET":
        department_id = request.args.get("department_id")
        department = Department.query.get(department_id)
        position_list = Department.query.get(department_id).department_position_map
    if request.method == "POST":
        department_id = request.form.get("department_id")
        position = Position()
        position.name = request.form.get("name")
        position.level = request.form.get("level")
        position.department_id = request.form.get("department_id")
        position.save()
        return redirect(f"/position?department_id={department_id}")
    return render_template('position.html', **locals())


# 删除职位
@user_print.route('/delete_position')
@login_check
def delete_position():
    position_id = request.args.get("position_id")
    position = Position.query.get(position_id)
    department_id = position.position_department_map.id
    position.delete()
    return redirect(f"/position?department_id={department_id}")


# 部门管理
@user_print.route('/position_permission', methods=["POST", "GET"])
@login_check
def position_permission():
    permission_id = request.args.get("permission_id")
    permission = Permission.query.get(permission_id)
    position_list = Position.query.all()
    if request.method == "POST":
        # 权限添加职位
        new_position_list = request.form.getlist("position_ids")  # 获取表单提交的要授予权限的职位id
        permission_id = request.form.get("permission_id")  # 获取当前要修改的权限的id
        permission = Permission.query.get(permission_id)  # 获取当前要修改的权限的对象
        permission.permission_position_map.clear()  # 清空权限所对应的所有职位数据
        for position_id in new_position_list:
            # 循环遍历要添加权限的职位id
            position = Position.query.get(position_id)  # 根据职位id获取职位对象
            position.position_permission_map.append(permission)
            position.update()
        return redirect("/permission")
    return render_template('position_permission.html', **locals())


# 个人考勤
@user_print.route('/attendance_me', methods=["POST", "GET"])
@login_check
def attendance_me():
    username = session.get("username")
    person = Person.query.filter(Person.username == username).first()
    attendance_list = person.person_attendances_map
    if request.method == "POST":
        reason = request.form.get("reason")
        type = request.form.get("type")
        day = request.form.get("day")
        start = request.form.get("start")
        end = request.form.get("end")
        # 设置
        status = "申请中"  # 默认假条状态都是申请中
        # 新增
        attendance = Attendance()
        attendance.reason = reason
        attendance.type = type
        attendance.day = day
        attendance.start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        attendance.end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        attendance.status = status
        attendance.person_id = person.id
        attendance.save()
        return redirect("/attendance_me")
    return render_template('attendance_me.html', **locals())


# 下属考勤
@user_print.route('/attendance_subordinate')
@login_check
def attendance_subordinate():
    person = Person.query.filter(Person.username == session.get("username")).first()
    attendance_list = Attendance.query.join(Person).join(Position) \
        .filter(Position.position_department_map == person.person_position_map.position_department_map) \
        .filter(Position.level < person.person_position_map.level) \
        .order_by(Attendance.id.desc()) \
        .all()
    return render_template('attendance_subordinate.html', **locals())


# 下属考勤
@user_print.route('/attendance_subordinate_update')
@login_check
def attendance_subordinate_update():
    """下属考勤修改页面"""
    # 获取当前登录用户
    person = Person.query.filter(Person.username == session.get("username")).first()
    # 获取参数
    attendance_id = request.args.get("attendance_id")
    status = request.args.get("status")
    # 查询对象
    attendance = Attendance.query.get(attendance_id)
    # 判断
    if status == "yes":
        attendance.status = "已通过"
    else:
        attendance.status = "已驳回"
    # 修改
    attendance.approver = person.username
    attendance.update()
    # 重定向
    return redirect("attendance_subordinate")


# 权限管理
@user_print.route('/permission')
@login_check
def permission():
    permission_list = Permission.query.all()
    return render_template('permission.html', **locals())


# 新闻
@user_print.route('/news')
@login_check
def news():
    news_list = News.query.all()
    return render_template('news.html', **locals())


# 添加新闻
@user_print.route('/add_news', methods=["POST", "GET"])
@login_check
def add_news():
    if request.method == "POST":
        news = News()
        data = request.form
        title = data.get("title")
        author = data.get("author")
        content = data.get("content")
        picture = request.files.get("picture")
        if picture:
            filename = change_filename(picture.filename)
            file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static/img',
                                     filename)
            picture.save(file_path)
            news.picture = filename
        pubtime = datetime.now()
        news.title = title
        news.author = author
        news.content = content
        news.pubtime = pubtime
        news.save()
        return redirect("/news")
    return render_template('add_news.html', **locals())


# 新闻详情
@user_print.route('/detail_news/<int:id>')
@login_check
def detail_news(id):
    news = News.query.get(id)
    return render_template('detail_news.html', **locals())


# 新闻删除
@user_print.route('/delete_news/<int:id>')
@login_check
def delete_news(id):
    news = News.query.get(id)
    news.delete()
    return redirect('/news')


# 编辑新闻
@user_print.route('/edit_news/<int:id>', methods=["POST", "GET"])
@login_check
def edit_news(id):
    news = News.query.get(id)
    if request.method == "POST":
        data = request.form
        title = data.get("title")
        author = data.get("author")
        content = data.get("content")
        picture = request.files.get("picture")
        if picture:
            filename = change_filename(picture.filename)
            file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static/img',
                                     filename)
            picture.save(file_path)
            news.picture = filename
        pubtime = datetime.now()
        news.title = title
        news.author = author
        news.content = content
        news.pubtime = pubtime
        news.update()
        return redirect("/news")
    return render_template("edit_news.html", **locals())


# 登录
@user_print.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")
        user = Person.query.filter(Person.username == username).first()
        if user:
            if user.password == encrypt_password(password):
                response = redirect('/')
                response.set_cookie("username", username)
                response.set_cookie("user_id", str(user.id))
                session["username"] = username
                return response
    return render_template('login.html', **locals())


# 退出
@user_print.route('/logout')
def logout():
    response = redirect("/login")
    response.delete_cookie("username")
    response.delete_cookie("user_id")
    session.pop('username')
    return response


# session设置
@user_print.route('/session')
def set_session():
    session["username"] = "laowang"
    return "set_session"


# session设置
@user_print.route('/get_session')
def get_session():
    s = session.get('username')
    print(s)
    return "get_session"


# session设置
@user_print.route('/delete_session')
def delete_session():
    session.pop('username')
    return "delete_session"


from .forms import RegisterForm


# 后端验证
@user_print.route('/register', methods=["GET", "POST"])
def register():
    my_form = RegisterForm()
    if request.method == "POST":
        if my_form.validate_on_submit():
            print("注册成功！")
        else:
            print(my_form.username.errors)  # ['邮箱']
            print(my_form.errors)  # {'username': ['邮箱'], 'repassword': ['密码不一致']}
    return render_template("register.html", **locals())


@csrf.exempt
@user_print.route('/aaa', methods=["POST"])
def aaa():
    return "aaa"


@user_print.route('/echar')
def echar():
    return render_template("echar.html")


@user_print.route('/show')
def show():
    """
    首页统计表格渲染
    """
    data = Department.query.outerjoin(Position).outerjoin(Person).group_by(Department.name) \
        .with_entities(Department.name, func.count(Person.id)).all()
    datas = dict(data)
    # department_list = Department.query.all()
    # datas = {}
    # for department in department_list:
    #     count = 0  # 部门人员统计
    #     position_list = department.department_position_map
    #     for position in position_list:
    #         person_list = position.position_person_map
    #         count += len(person_list)
    #         datas[department.name] = count
    datas = {
        "x": list(datas.keys()),
        "y": list(datas.values())
    }
    return jsonify(datas)

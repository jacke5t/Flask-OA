from BluePrint import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Person(Base):
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    nickname = db.Column(db.String(100))
    gender = db.Column(db.String(32), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    wordid = db.Column(db.String(32), nullable=True)
    phone = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    photo = db.Column(db.String(64), nullable=True)
    address = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)
    position_id = db.Column(db.Integer, db.ForeignKey("position.id"))

    person_attendances_map = db.relationship(
        "Attendance",
        backref='attendance_person_map',
        cascade="all,delete-orphan"
    )


class Position(Base):
    name = db.Column(db.String(32))
    level = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    # 根据职位信息查询所对应的权限信息
    position_permission_map = db.relationship(
        "Permission",
        secondary='position_permission',
        backref='permission_position_map'
    )
    # 根据职位查询所对应的员工对象
    position_person_map = db.relationship(
        "Person",
        backref="person_position_map",
        cascade="all,delete-orphan"
    )


class Department(Base):
    name = db.Column(db.String(32))
    description = db.Column(db.Text)
    # 创建关系映射d_position提供给department表快速查询每个部门中的所有职位对象
    department_position_map = db.relationship(
        "Position",
        backref="position_department_map",  # 提供给职位表查询每个职位所属的部门对象
        cascade="all,delete-orphan"
    )


class Permission(Base):
    name = db.Column(db.String(32))
    description = db.Column(db.Text)


position_permission = db.Table(
    "position_permission",  # 中间表表名
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id")),
    db.Column("position_id", db.Integer, db.ForeignKey("position.id"))
)


class Attendance(Base):
    reason = db.Column(db.TEXT)
    type = db.Column(db.String(32))
    day = db.Column(db.Float)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    approver = db.Column(db.String(32))
    status = db.Column(db.String(32))
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))


class News(Base):
    """新闻表"""
    title = db.Column(db.String(32))  # 标题
    author = db.Column(db.String(32))  # 作者
    content = db.Column(db.Text)  # 内容
    pubtime = db.Column(db.DateTime)  # 发表日期
    picture = db.Column(db.String(128), nullable=True)  # 图片 可以为空

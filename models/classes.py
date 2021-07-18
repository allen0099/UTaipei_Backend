from app import db
from .collection import Collection


class Classes(db.Model):
    __tablename__: str = "classes"

    id = db.Column(db.String, primary_key=True)

    _degree = db.Column(db.String)
    _department = db.Column(db.String)
    _unit = db.Column(db.String)
    _class_year = db.Column(db.String)
    _class_type = db.Column(db.String)
    chinese_name = db.Column(db.String)
    english_name = db.Column(db.String)
    category = db.Column(db.String)
    class_name = db.Column(db.String)
    points = db.Column(db.String)
    full_half = db.Column(db.String)
    req_select = db.Column(db.String)
    hours = db.Column(db.String)

    enrolled_max = db.Column(db.String)
    enrolled_min = db.Column(db.String)
    enrolled_current = db.Column(db.String)

    campus = db.Column(db.String)

    syllabus = db.Column(db.String)

    notes = db.Column(db.String)
    limit = db.Column(db.Boolean)

    teachers = db.relationship('Teachers', backref='class_', lazy=True, cascade="all, delete-orphan")
    times = db.relationship('Timetable', backref='class_', lazy=True, cascade="all, delete-orphan")

    def __init__(self, sc: Collection, degree, department, unit, cls_year):
        self.id = sc.course_code

        self._degree = degree
        self._department = department
        self._unit = unit
        self._class_year = cls_year

        self._class_type = RevCategory[sc.category]

        self.chinese_name = sc.chinese_name
        self.english_name = sc.english_name
        self.category = sc.category
        self.class_name = sc.class_name
        self.points = sc.credit
        self.full_half = sc.full_half
        self.req_select = sc.req_select
        self.hours = sc.lecturing_hours

        self.enrolled_max = sc.enrolled_max
        self.enrolled_min = sc.enrolled_min
        self.enrolled_current = sc.enrolled_current

        self.campus = sc.campus

        self.syllabus = sc.syllabus

        self.notes = sc.notes
        self.limit = sc.limit

    def __repr__(self):
        return f"{self.id}"


Category = {
    "%": "所有類別",
    "a1": "校定必修",
    "a2": "共同必修",
    "a3": "校定必修(學科)",
    "a7": "院定必修",
    "aa": "國文類",
    "ab": "英文類",
    "ac": "體育類",
    "ad": "軍訓類",
    "ae": "服務學習類",
    "b1": "系定必修",
    "b2": "系定必修(學科)",
    "b3": "系定必修(術科)",
    "b4": "系定選修",
    "b5": "系定選修(學科)",
    "b6": "系定選修(術科)",
    "b7": "專長(水陸球技藝)",
    "b8": "選修專長(水陸球技藝)",
    "b9": "學科",
    "ba": "術科",
    "Bc": "共同選修",
    "BN": "藝術與美感領域",
    "BO": "人文與文化思考領域",
    "BP": "公民素養與社會探索領域",
    "BQ": "自然、生命與科技領域",
    "c1": "分組必修",
    "C1": "學科",
    "c2": "分組必修(學科)",
    "c3": "分組必修(術科)",
    "c4": "分組選修",
    "c5": "分組選修(學科)",
    "c6": "分組選修(術科)",
    "E1": "專長(水陸球技藝)",
    "j1": "教學基本學科課程",
    "j2": "教育基礎課程",
    "j3": "教育方法課程",
    "j4": "教材教法及教學實習課程",
    "j5": "選修課程",
    "k2": "教育基礎課程",
    "k3": "教育方法課程",
    "k6": "教保專業知能課程",
    "l0": "特殊教育專業課程",
    "l3": "一般教育專業課程(中等學校教育階段)",
    "l9": "特殊需求與領域調整課程",
}
RevCategory = {
    v: k for k, v in Category.items()
}

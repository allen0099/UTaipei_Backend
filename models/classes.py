from app import db
from .collection import Collection


class Classes(db.Model):
    __tablename__: str = "classes"

    id = db.Column(db.String, primary_key=True)
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

    def __init__(self, sc: Collection):
        self.id = sc.course_code
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

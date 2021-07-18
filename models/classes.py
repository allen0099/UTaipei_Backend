from app import db


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
    teacher = db.Column(db.String)

    syllabus = db.Column(db.String)

    notes = db.Column(db.String)
    limit = db.Column(db.String)

    times = db.relationship('Timetable', backref='class_', lazy=True, cascade="all, delete-orphan")

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f"{self.id}"

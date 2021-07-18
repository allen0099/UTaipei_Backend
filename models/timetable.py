from app import db


class Timetable(db.Model):
    __tablename__: str = "timetable"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.String, db.ForeignKey('classes.id'), nullable=False)
    weekday = db.Column(db.String)
    time = db.Column(db.String)

    def __init__(self, id, weekday, time):
        self.class_id = id
        self.weekday = weekday
        self.time = time

    def __repr__(self):
        return f"{self.class_id} -> {self.weekday}{self.time}"

from app import db


class Teachers(db.Model):
    __tablename__: str = "teachers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.String, db.ForeignKey('classes.id'), nullable=False)
    name = db.Column(db.String)

    def __init__(self, id, name):
        self.class_id = id
        self.name = name

    def __repr__(self):
        return f"{self.class_id} -> {self.name}"

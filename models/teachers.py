from app import db
from .mixin import Serializer


class Teachers(db.Model, Serializer):
    __tablename__: str = "teachers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.String, db.ForeignKey('classes.id'), nullable=False)
    name = db.Column(db.String)

    def serialize(self):
        d = Serializer.serialize(self)
        del d['id']
        del d['class_id']
        return d

    def __init__(self, id, name):
        self.class_id = id
        self.name = name

    def __repr__(self):
        return f"{self.class_id}: {self.name}"

from app import db


class Config(db.Model):
    __tablename__: str = "config"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"{self.key} -> {self.value}\n"

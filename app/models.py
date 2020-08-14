from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(120), index=True, nullable=False)
    birth_date = db.Column(db.String(120), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<User {}>".format(self.id)

    def form(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "zip_code": self.zip_code,
        }

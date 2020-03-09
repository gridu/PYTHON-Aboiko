from application import db


class Access_Request(db.Model):
    __tablename__ = "access_request"
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

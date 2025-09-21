from models import db

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Habit {self.name}>'
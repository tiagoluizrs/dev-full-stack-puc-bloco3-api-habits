from models import db

class State(db.Model):
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    cities = db.relationship('City', back_populates='state')

    def __repr__(self):
        return f'<State {self.name}>'
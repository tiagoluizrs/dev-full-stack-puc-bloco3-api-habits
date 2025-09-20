from models import db

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    state = db.relationship('State', back_populates='cities')

    def __repr__(self):
        return f'<City {self.name}>'
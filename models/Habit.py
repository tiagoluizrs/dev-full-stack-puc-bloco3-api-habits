from models import db

from enum import Enum

class CategoryEnum(Enum):
    transporte = "transporte"
    energia = "energia"
    alimentacao = "alimentacao"

class FrequencyEnum(Enum):
    diario = "diario"
    semanal = "semanal"
    mensal = "mensal"

class UnitEnum(Enum):
    km = "km"
    kwh_economizados = "kwh_economizados"
    refeicoes = "refeicoes"

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Enum(CategoryEnum), nullable=False)
    frequency = db.Column(db.Enum(FrequencyEnum), nullable=False)
    quantity = db.Column(db.Enum(UnitEnum), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    def __repr__(self):
        return f'<Habit {self.name}>'
from models import db
from models.Habit import Habit
import requests
import os
from datetime import datetime, timedelta

def create_habit(data):
    name = data.get('name')
    id_user = data.get('id_user')
    frequency = data.get('frequency')
    quantity = data.get('quantity')
    start_date = data.get('start_date')
    location = data.get('location')

    if not all([name, id_user, frequency, quantity, start_date, location]):
        return {'error': 'Missing fields'}, 400

    habit = Habit(
        name=name,
        id_user=id_user,
        frequency=frequency,
        quantity=quantity,
        start_date=start_date,
        location=location
    )
    db.session.add(habit)
    db.session.commit()
    return {'message': 'Habit created successfully', 'id': habit.id}, 201

def delete_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if not habit:
        return {'error': 'Habit not found'}, 404
    db.session.delete(habit)
    db.session.commit()
    return {'message': 'Habit deleted successfully'}, 200

def update_habit(habit_id, data):
    habit = Habit.query.get(habit_id)
    if not habit:
        return {'error': 'Habit not found'}, 404
    for field in ['name', 'id_user', 'frequency', 'quantity', 'start_date', 'location']:
        if field in data:
            value = data[field]
            setattr(habit, field, value)
    db.session.commit()
    return {'message': 'Habit updated successfully'}, 200

def list_habits(id_user):
    habits = Habit.query.filter_by(id_user=id_user).all()
    result = []
    for habit in habits:
        result.append({
            'id': habit.id,
            'name': habit.name,
            'id_user': habit.id_user,
            'frequency': habit.frequency,
            'quantity': habit.quantity,
            'start_date': str(habit.start_date),
            'location': habit.location
        })
    return result, 200

def get_habit_by_id(habit_id):
    habit = Habit.query.get(habit_id)
    if not habit:
        return {'error': 'Habit not found'}, 404
    result = {
        'id': habit.id,
        'name': habit.name,
        'id_user': habit.id_user,
        'frequency': habit.frequency,
        'quantity': habit.quantity,
        'start_date': str(habit.start_date),
        'location': habit.location
    }
    return result, 200

def getHabitRankingEnergy(user_id, params):
    query = Habit.query.filter_by(id_user=user_id)
    start_date_param = params.get('start_date')
    end_date_param = params.get('end_date')
    if start_date_param and end_date_param:
        query = query.filter(Habit.start_date >= start_date_param, Habit.start_date <= end_date_param)
    habits = query.all()
    labels = []
    dataCo2 = []
    today = datetime.today().date()
    for h in habits:
        if not h.start_date:
            continue  # ignora hábitos sem data de início
        start_date = h.start_date if isinstance(h.start_date, datetime) else datetime.strptime(str(h.start_date), '%Y-%m-%d').date()
        end_date = getattr(h, 'end_date', None)
        if not end_date:
            end_date = today
        else:
            end_date = end_date if isinstance(end_date, datetime) else datetime.strptime(str(end_date), '%Y-%m-%d').date()
        quantity = h.quantity if h.quantity is not None else 0
        freq = getattr(h, 'frequency', '').lower()
        total = 0
        if freq == 'diário':
            days = (end_date - start_date).days + 1
            total = quantity * days
        elif freq == 'semanal':
            weeks = ((end_date - start_date).days // 7) + 1
            total = quantity * weeks
        elif freq == 'mensal':
            months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1
            total = quantity * months
        else:
            total = quantity
        co2 = estimate_electricity_emission(total)
        labels.append(h.name)
        dataCo2.append(co2)
    return {
        "labels": labels,
        "data": dataCo2
    }

def getEnergyEconomic(user_id, params):
    query = Habit.query.filter_by(id_user=user_id)
    start_date_param = params.get('start_date')
    end_date_param = params.get('end_date')
    if start_date_param and end_date_param:
        query = query.filter(Habit.start_date >= start_date_param, Habit.start_date <= end_date_param)
    habits = query.all()
    today = datetime.today().date()
    total_quantity = 0
    for h in habits:
        if not h.start_date:
            continue
        start_date = h.start_date if isinstance(h.start_date, datetime) else datetime.strptime(str(h.start_date), '%Y-%m-%d').date()
        end_date = getattr(h, 'end_date', None)
        if not end_date:
            end_date = today
        else:
            end_date = end_date if isinstance(end_date, datetime) else datetime.strptime(str(end_date), '%Y-%m-%d').date()
        quantity = h.quantity if h.quantity is not None else 0
        freq = getattr(h, 'frequency', '').lower()
        total = 0
        if freq == 'diário':
            days = (end_date - start_date).days + 1
            total = quantity * days
        elif freq == 'semanal':
            weeks = ((end_date - start_date).days // 7) + 1
            total = quantity * weeks
        elif freq == 'mensal':
            months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1
            total = quantity * months
        else:
            total = quantity
        total_quantity += total
    co2 = estimate_electricity_emission(total_quantity)
    return co2

def dashboard_habits(user_id, params):
    return [{
        "economy_on_period": {
            "labels": ['Carbono não emitido (CO₂ em Kg)'],
            "data": [getEnergyEconomic(user_id, params)]
        },
        "energy_habit_ranking_on_period": getHabitRankingEnergy(user_id, params)
    }, 200]

def estimate_electricity_emission(energy):
    api_key = os.getenv('CLIMATE_API_KEY')
    url = 'https://api.climatiq.io/data/v1/estimate'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        "emission_factor": {
            "activity_id": "electricity-supply_grid-source_residual_mix",
            "data_version": "^21"
        },
        "parameters": {
            "energy": energy,
            "energy_unit": "kWh"
        }
    }
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    result = response.json()
    return result.get('co2e', 0)
from models import db
from models.Habit import Habit

def create_habit(data):
    name = data.get('name')
    id_user = data.get('id_user')
    category = data.get('category')
    frequency = data.get('frequency')
    quantity = data.get('quantity')
    unit = data.get('unit')
    start_date = data.get('start_date')
    location = data.get('location')

    if not all([name, id_user, category, frequency, quantity, unit, start_date, location]):
        return {'error': 'Missing fields'}, 400

    habit = Habit(
        name=name,
        id_user=id_user,
        category=category,
        frequency=frequency,
        quantity=quantity,
        unit=unit,
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
    for field in ['name', 'id_user', 'category', 'frequency', 'quantity', 'unit', 'start_date', 'location']:
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
            'category': habit.category,
            'frequency': habit.frequency,
            'quantity': habit.quantity,
            'unit': habit.unit,
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
        'category': habit.category,
        'frequency': habit.frequency,
        'quantity': habit.quantity,
        'unit': habit.unit,
        'start_date': str(habit.start_date),
        'location': habit.location
    }
    return result, 200

def dashboard_habits(user_id):
    return [{
        "user_id": user_id,
    }, 200]
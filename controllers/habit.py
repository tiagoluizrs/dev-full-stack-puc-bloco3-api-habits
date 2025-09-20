from models import db
from models.Habit import Habit, CategoryEnum, FrequencyEnum, UnitEnum
from models.City import City

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

    if category not in [e.value for e in CategoryEnum]:
        return {'error': 'Invalid category'}, 400
    if frequency not in [e.value for e in FrequencyEnum]:
        return {'error': 'Invalid frequency'}, 400
    if unit not in [e.value for e in UnitEnum]:
        return {'error': 'Invalid unit'}, 400

    city = City.query.get(location)
    if not city:
        return {'error': 'City not found'}, 404

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
            if field == 'category' and value not in [e.value for e in CategoryEnum]:
                return {'error': 'Invalid category'}, 400
            if field == 'frequency' and value not in [e.value for e in FrequencyEnum]:
                return {'error': 'Invalid frequency'}, 400
            if field == 'unit' and value not in [e.value for e in UnitEnum]:
                return {'error': 'Invalid unit'}, 400
            if field == 'location':
                city = City.query.get(value)
                if not city:
                    return {'error': 'City not found'}, 404
            setattr(habit, field, value)
    db.session.commit()
    return {'message': 'Habit updated successfully'}, 200

def list_habits():
    habits = Habit.query.all()
    result = []
    for habit in habits:
        result.append({
            'id': habit.id,
            'name': habit.name,
            'id_user': habit.id_user,
            'category': habit.category,
            'category_name': habit.category_name,
            'frequency': habit.frequency,
            'frequency_name': habit.frequency_name,
            'quantity': habit.quantity,
            'unit': habit.unit,
            'unit_name': habit.unit_name,
            'start_date': str(habit.start_date),
            'location': habit.location,
            'city_name': habit.city.name if habit.city else None
        })
    return {'habits': result}, 200

def get_habit_by_id(habit_id):
    habit = Habit.query.get(habit_id)
    if not habit:
        return {'error': 'Habit not found'}, 404
    result = {
        'id': habit.id,
        'name': habit.name,
        'id_user': habit.id_user,
        'category': habit.category,
        'category_name': habit.category_name,
        'frequency': habit.frequency,
        'frequency_name': habit.frequency_name,
        'quantity': habit.quantity,
        'unit': habit.unit,
        'unit_name': habit.unit_name,
        'start_date': str(habit.start_date),
        'location': habit.location,
        'city_name': habit.city.name if habit.city else None
    }
    return result, 200

def dashboard_habits(user_id):
    return [{
        "user_id": user_id,
    }, 200]
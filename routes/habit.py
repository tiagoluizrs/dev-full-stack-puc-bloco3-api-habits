import requests
from flask import request, jsonify, g
from functools import wraps
from controllers.habit import get_habit_by_id, list_habits, create_habit, delete_habit, update_habit, dashboard_habits
import os

AUTH_SERVICE_HOST = os.getenv('AUTH_SERVICE_HOST', 'http://api-auth:5002')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
        token = auth_header.split(' ')[1]
        try:
            resp = requests.post(f'{AUTH_SERVICE_HOST}/auth/validate-token', json={'token': token}, timeout=5)
            if resp.status_code != 200 or not resp.json().get('user_id'):
                return jsonify({'error': 'Invalid or expired token'}), 401
            g.user_id = resp.json()['user_id']
        except Exception:
            return jsonify({'error': 'Auth service unavailable'}), 503
        return f(*args, **kwargs)
    return decorated

def register_habit_routes(app):
    @app.route('/habits', methods=['GET'])
    @token_required
    def habits_list():
        result, status = list_habits(getattr(g, 'user_id', None))
        return jsonify(result), status

    @app.route('/habits/<int:habit_id>', methods=['GET'])
    @token_required
    def habit_get(habit_id):
        result, status = get_habit_by_id(habit_id)
        return jsonify(result), status

    @app.route('/habits', methods=['POST'])
    @token_required
    def habit_create():
        data = request.get_json()
        result, status = create_habit({**data, 'id_user': getattr(g, 'user_id', None)})
        return jsonify(result), status

    @app.route('/habits/<int:habit_id>', methods=['PUT'])
    @token_required
    def habit_update(habit_id):
        data = request.get_json()
        result, status = update_habit(habit_id, data)
        return jsonify(result), status

    @app.route('/habits/<int:habit_id>', methods=['DELETE'])
    @token_required
    def habit_delete(habit_id):
        result, status = delete_habit(habit_id)
        return jsonify(result), status

    @app.route('/habits/dashboard', methods=['GET'])
    @token_required
    def habit_dashboard():
        user_id = getattr(g, 'user_id', None)
        params = request.args
        if not user_id:
            return jsonify({'error': 'User ID not found'}), 400
        result, status = dashboard_habits(user_id, params)
        return jsonify(result), status
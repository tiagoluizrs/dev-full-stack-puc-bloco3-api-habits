from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

def register_routes(app):
    from routes.habit import register_habit_routes
    register_habit_routes(app)

register_routes(app)

if __name__ == '__main__':
    app.run()

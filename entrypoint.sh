#!/bin/sh
flask db init
flask db migrate -m "Auto migration"
flask db upgrade
exec flask run --host=0.0.0.0 --port=5003
#################
# if want to init or modify the database
# 1.modify your model.py
# 2.in cmd (python manage.py db migrate -m "script") (if init enter (python manage.py db init) first)
# 3.in cmd (python manage.py db upgrade)
# 4. your database change success
#################

from app import app
from flask_migrate import MigrateCommand
from flask_script import Manager

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

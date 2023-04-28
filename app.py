from appsample import create_app
import os


# if it needs test change controller to test
blueprints = ['appsample.controller.main:main',
              'appsample.controller.auth:auth',
              'appsample.controller.role:role',
              'appsample.controller.user:user']
# if need test change development to testing
app = create_app(os.getenv('FLASK_CONFIG') or 'development', blueprints)

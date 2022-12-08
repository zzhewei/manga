from gevent import monkey
# monkey.patch_all()  # 異步 基於greenlet
# import eventlet.wsgi
from gevent import pywsgi
from appsample import create_app
import os


# if need test change controller to test
blueprints = ['appsample.controller.main:main',
              'appsample.controller.auth:auth',
              'appsample.controller.role:role',
              'appsample.controller.user:user']
# if need test change development to testing
app = create_app(os.getenv('FLASK_CONFIG') or 'development', blueprints)


if __name__ == '__main__':
    # server = pywsgi.WSGIServer(('0.0.0.0', 9898), app)  # 需使用支持 gevent 的 WSGI
    # server.serve_forever()
    app.run(host="0.0.0.0", debug=True)
    # eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 9898)), app)

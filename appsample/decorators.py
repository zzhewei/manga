###############################
# reference:https://medium.com/citycoddee/python%E9%80%B2%E9%9A%8E%E6%8A%80%E5%B7%A7-3-%E7%A5%9E%E5%A5%87%E5%8F%88%E7%BE%8E%E5%A5%BD%E7%9A%84-decorator-%E5%97%B7%E5%97%9A-6559edc87bc0
#           https://blog.csdn.net/weixin_42817311/article/details/107875619
#           https://medium.com/tsungs-blog/python-%E4%BD%9C%E7%94%A8%E5%9F%9F%E8%88%87closure-%E9%96%89%E5%8C%85-18426536e25c
###############################

from functools import wraps

from flask import abort
from flask_login import current_user

from .model import Permission


def permission_required(permission):
    # Closure
    def decorator(f):
        # just show correct f.__name__ and f.__doc__
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

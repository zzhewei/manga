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


"""
@permission_required(permission)
def test():
    pass

等同於

def test():
    pass
test = permission_required(permission)(test)

由左至右 先處理permission_required(permission) 返回decorator是一个函數
所以變成 test = decorator(test), permission變成captured variable(Closure的觀念)
之後又返回 decorated_function 所以test = decorated_function test也變成captured variable
最後在decorated_function內部才可以比對permission 跟返回f(*args, **kwargs)



def print_func_name(func):
    def wrap():
        print("Now use function '{}'".format(func.__name__))
        func()
    return wrap


def dog_bark():
    print("Bark !!!")


def cat_miaow():
    print("Miaow ~~~")


if __name__ == "__main__":
    print_func_name(dog_bark)()
    # > Now use function 'dog_bark'
    # > Bark !!!

    print_func_name(cat_miaow)()
    # > Now use function 'cat_miaow'
    # > Miaow ~~~
print_func_name(dog_bark) 和 print_func_name(cat_miaow) 只會 return function 本身，所以要在後面加上 () 來 call function
"""

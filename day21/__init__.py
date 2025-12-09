from flask import Flask, request, session, redirect, template_rendered


def auth():

    if request.path.startswith('/static'):
        # 继续向后执行不拦截
        return

    #print("拦截器")
    if request.path == '/login':
        # 继续向后执行
        return

    user_info = session.get('user_info')
    if user_info:
        # 继续向后不拦截
        return

    return  redirect('/login')

def get_real_name():
    user_info = session.get('user_info')
    real_name = user_info['real_name']
    return real_name

def create_app():
    app = Flask(__name__)
    app.secret_key = 'asdijaod'

    from .views import account
    from .views import order
    app.register_blueprint(account.ac)
    app.register_blueprint(order.od)
    app.template_global()(get_real_name)

    app.before_request(auth)

    return app
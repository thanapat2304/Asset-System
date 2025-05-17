from flask import session, redirect, url_for, request , make_response
from backend.db_connection import connect_aep_portal

users = [
    {
        'username': 'admin',
        'password': 'admin1',
        'user_name': 'Thanapurt'
    }
]

def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('index', error=1))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return redirect(url_for('index', error="กรุณากรอกข้อมูลให้ครบถ้วน"))

    for user in users:
        if user['username'] == username and user['password'] == password:
            session['username'] = user['username']
            session['user_name'] = user['user_name']
            session.permanent = True

            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('index', error="รหัสผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"))
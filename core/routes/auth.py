from flask import Blueprint, redirect, url_for, request, flash, render_template
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from ..models import User
from ..extensions import db
from ..functions import validate_password, validate_email, validate_username

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('main.index'))
    
'''
Login routes
'''

@auth.route('/login/', methods=['GET'])
def login_get():
    if not current_user.is_authenticated:
        context = {
            'title': 'Login | My Fitness Cat',
        }
        return render_template(
            'auth/login.html',
            **context
        )
    else:
        return redirect(url_for('main.index'))

@auth.route('/login/', methods=['POST'])
def login():
    if not current_user.is_authenticated:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password_hash, password):
            flash('Invalid username or password')
            return 'Invalid username or password'
        else:
            login_user(user, remember=True)
            return 'User logged in'
    else: 
        return 'Already Logged in'

'''
register routes
'''

@auth.route('/register/', methods=['GET'])
def register_get():
    if not current_user.is_authenticated:
        context = {
            'title': 'Register | My Fitness Cat'
        }

        return render_template(
            'auth/register.html',
            **context
        )
    else:
        return redirect(url_for('main.index'))
    
@auth.route('/register/', methods=['POST'])
def register():
    if not current_user.is_authenticated:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        first_name = request.form.get('f_name')
        last_name = request.form.get('l_name')

        # validation
        if not validate_password(password):
            return 'Invalid password.'
        elif not validate_email(email):
            return 'Invalid email.'
        elif not validate_username(username):
            return 'Invalid username.'
        else: 
            password_hash = generate_password_hash(password, method='sha256')

        user = User(
            username=username,
            password_hash=password_hash,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(user)
        db.session.commit()

        return 'User added'
    else:
        return 'Already Logged in'

'''
Logout routes
'''
    
@auth.route('/logout/')
def logout():
    if not current_user.is_authenticated:
        return 'You must be logged in'
    else:
        logout_user()
        return redirect(url_for('auth.login'))
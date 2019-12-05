from app import app
from flask import request, jsonify, render_template
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Objects, HistoryUser


@app.route('/registration', methods=['POST'])
def user_register():
    try:
        json = request.get_json()
        User().create_user(json['email'], json['password'])
        return jsonify('200')
    except Exception as err:
        return jsonify(err)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify('200')


@app.route('/login', methods=['POST'])
def login():
    json = request.get_json()
    email = json['email']
    password = json['password']
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(user.password, password):
        return 'False'
    login_user(user)
    #после входа отправляем информацию о пользователе
    # добавить возврашение истории
    return jsonify(id=user.id,
                   email=user.email,
                   balance=user.balance)


@app.route('/replenish', methods=['POST'])
def replenish_balance():
    json = request.get_json()
    email = json['email']
    value = float(json['value'])
    user = User.query.filter_by(email=email).first()
    if user is None:
        return 'False'
    User().update_balance(email, value)
    return jsonify('200')


@app.route('/call', methods=['POST'])
def create_object():
    json = request.get_json()
    name = json['name']
    input_phone = json['input']
    output_phone = json['output']
    email = json['email']
    comment = json['comment']
    user = User.query.filter_by(email=email).first()
    if user is None:
        return 'False'
    Objects().create_object(user.id, input_phone, output_phone, name, comment)
    return jsonify('200')

@app.route('/history', methods=['POST'])
def get_history():
    json = request.get_json()
    email = json['email']
    user = User.query.filter_by(email=email).first()
    if user is None:
        return 'False'


from app import app
from flask import request, jsonify, render_template, json
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Objects, HistoryUser


@app.route('/registration', methods=['POST'])
def user_register():
    try:
        email = request.values.get('email')
        password = request.values.get('password')
        if User.query.filter_by(email=email).first():
            response = jsonify({'response': 'user exist'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 300
        User().create_user(email, password)
        response = jsonify({'some': 'data'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
    except Exception as err:
        return jsonify(err)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify('200')


@app.route('/login', methods=['POST'])
def login():
    email = request.values.get('email')
    password = request.values.get('password')
    user = User.query.filter_by(email='asd@mail.ru').first()
    if not user or not user.check_password(user.password, password):
        print('bad')
        return jsonify({'response': 'None'}), 301
    login_user(user)
    print(current_user.id)
    #после входа отправляем информацию о пользователе
    # добавить возврашение истории
    response = jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


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
    name = request.values.get('name')
    input_phone = request.values.get('input')
    output_phone = request.values.get('output')
    comment = request.values.get('comment')
    print(current_user)
    if current_user.is_authenticated:
        id = current_user.get_id()
        print(id)
    Objects().create_object(17, input_phone, output_phone, name, comment)
    response = jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


@app.route('/objects', methods=['POST'])
def get_objects():
    print(request.values.get('load'))
    objects = Objects.query.filter_by(uid=17)
    result = []
    for obj in objects:
        row = obj.__dict__
        result.append(row)
    print(result)
    response = jsonify({'response': result})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

@app.route('/history', methods=['POST'])
def get_history():
    json = request.get_json()
    email = json['email']
    user = User.query.filter_by(email=email).first()
    if user is None:
        return 'False'


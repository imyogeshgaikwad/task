from flask import Blueprint, jsonify, request
from models import db, User, Task
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Blueprint('app', __name__)
jwt = JWTManager()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    status = request.args.get('status')
    sort_by = request.args.get('sort', 'id')

    query = Task.query
    if status:
        query = query.filter_by(status=status)
    
    tasks = query.order_by(getattr(Task, sort_by)).all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'name' not in data or 'status' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    new_task = Task(name=data['name'], status=data['status'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get_or_404(task_id)
    
    if 'name' in data:
        task.name = data['name']
    if 'status' in data:
        task.status = data['status']
    
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

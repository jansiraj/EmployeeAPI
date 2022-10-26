import json
from flask import Blueprint, request, jsonify, abort, make_response
from models import Employee
from __init__ import db


employee = Blueprint('employee', __name__)
BAD_REQUEST = 'Bad request'

@employee.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': BAD_REQUEST}), 400)

@employee.route('/createEmployee', methods=['POST'])
def create_employee():
    employee_data = request.get_json()
    name = employee_data.get('name')
    email = employee_data.get('email')
    age = employee_data.get('age')
    employee_id = employee_data.get('employee_id')
    position = employee_data.get('position')
    exists_email = Employee.query.filter_by(email=email).first()
    exists_employee_id = Employee.query.filter_by(employee_id=employee_id).first()
    if type(employee_id) is not int or type(age) is not int or type(name) is not str:
        abort(400)
    if not name or not email or not age or not employee_id or not position:
        abort(400)
    if exists_email or exists_employee_id:
        return jsonify({'message': 'Employee already exists'}), 200
    new_employee = Employee(employee_id, email, name, age, position)
    new_employee.email = email
    new_employee.employee_id = employee_id
    new_employee.name = name
    new_employee.age = age
    new_employee.position = position
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee details created Successfully', 'created_data': str(employee_data)}), 201

@employee.route('/getEmployee/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    emp_obj = Employee.query.filter_by(employee_id=employee_id).first()
    if not emp_obj:
        abort(400)
    employee_dict = {'id': emp_obj.id, 'name': emp_obj.name, 'email': emp_obj.email,
                'employee_id': emp_obj.employee_id, 'age': emp_obj.age, 
                'position': emp_obj.position}

    return jsonify({'message': 'Successfully fetched Employee detail', 
        'employee_details': employee_dict}), 200

@employee.route('/getEmployeesAll', methods=['GET']) 
def get_all_employees():
    employees = Employee.query.all()
    employee_detail_list = []

    for emp_obj in employees:
        employee_dict = {'id': emp_obj.id, 'name': emp_obj.name, 'email': emp_obj.email,
                    'employee_id': emp_obj.employee_id, 'age': emp_obj.age, 
                    'position': emp_obj.position}

        employee_detail_list.append(employee_dict)

    return jsonify({'message': 'Successfully fetched all Employee details', 
        'employee_details': employee_detail_list})


@employee.route('/updateEmployee/<int:employee_id>', methods=['PATCH'])
def update_employee(employee_id):
    patched_data = request.get_json()
    name = patched_data.get('name')
    email = patched_data.get('email')
    age = patched_data.get('age')
    position = patched_data.get('position')
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    if not employee:
        return jsonify({'message': 'Employee not Found'}), 200
    else:
        if name:
            if type(name) is not str:
                abort(400)
            employee.name = name
        if age:
            if type(age) is not int:
                abort(400)
            employee.age = age
        if position:
            if type(age) is not int:
                abort(400)
            employee.position = position
        db.session.commit()
        return jsonify({'message': 'Employee details updated Successfully'}), 200


@employee.route('/deleteEmployee/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    if not employee:
        abort(400)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted Successfully'}), 200


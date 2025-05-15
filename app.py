import json
import pydash as _
from datetime import datetime
import pytz

from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dev:dev@localhost:5432/flask_db"
db = SQLAlchemy(app)

from models.employees import Employees

@app.route("/")
def hello_world():
  return Response("Hello World!")

@app.route("/employees/add", methods=['POST'])
def add_employee():
  request_data = json.loads(request.data)
  employee = Employees(
    name=request_data["name"],
    age=request_data["age"],
    email=request_data["email"]
  )

  db.session.add(employee)
  db.session.commit()

  return {
    "message": "success",
    "data": employee.as_dict()
  }

@app.route("/employees/delete/<employee_name>", methods=['DELETE'])
def delete_employee(employee_name):
  employee = db.session.query(Employees).filter_by(name=employee_name).one_or_none()

  if employee is None:
    return Response(f"employee {employee_name} not found.", status=422)

  db.session.delete(employee)
  db.session.commit()

  return Response(status=204, mimetype='application/json')

@app.route("/employees/get", methods=['GET'])
def get_all_employees():
  employees = db.session.query(Employees).all()
  employees_arr = [e.as_dict() for e in employees]

  return employees_arr

@app.route("/employees/update/<employee_id>", methods=['PATCH'])
def update_employee(employee_id):
  employee = db.session.query(Employees).filter_by(id=employee_id).one_or_none()

  if employee is None:
    return Response(f"Employee with id {employee_id} not found.", status=422)

  request_data = json.loads(request.data)
  employee.name = _.get(request_data, "name", employee.name)
  employee.age = _.get(request_data, "age", employee.age)
  employee.email = _.get(request_data, "email", employee.email)
  employee.updated_at = datetime.now(pytz.utc)

  db.session.add(employee)
  db.session.commit()

  return Response(status=204, mimetype='application/json')
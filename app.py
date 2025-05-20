import json
import pydash as _
from datetime import datetime
import pytz
import os

from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USERNAME}:{DB_PASWORD}@{DB_URL}:5432/{DB_NAME}"
db = SQLAlchemy(app)

from models.employees import Employees
from services.employees import EmployeesService

@app.route("/")
def hello_world():
  return Response("Hello World!")

@app.route("/employees/add", methods=['POST'])
def add_employee():
  try:
    employees_service = EmployeesService(db.session)
    request_data = json.loads(request.data)
    employee = employees_service.insert_employee(request_data)

    return jsonify({
      "message": "success",
      "employee": employee.as_dict()
    })
  except Exception as ex:
    return Response(status=422, response=f"Failed to insert employee : {ex}")

@app.route("/employees/delete/<email>", methods=['DELETE'])
def delete_employee(email):
  try:
    employees_service = EmployeesService(db.session)
    employees_service.delete_employee(email)

    return Response(status=204, mimetype="application/json")
  except Exception as ex:
    return Response(status=422, response=f"Failed to delete employee : {ex}")

@app.route("/employees/get", methods=['GET'])
def get_all_employees():
  try:
    employees_service = EmployeesService(db.session)
    all_employees = employees_service.get_all()

    return jsonify({
      "message": "success",
      "employees": all_employees
    })
  except Exception as ex:
    return Response(500, response=f"Failed to get all employees : {ex}")

@app.route("/employees/update/<email>", methods=['PATCH'])
def update_employee(email):
  try:
    employees_service = EmployeesService(db.session)
    request_data = json.loads(request.data)

    if _.is_empty(request_data):
      return Response(status=422, response=f"Updated data cannot be empy.")

    employee = employees_service.update_employee(email=email, data=request_data)

    return jsonify({
      "message": "success",
      "employee": employee.as_dict()
    })
  except Exception as ex:
    return Response(status=500, response=f"Failed to update data : {ex}")
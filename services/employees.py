from models.employees import Employees
from queries.employees import EmployeesQuery

from datetime import datetime
import pydash as _
import pytz

class EmployeesService:
  def __init__(self, session):
    self.session = session
    self.employees_query = EmployeesQuery(self.session)

  def insert_employee(self, data):
    existing_employee = self.employees_query.get_by_email(
      email=data["email"]
    )

    if existing_employee is not None:
      raise RuntimeError(f"Employee already exist.")

    employee = Employees(
      name=data["name"],
      age=data["age"],
      email=data["email"]
    )
    self.employees_query.insert(employee)

  def delete_employee(self, email):
    existing_employee = self.employees_query.get_by_email(
      email=email
    )

    if existing_employee is None:
      raise RuntimeError(f"Employee do not exist.")

    self.employees_query.delete(existing_employee)

  def get_all(self):
    all_employees = self.employees_query.get_all()

    return [employee.as_dict() for employee in all_employees]

  def update_employee(self, email, data):
    existing_employee = self.employees_query.get_by_email(
      email=email
    )

    if existing_employee is None:
      raise RuntimeError(f"Employee do not exist.")

    existing_employee.name = _.get(data, "name", existing_employee.name)
    existing_employee.age = _.get(data, "age", existing_employee.age)
    existing_employee.email = _.get(data, "email", existing_employee.email)
    existing_employee.updated_at = datetime.now(pytz.utc)

    self.employees_query.update_employee(existing_employee)
from models.employees import Employees

class EmployeesQuery:
  def __init__(self, session):
    self.session = session

  def insert(self, employee):
    self.session.add(employee)
    self.session.commit()

  def delete(self, employee):
    self.session.delete(employee)
    self.session.commit()

  def update_employee(self, employee):
    self.session.add(employee)
    self.session.commit()

  def get_all(self):
    return self.session.query(Employees).all()

  def get_by_email(self, email):
    employee = self.session.query(Employees).filter_by(email=email).one_or_none()

    return employee

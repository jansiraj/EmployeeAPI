from __init__ import db
 
class Employee(db.Model):
    __tablename__ = "employee"
 
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer(),unique = True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    position = db.Column(db.String(80))
 
    def __init__(self, employee_id, email, name, age, position):
        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.age = age
        self.position = position
 
    def __repr__(self):
        return f"{self.name}:{self.employee_id}"
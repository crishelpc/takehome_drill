from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/records'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_number = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    middle_name = db.Column(db.String(64))
    sex = db.Column(db.String(10), nullable=False) 
    birthday = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "student_number": self.student_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "sex": self.sex,
            "birthday": self.birthday.strftime("%Y-%m-%d"),
        }

@app.route("/api/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify({"success": True, "data": [student.to_dict() for student in students]}), HTTPStatus.OK

@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify(
            {
                "success": False, 
                "error": "Student not found"
            }
        ), HTTPStatus.NOT_FOUND
    
    return jsonify(
        {
            "success": True, 
            "data": student.to_dict()
        }
    ), HTTPStatus.OK


if __name__ == "__main__":
    app.run(debug=True)
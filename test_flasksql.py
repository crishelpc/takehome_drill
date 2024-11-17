import pytest
import json
from flask_sql import app, db, Student

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/records' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  
            yield client
            db.session.remove()
            db.drop_all()  

def test_get_all_students(test_client):
    response = test_client.get('/api/students')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert isinstance(data['data'], list)

def test_create_student(test_client):
    new_student = {
        "student_number": "2022-8-1234",
        "first_name": "Fernando",
        "last_name": "Pineda",
        "middle_name": "Pineda",
        "sex": "Male",
        "birthday": "2003-11-03"
    }
    response = test_client.post('/api/students', json=new_student)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['student_number'] == '2022-8-1234' 

def test_get_single_student(test_client):
    student = Student(
        student_number="2022-9-0123",
        first_name="John",
        last_name="Smith",
        middle_name="M",
        sex="Male",
        birthday="2000-01-01"
    )
    db.session.add(student)
    db.session.commit()

    response = test_client.get(f'/api/students/{student.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['first_name'] == "John"

def test_update_student(test_client):
    student = Student.query.first()  
    update_data = {
        "first_name": "Updated Name"
    }
    response = test_client.put(f'/api/students/{student.id}', json=update_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['first_name'] == "Updated Name"

def test_delete_student(test_client):
    student = Student.query.first()  
    response = test_client.delete(f'/api/students/{student.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data'] == "Student deleted successfully."

    response = test_client.get(f'/api/students/{student.id}')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False

def test_create_student_missing_field(test_client):
    new_student = {
        "first_name": "Mike",
        "last_name": "Johnson",
        "sex": "Male",
        "birthday": "2001-03-03"
    }
    response = test_client.post('/api/students', json=new_student)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert "Missing required field" in data['error']
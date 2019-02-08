# coding=utf-8
from flask import Flask, jsonify, request

from flask_cors import CORS, cross_origin

from .entities.entity import Session, engine, Base
from .entities.exam import Exam, ExamSchema

#from .auth import AuthError, requires_auth

#creating the flask application
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Sapp.config['CORS_HEADERS'] = 'Content-Type'

# if needed, generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check for existing data
exams = session.query(Exam).all()

@app.route('/exams')
@cross_origin()
def get_exams():
    #fetching from databas
    session = Session()
    exam_objects = session.query(Exam).all()

    #transforming into json-serializable objects

    schema = ExamSchema(many=True)
    exams = schema.dump(exam_objects)

    #serializing as json
    session.close()
    return jsonify(exams.data)

@app.route('/exams', methods=['POST'])
#@requires_auth
def add_exam():
    #mount exam object
    posted_exam = ExamSchema(only=('title', 'description')).load(request.get_json())

    exam = Exam(**posted_exam.data, created_by="HTTP post request")

    #persist exam
    session = Session()
    session.add(exam)
    session.commit()

    #return created exam
    new_exam = ExamSchema().dump(exam).data
    session.close()
    return jsonify(new_exam), 201

desc = int(input("Desea agregar un examen?\n1-si\n2-No\n"))
if desc is 1:
    resp = 0
# create and persist dummy exam
    while resp is not 2:
        x = input("Ingrese el titulo del examen:\n")
        y = input("Ingrese la descripcion del examen:\n")
        z = input("Ingrese su nombre:\n")

        resp = int(input("Desea igresar un nuevo examen?\n1-si\n2-no\n"))
        python_exam = Exam(x,y,z)
        session.add(python_exam)
        session.commit()
        session.close()





    # reload exams
exams = session.query(Exam).all()
"""
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
"""
# show existing exams
print('### Exams:')
for exam in exams:
    print(f'({exam.id}) {exam.title} - {exam.description}')
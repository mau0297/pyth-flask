# coding=utf-8
from flask import Flask, jsonify, request

from flask_cors import CORS, cross_origin

from .entities.entity import Session, engine, Base
from .entities.exam import Exam, ExamSchema

#creating the flask application
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Sapp.config['CORS_HEADERS'] = 'Content-Type'

# if needed, generate database schema
Base.metadata.create_all(engine)

# generate database schema
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

if len(exams) == 0:
    # create and persist dummy exam
    python_exam = Exam("SQLAlchemy Exam", "Test your knowledge about SQLAlchemy.", "script")
    python_exam2 = Exam("Prueba","Esta es una prueba de sqlAlchemy","Mauricio")
    session.add(python_exam)
    session.add(python_exam2)
    session.commit()
    session.close()

    # reload exams
    exams = session.query(Exam).all()

# show existing exams
print('### Exams:')
for exam in exams:
    print(f'({exam.id}) {exam.title} - {exam.description}')